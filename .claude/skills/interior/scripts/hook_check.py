#!/usr/bin/env python3
"""hook_check.py — dispatcher cho PostToolUse hook (Write/Edit).

Đọc JSON hook trên stdin, lấy file_path. PATH-SCOPED: chỉ xử lý file trong `designs/`
(exit sớm nếu không phải) để không phí thời gian với file khác.

- file .yaml  → chạy check_project.py trên thư mục dự án
- file .svg   → chạy check_layout.py trên file đó

WARN-NOT-BLOCK (ROADMAP §36/§43): PostToolUse vốn KHÔNG chặn được (tool đã chạy xong).
Nếu check có ❌ FAIL hoặc ⚠️ WARN → in ra stderr + exit 2 để Claude THẤY finding và
báo lại user. Sạch → exit 0 (im lặng). Script KHÔNG bao giờ tự sửa artifact.
"""
import sys
import os
import json
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # không có input hợp lệ → không làm gì

    fp = (data.get('tool_input') or {}).get('file_path') or ''
    if not fp:
        return 0

    norm = fp.replace('\\', '/')
    parts = norm.split('/')
    if 'designs' not in parts:
        return 0  # path-scoped: ngoài designs/ → bỏ qua

    base = os.path.basename(norm)
    folder = os.path.dirname(fp)

    if base.endswith('.yaml'):
        script, arg = 'check_project.py', folder or '.'
    elif base.endswith('.svg'):
        script, arg = 'check_layout.py', fp
    else:
        return 0

    script_path = os.path.join(HERE, script)
    if not os.path.exists(script_path):
        return 0

    try:
        r = subprocess.run([sys.executable, script_path, arg],
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return 0

    combined = (r.stdout or '') + (r.stderr or '')
    if '❌' in combined or '⚠️' in combined:
        sys.stderr.write(combined)
        sys.stderr.write('\n[interior hook] Trên là finding kiểm tự động — báo user, KHÔNG tự sửa file.\n')
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
