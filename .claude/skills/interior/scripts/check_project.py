#!/usr/bin/env python3
"""check_project.py — kiểm 00-project.yaml theo schema.md + bất biến xuyên artifact (§7).

Dùng:
    python3 check_project.py <designs/<slug>/00-project.yaml | designs/<slug>/>

Triết lý: WARN-NOT-BLOCK (xem ROADMAP §36). Script chỉ KIỂM VÀ BÁO, không tự sửa.
In bảng PASS/FAIL/WARN ra stdout. Exit code:
    0 = sạch (không FAIL)
    2 = có FAIL  → khi gọi từ PostToolUse hook, exit 2 đẩy stderr về Claude để báo user
                   (PostToolUse vốn KHÔNG chặn được thao tác — tool đã chạy xong).
WARN không làm đổi exit code (mặc định) — chỉ là gợi ý nghề.

Không phụ thuộc thư viện ngoài: thử pyyaml, nếu thiếu dùng parser YAML-subset nội bộ
đủ cho cấu trúc 00-project.yaml (xem schema.md §3).
"""
import sys
import os
import re

# ── mã trong accepted_tradeoffs sẽ được nạp để bỏ qua khi báo ───────────────
HEX_RE = re.compile(r'#[0-9A-Fa-f]{3,8}\b')
HEX_OK = re.compile(r'^#[0-9A-F]{6}$')          # đúng spec: 6 ký tự HOA
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
WALLS = {'N', 'E', 'S', 'W'}
SWINGS = {'in-left', 'in-right', 'out-left', 'out-right'}
PROJECT_TYPES = {'phong-khach', 'phong-ngu', 'bep-an', 'phong-tam', 'khac'}
SCOPES = {'do-roi', 'do-roi-va-hoan-thien'}
STATUS_VALUES = {'pending', 'done', 'stale'}
SUN_VALUES = {'bac', 'nam', 'dong', 'tay', 'dong-bac', 'dong-nam', 'tay-bac', 'tay-nam'}
STATUS_KEYS = ['brief', 'concept', 'layout', 'render', 'budget', 'present']

findings = []   # (level, code, message) — level: FAIL | WARN | INFO


def add(level, code, msg):
    findings.append((level, code, msg))


# ─────────────────────────────────────────────────────────────────────────────
# Parser YAML-subset (fallback khi không có pyyaml)
# ─────────────────────────────────────────────────────────────────────────────
def _strip_comment(line):
    out, q = [], None
    for ch in line:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out).rstrip()


def _scalar(tok):
    tok = tok.strip()
    if tok == '' or tok == '~' or tok.lower() == 'null':
        return None
    if tok.lower() == 'true':
        return True
    if tok.lower() == 'false':
        return False
    if (tok[0] == '"' and tok[-1] == '"') or (tok[0] == "'" and tok[-1] == "'"):
        return tok[1:-1]
    if re.fullmatch(r'-?\d+', tok):
        return int(tok)
    if re.fullmatch(r'-?\d+\.\d+', tok):
        return float(tok)
    return tok


def _split_flow(s):
    """Tách phần tử top-level theo dấu phẩy, tôn trọng [] {} '' \"\"."""
    parts, depth, q, buf = [], 0, None, []
    for ch in s:
        if q:
            buf.append(ch)
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
            buf.append(ch)
        elif ch in '[{':
            depth += 1
            buf.append(ch)
        elif ch in ']}':
            depth -= 1
            buf.append(ch)
        elif ch == ',' and depth == 0:
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    if ''.join(buf).strip():
        parts.append(''.join(buf))
    return parts


def _parse_flow(tok):
    tok = tok.strip()
    if tok.startswith('[') and tok.endswith(']'):
        inner = tok[1:-1].strip()
        return [_parse_flow(p) for p in _split_flow(inner)] if inner else []
    if tok.startswith('{') and tok.endswith('}'):
        inner = tok[1:-1].strip()
        d = {}
        if inner:
            for p in _split_flow(inner):
                if ':' in p:
                    k, v = p.split(':', 1)
                    d[k.strip()] = _parse_flow(v)
        return d
    return _scalar(tok)


def _value(tok):
    tok = tok.strip()
    if tok and tok[0] in '[{':
        return _parse_flow(tok)
    return _scalar(tok)


