#!/usr/bin/env python3
"""check_layout.py — kiểm hình học SVG layout theo bất biến §7.4/§7.5 + tỉ lệ nghề KH-01.

Dùng:
    python3 check_layout.py <file .svg> [<00-project.yaml>]
    python3 check_layout.py <designs/<slug>/>      # tự tìm 03-layout.svg + 00-project.yaml

Kiểm (THUẦN HÌNH HỌC — tất định):
    §7.5  Tỉ lệ 1px=1cm: khung phòng SVG == room.width_cm × depth_cm.
    §7.4  Đồ khối: không lọt ngoài phòng; không chồng nhau (thảm/lớp mềm nét đứt là ngoại lệ);
          không đè cung quét cửa (đĩa-quạt bán kính = bề rộng cửa, chỉ cửa mở vào `in-*`).
    KH-01 Tỉ lệ đồ-trên-sàn ≤ ~45% (WARN nếu vượt).

KHÔNG tự tính bảng ergonomics ngữ nghĩa (cần biết "đâu là cạnh giường" — không suy ra
tin cậy từ hình học thuần): đó là việc của interior-layout + interior-review. Script in INFO nhắc.

Triết lý WARN-NOT-BLOCK: chỉ kiểm & báo. Exit 0 = sạch; 2 = có FAIL (đẩy stderr về Claude
khi gọi từ PostToolUse hook). Không phụ thuộc thư viện ngoài.
"""
import sys
import os
import re
import math

# nạp load_yaml từ check_project.py (cùng thư mục)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from check_project import load_yaml
except Exception:
    load_yaml = None

TOL = 1.0          # cm — bỏ qua chồng/lọt ≤ 1cm (chạm cạnh, sai số vẽ)
FLOOR_RATIO_MAX = 0.45
findings = []      # (level, code, msg)


def add(level, code, msg):
    findings.append((level, code, msg))