def mini_yaml(text):
    """Parse subset YAML khối + flow đủ cho 00-project.yaml."""
    # bước 1: bỏ comment + dòng trống
    raw_lines = []
    for raw in text.split('\n'):
        s = _strip_comment(raw)
        if s.strip() == '':
            continue
        raw_lines.append(s)

    # bước 2: nối các dòng tiếp nối của flow [ ] / { } chưa cân bằng
    def _depth_delta(s):
        d, q = 0, None
        for ch in s:
            if q:
                if ch == q:
                    q = None
            elif ch in '"\'':
                q = ch
            elif ch in '[{':
                d += 1
            elif ch in ']}':
                d -= 1
        return d

    joined = []
    i = 0
    while i < len(raw_lines):
        cur = raw_lines[i]
        depth = _depth_delta(cur)
        while depth > 0 and i + 1 < len(raw_lines):
            i += 1
            cur = cur + ' ' + raw_lines[i].strip()
            depth += _depth_delta(raw_lines[i])
        joined.append(cur)
        i += 1

    lines = []
    for s in joined:
        indent = len(s) - len(s.lstrip(' '))
        lines.append((indent, s.strip()))

    pos = 0

    def parse_block(min_indent):
        nonlocal pos
        # quyết định map hay list dựa vào dòng đầu cùng cấp
        if pos >= len(lines):
            return None
        indent, content = lines[pos]
        if content.startswith('- '):
            return parse_list(indent)
        return parse_map(indent)

    def parse_map(cur_indent):
        nonlocal pos
        d = {}
        while pos < len(lines):
            indent, content = lines[pos]
            if indent < cur_indent or content.startswith('- '):
                break
            if indent > cur_indent:
                break
            if ':' not in content:
                pos += 1
                continue
            key, _, rest = content.partition(':')
            key, rest = key.strip(), rest.strip()
            pos += 1
            if rest == '':
                # giá trị lồng ở dòng sau (map/list) hoặc null
                if pos < len(lines) and lines[pos][0] > cur_indent:
                    d[key] = parse_block(lines[pos][0])
                else:
                    d[key] = None
            else:
                d[key] = _value(rest)
        return d

    def parse_list(cur_indent):
        nonlocal pos
        lst = []
        while pos < len(lines):
            indent, content = lines[pos]
            if indent != cur_indent or not content.startswith('- '):
                break
            item = content[2:].strip()
            pos += 1
            if item and item[0] in '[{':
                lst.append(_parse_flow(item))
            elif ':' in item:
                # map mở đầu ngay trên dòng "- key: val" → gom các dòng con
                key, _, rest = item.partition(':')
                m = {key.strip(): _value(rest) if rest.strip() else None}
                while pos < len(lines) and lines[pos][0] > cur_indent:
                    ind2, c2 = lines[pos]
                    if c2.startswith('- '):
                        break
                    k2, _, r2 = c2.partition(':')
                    pos += 1
                    if r2.strip() == '' and pos < len(lines) and lines[pos][0] > ind2:
                        m[k2.strip()] = parse_block(lines[pos][0])
                    else:
                        m[k2.strip()] = _value(r2)
                lst.append(m)
            else:
                lst.append(_scalar(item))
        return lst

    return parse_map(0) if lines else {}


def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return mini_yaml(text)


# ─────────────────────────────────────────────────────────────────────────────
# Kiểm tra schema
# ─────────────────────────────────────────────────────────────────────────────
def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def check_schema(d):
    if not isinstance(d, dict):
        add('FAIL', 'YAML', 'Không parse được 00-project.yaml thành cấu trúc map.')
        return

    # project
    p = d.get('project')
    if not isinstance(p, dict):
        add('FAIL', 'project', 'Thiếu khối `project` (bắt buộc).')
    else:
        if not p.get('slug'):
            add('FAIL', 'project.slug', 'Thiếu `slug`.')
        if p.get('type') not in PROJECT_TYPES:
            add('FAIL', 'project.type', f"`type`={p.get('type')!r} không thuộc {sorted(PROJECT_TYPES)}.")
        if not (isinstance(p.get('created'), str) and DATE_RE.match(p.get('created', ''))):
            add('FAIL', 'project.created', f"`created`={p.get('created')!r} phải dạng YYYY-MM-DD.")

    # status
    st = d.get('status')
    if not isinstance(st, dict):
        add('FAIL', 'status', 'Thiếu khối `status` (bắt buộc).')
    else:
        for k in STATUS_KEYS:
            if k not in st:
                add('FAIL', f'status.{k}', f'Thiếu `status.{k}`.')
            elif st[k] not in STATUS_VALUES:
                add('FAIL', f'status.{k}', f"`status.{k}`={st[k]!r} ∉ {sorted(STATUS_VALUES)} (bất biến §7.6).")

    # room
    room = d.get('room')
    if not isinstance(room, dict):
        add('FAIL', 'room', 'Thiếu khối `room` (bắt buộc).')
    else:
        for k in ('width_cm', 'depth_cm', 'height_cm'):
            if not is_int(room.get(k)) or room.get(k, 0) <= 0:
                add('FAIL', f'room.{k}', f"`room.{k}`={room.get(k)!r} phải là số nguyên cm > 0.")
        W, D = room.get('width_cm'), room.get('depth_cm')
        check_openings(room.get('doors'), 'doors', W, D, True)
        check_openings(room.get('windows'), 'windows', W, D, False)
        sun = room.get('sun')
        if sun is not None and sun not in SUN_VALUES:
            add('WARN', 'room.sun', f"`room.sun`={sun!r} ∉ {sorted(SUN_VALUES)}.")

    # budget
    b = d.get('budget')
    if not isinstance(b, dict):
        add('FAIL', 'budget', 'Thiếu khối `budget` (bắt buộc).')
    else:
        if not is_int(b.get('total_trieu')) or b.get('total_trieu', 0) <= 0:
            add('FAIL', 'budget.total_trieu', f"`total_trieu`={b.get('total_trieu')!r} phải số nguyên triệu > 0.")
        if b.get('scope') not in SCOPES:
            add('FAIL', 'budget.scope', f"`scope`={b.get('scope')!r} ∉ {sorted(SCOPES)}.")

    if not d.get('users'):
        add('FAIL', 'users', 'Thiếu `users` (chân dung người dùng, bắt buộc).')

    check_concept(d.get('concept'))


def check_openings(items, name, W, D, is_door):
    if items is None:
        if is_door:
            add('WARN', f'room.{name}', 'Không có cửa ra vào — kiểm lại có thật vậy không.')
        return
    if not isinstance(items, list):
        add('FAIL', f'room.{name}', f'`room.{name}` phải là list.')
        return
    for i, it in enumerate(items):
        tag = f'room.{name}[{i}]'
        if not isinstance(it, dict):
            add('FAIL', tag, 'Mỗi cửa/cửa sổ phải là map.')
            continue
        wall = it.get('wall')
        if wall not in WALLS:
            add('FAIL', f'{tag}.wall', f"`wall`={wall!r} ∉ {sorted(WALLS)}.")
        off, wid = it.get('offset_cm'), it.get('width_cm')
        if not is_int(off):
            add('FAIL', f'{tag}.offset_cm', f"`offset_cm`={off!r} phải số nguyên.")
        if not is_int(wid):
            add('FAIL', f'{tag}.width_cm', f"`width_cm`={wid!r} phải số nguyên.")
        if is_door:
            if it.get('swing') not in SWINGS:
                add('FAIL', f'{tag}.swing', f"`swing`={it.get('swing')!r} ∉ {sorted(SWINGS)}.")
        # nằm trong chiều dài tường?
        if is_int(off) and is_int(wid) and wall in WALLS and is_int(W) and is_int(D):
            wall_len = W if wall in ('N', 'S') else D
            if off < 0 or off + wid > wall_len:
                add('FAIL', tag, f"Cửa/cửa sổ vượt chiều dài tường {wall} ({wall_len}cm): offset {off} + rộng {wid} = {off+wid}.")


def check_concept(c):
    if c is None:
        add('INFO', 'concept', 'concept = null (chưa chạy interior-concept) — bỏ qua kiểm concept.')
        return
    if not isinstance(c, dict):
        add('FAIL', 'concept', '`concept` phải là map hoặc null.')
        return
    for k in ('name', 'parti', 'style'):
        if not c.get(k):
            add('FAIL', f'concept.{k}', f'Thiếu `concept.{k}` (bắt buộc khi concept ≠ null — schema §3, §6).')
    pal = c.get('palette')
    if not isinstance(pal, dict):
        add('FAIL', 'concept.palette', 'Thiếu `palette` hoặc sai kiểu.')
    else:
        for role in ('nen', 'nhan', 'vatlieu'):
            v = pal.get(role)
            if not (isinstance(v, str) and HEX_OK.match(v)):
                add('FAIL', f'palette.{role}', f"`{role}`={v!r} phải hex 6 ký tự HOA (#RRGGBB) — schema §0, §2.")
        phu = pal.get('phu')
        if not (isinstance(phu, list) and len(phu) == 2):
            add('FAIL', 'palette.phu', f"`phu` phải đúng 2 hex, nhận {phu!r} (§2).")
        else:
            for v in phu:
                if not (isinstance(v, str) and HEX_OK.match(v)):
                    add('FAIL', 'palette.phu', f"phần tử `phu`={v!r} phải hex 6 ký tự HOA.")
    for k in ('materials', 'key_items'):
        if not isinstance(c.get(k), list) or not c.get(k):
            add('FAIL', f'concept.{k}', f'`{k}` phải là list không rỗng.')