# ── parse SVG: rect & circle, kèm thuộc tính ────────────────────────────────
def _attrs(tag):
    return dict(re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', tag))


def parse_shapes(svg):
    rects, circles = [], []
    for m in re.finditer(r'<rect\b[^>]*?/?>', svg):
        a = _attrs(m.group(0))
        try:
            rects.append({
                'x': float(a.get('x', 0)), 'y': float(a.get('y', 0)),
                'w': float(a['width']), 'h': float(a['height']),
                'fill': a.get('fill', ''), 'dash': 'stroke-dasharray' in a,
            })
        except (KeyError, ValueError):
            continue
    for m in re.finditer(r'<circle\b[^>]*?/?>', svg):
        a = _attrs(m.group(0))
        try:
            circles.append({
                'cx': float(a['cx']), 'cy': float(a['cy']), 'r': float(a['r']),
                'fill': a.get('fill', ''), 'dash': 'stroke-dasharray' in a,
            })
        except (KeyError, ValueError):
            continue
    return rects, circles


def circle_bbox(c):
    return {'x': c['cx'] - c['r'], 'y': c['cy'] - c['r'],
            'w': 2 * c['r'], 'h': 2 * c['r'], 'dash': c['dash'],
            'fill': c['fill'], '_circle': c}


def overlap(a, b):
    """Diện tích giao của 2 bbox; >0 nếu chồng."""
    dx = min(a['x'] + a['w'], b['x'] + b['w']) - max(a['x'], b['x'])
    dy = min(a['y'] + a['h'], b['y'] + b['h']) - max(a['y'], b['y'])
    return dx, dy


def main():
    args = sys.argv[1:]
    if not args:
        print('Dùng: python3 check_layout.py <file.svg | thư mục dự án> [00-project.yaml]', file=sys.stderr)
        return 2

    target = args[0]
    if os.path.isdir(target):
        folder = target
        svg_path = os.path.join(folder, '03-layout.svg')
        yaml_path = os.path.join(folder, '00-project.yaml')
    else:
        svg_path = target
        folder = os.path.dirname(os.path.abspath(svg_path))
        yaml_path = args[1] if len(args) > 1 else os.path.join(folder, '00-project.yaml')

    if not os.path.exists(svg_path):
        print(f'Không tìm thấy SVG: {svg_path}', file=sys.stderr)
        return 2

    with open(svg_path, encoding='utf-8') as f:
        svg = f.read()

    room = None
    if load_yaml and os.path.exists(yaml_path):
        try:
            d = load_yaml(yaml_path)
            room = d.get('room') if isinstance(d, dict) else None
        except Exception as e:
            add('WARN', 'yaml', f'Không đọc được {os.path.basename(yaml_path)}: {e}')
    if room is None:
        add('WARN', 'yaml', 'Thiếu 00-project.yaml — chỉ kiểm chồng/giao trong SVG, không đối chiếu số đo thật.')

    rects, circles = parse_shapes(svg)
    if not rects:
        add('FAIL', 'SVG', 'Không tìm thấy <rect> nào — SVG rỗng/sai?')

    W = room.get('width_cm') if room else None
    D = room.get('depth_cm') if room else None

    # ── nhận diện khung phòng + §7.5 tỉ lệ ──
    room_rect = None
    for r in rects:
        is_grid = 'url(#grid' in r['fill']
        is_origin = abs(r['x']) <= TOL and abs(r['y']) <= TOL
        if is_grid or (is_origin and W and abs(r['w'] - W) <= TOL and abs(r['h'] - D) <= TOL):
            room_rect = r
            break
    if room_rect is None and rects:
        room_rect = max(rects, key=lambda r: r['w'] * r['h'])  # fallback: rect lớn nhất
        add('WARN', 'SVG', 'Không nhận ra khung phòng chắc chắn — dùng rect lớn nhất làm khung.')

    if room_rect and W and D:
        if abs(room_rect['w'] - W) > TOL or abs(room_rect['h'] - D) > TOL:
            add('FAIL', '§7.5', f"Khung phòng SVG {room_rect['w']:g}×{room_rect['h']:g} ≠ room {W}×{D} cm "
                                f"(sai tỉ lệ 1px=1cm hoặc sai số đo).")

    # khung dùng để kiểm "lọt ngoài"
    if W and D:
        rx0, ry0, rx1, ry1 = 0.0, 0.0, float(W), float(D)
    elif room_rect:
        rx0, ry0 = room_rect['x'], room_rect['y']
        rx1, ry1 = room_rect['x'] + room_rect['w'], room_rect['y'] + room_rect['h']
    else:
        rx0 = ry0 = rx1 = ry1 = None

    # ── đồ nội thất = mọi shape trừ khung phòng ──
    furniture = []
    for r in rects:
        if r is room_rect:
            continue
        furniture.append(r)
    for c in circles:
        furniture.append(circle_bbox(c))

    solid = [f for f in furniture if not f['dash']]   # bỏ thảm/lớp mềm nét đứt

    # ── lọt ngoài phòng (§7.4) ──
    if rx0 is not None:
        for f in solid:
            if (f['x'] < rx0 - TOL or f['y'] < ry0 - TOL or
                    f['x'] + f['w'] > rx1 + TOL or f['y'] + f['h'] > ry1 + TOL):
                lbl = '(tròn)' if '_circle' in f else ''
                add('FAIL', '§7.4', f"Đồ {lbl}tại ({f['x']:g},{f['y']:g}) cỡ {f['w']:g}×{f['h']:g} "
                                    f"lọt ngoài phòng [{rx0:g},{ry0:g}]–[{rx1:g},{ry1:g}].")

    # ── chồng nhau (§7.4) ──
    for i in range(len(solid)):
        for j in range(i + 1, len(solid)):
            dx, dy = overlap(solid[i], solid[j])
            if dx > TOL and dy > TOL:
                a, b = solid[i], solid[j]
                add('FAIL', '§7.4', f"Hai món chồng nhau ~{dx:g}×{dy:g}cm: "
                                    f"({a['x']:g},{a['y']:g} {a['w']:g}×{a['h']:g}) ∩ "
                                    f"({b['x']:g},{b['y']:g} {b['w']:g}×{b['h']:g}).")

    # ── đè cung quét cửa (§7.4) — chỉ cửa mở vào `in-*` ──
    doors = (room or {}).get('doors') or []
    for di, door in enumerate(doors):
        if not isinstance(door, dict):
            continue
        swing = str(door.get('swing', ''))
        if not swing.startswith('in'):
            continue
        wall, off, wid = door.get('wall'), door.get('offset_cm'), door.get('width_cm')
        if wall not in ('N', 'E', 'S', 'W') or not isinstance(off, int) or not isinstance(wid, int):
            continue
        right = swing.endswith('right')
        # toạ độ bản lề + bbox quạt quét (góc 90°, bán kính = wid)
        if wall in ('N', 'S'):
            wy = 0.0 if wall == 'N' else float(D if D else (ry1 or 0))
            hx = float(off + wid) if right else float(off)
            qx0, qx1 = (hx - wid, hx) if right else (hx, hx + wid)
            qy0, qy1 = (wy, wy + wid) if wall == 'N' else (wy - wid, wy)
            hinge = (hx, wy)
        else:  # E / W
            wx = 0.0 if wall == 'W' else float(W if W else (rx1 or 0))
            hy = float(off + wid) if right else float(off)
            qy0, qy1 = (hy - wid, hy) if right else (hy, hy + wid)
            qx0, qx1 = (wx, wx + wid) if wall == 'W' else (wx - wid, wx)
            hinge = (wx, hy)
        quad = {'x': qx0, 'y': qy0, 'w': qx1 - qx0, 'h': qy1 - qy0}
        for f in solid:
            dx, dy = overlap(f, quad)
            if dx <= TOL or dy <= TOL:
                continue
            # giao bbox với quạt → điểm gần bản lề nhất trong vùng giao
            ix0, iy0 = max(f['x'], quad['x']), max(f['y'], quad['y'])
            ix1, iy1 = min(f['x'] + f['w'], quad['x'] + quad['w']), min(f['y'] + f['h'], quad['y'] + quad['h'])
            cxp = min(max(hinge[0], ix0), ix1)
            cyp = min(max(hinge[1], iy0), iy1)
            dist = math.hypot(cxp - hinge[0], cyp - hinge[1])
            if dist <= wid - TOL:
                add('FAIL', '§7.4', f"Đồ tại ({f['x']:g},{f['y']:g}) đè cung quét cửa {wall} "
                                    f"(bản lề {hinge[0]:g},{hinge[1]:g}, bán kính {wid}cm; gần nhất {dist:.0f}cm).")

    # ── KH-01 tỉ lệ đồ-trên-sàn ──
    if W and D:
        area = 0.0
        for f in solid:
            if '_circle' in f:
                c = f['_circle']
                area += math.pi * c['r'] ** 2
            else:
                area += f['w'] * f['h']
        ratio = area / (W * D)
        if ratio > FLOOR_RATIO_MAX:
            add('WARN', 'KH-01', f"Tỉ lệ đồ-trên-sàn {ratio*100:.0f}% > {FLOOR_RATIO_MAX*100:.0f}% — "
                                 f"phòng dễ bí, cân nhắc bớt/thu nhỏ đồ.")
        else:
            add('INFO', 'KH-01', f"Tỉ lệ đồ-trên-sàn {ratio*100:.0f}% (≤{FLOOR_RATIO_MAX*100:.0f}% — đạt).")

    add('INFO', 'ergonomics', 'Bảng ergonomics (khoảng cách theo ngữ nghĩa) là việc của interior-layout/'
                              'interior-review — script chỉ kiểm hình học thuần.')

    # ── báo cáo ──
    fails = [f for f in findings if f[0] == 'FAIL']
    warns = [f for f in findings if f[0] == 'WARN']
    infos = [f for f in findings if f[0] == 'INFO']
    out = sys.stderr if fails else sys.stdout
    print(f'\n── check_layout: {os.path.relpath(svg_path)} ──', file=out)
    if not fails and not warns:
        print('✅ PASS — hình học hợp lệ.', file=out)
    for lvl, code, msg in fails + warns + infos:
        icon = {'FAIL': '❌', 'WARN': '⚠️ ', 'INFO': 'ℹ️ '}[lvl]
        print(f'{icon} [{code}] {msg}', file=out)
    print(f'→ {len(fails)} FAIL · {len(warns)} WARN · {len(infos)} INFO', file=out)
    if fails:
        print('  (warn-not-block: trình finding để user quyết, script KHÔNG tự sửa — ROADMAP §36)', file=out)
    return 2 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