# ─────────────────────────────────────────────────────────────────────────────
# Bất biến xuyên artifact (§7) — cần đọc các file khác trong cùng thư mục
# ─────────────────────────────────────────────────────────────────────────────
def palette_hexes(d):
    c = d.get('concept')
    if not isinstance(c, dict):
        return []
    pal = c.get('palette')
    if not isinstance(pal, dict):
        return []
    out = []
    for role in ('nen', 'nhan', 'vatlieu'):
        v = pal.get(role)
        if isinstance(v, str):
            out.append(v)
    phu = pal.get('phu')
    if isinstance(phu, list):
        out += [v for v in phu if isinstance(v, str)]
    return out


def check_invariants(d, folder):
    # §7.1: mọi hex palette phải xuất hiện trong 02-concept.md (palette ⊆ concept-md)
    pal = palette_hexes(d)
    concept_md = os.path.join(folder, '02-concept.md')
    if pal and os.path.exists(concept_md):
        with open(concept_md, encoding='utf-8') as f:
            txt = f.read()
        found = {h.upper() for h in HEX_RE.findall(txt)}
        for h in pal:
            if h.upper() not in found:
                add('FAIL', '§7.1', f"Hex palette {h} (00-project.yaml) KHÔNG có trong 02-concept.md — hai nơi lệch (02 là chuẩn, sửa yaml theo).")
        extra = found - {h.upper() for h in pal}
        if extra:
            add('INFO', '§7.1', f"02-concept.md có hex ngoài palette: {sorted(extra)} — thường là màu concept đã loại / chi tiết nhỏ; kiểm nếu bất ngờ.")

    # §7.2: đồ trong 05-budget.md ⊆ đồ trong 03-layout.md — báo nhẹ (so khớp tên khó, chỉ cảnh báo nếu thiếu file)
    layout_md = os.path.join(folder, '03-layout.md')
    budget_md = os.path.join(folder, '05-budget.md')
    if os.path.exists(budget_md) and not os.path.exists(layout_md):
        add('WARN', '§7.2', '05-budget.md tồn tại nhưng thiếu 03-layout.md — dự toán phải bóc từ layout.')


# ─────────────────────────────────────────────────────────────────────────────
def resolve_path(arg):
    if os.path.isdir(arg):
        return os.path.join(arg, '00-project.yaml')
    return arg


def main():
    if len(sys.argv) < 2:
        print('Dùng: python3 check_project.py <designs/<slug>/00-project.yaml | thư mục dự án>', file=sys.stderr)
        return 2
    path = resolve_path(sys.argv[1])
    if not os.path.exists(path):
        print(f'Không tìm thấy: {path}', file=sys.stderr)
        return 2
    folder = os.path.dirname(os.path.abspath(path))

    try:
        d = load_yaml(path)
    except Exception as e:
        print(f'❌ Lỗi cú pháp YAML khi đọc {path}: {e}', file=sys.stderr)
        return 2

    check_schema(d)
    check_invariants(d, folder)

    fails = [f for f in findings if f[0] == 'FAIL']
    warns = [f for f in findings if f[0] == 'WARN']
    infos = [f for f in findings if f[0] == 'INFO']

    out = sys.stderr if fails else sys.stdout
    rel = os.path.relpath(path)
    print(f'\n── check_project: {rel} ──', file=out)
    if not findings:
        print('✅ PASS — yaml hợp schema, không phát hiện vấn đề.', file=out)
    for lvl, code, msg in fails + warns + infos:
        icon = {'FAIL': '❌', 'WARN': '⚠️ ', 'INFO': 'ℹ️ '}[lvl]
        print(f'{icon} [{code}] {msg}', file=out)
    print(f'→ {len(fails)} FAIL · {len(warns)} WARN · {len(infos)} INFO', file=out)
    if fails:
        print('  (warn-not-block: script KHÔNG tự sửa — trình finding để user quyết; xem ROADMAP §36)', file=out)
    return 2 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
