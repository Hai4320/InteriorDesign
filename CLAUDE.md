# CLAUDE.md — quy ước chung repo thiết kế nội thất

Repo này là bộ skill `interior` cho Claude Code: pipeline thiết kế nội thất cá nhân (6 bước) cho **nhà của chính user**. File này gom quy ước cấp repo; mỗi skill chỉ giữ phần đặc thù của bước.

## Nguyên tắc tối cao: Human-in-the-loop

Đây là thiết kế cho nhà của user — **mọi quyết định thẩm mỹ, ngân sách, sửa-dây-chuyền đều thuộc về user**. Cơ chế tự động chỉ **kiểm và báo, không tự quyết**:

1. **Gate/script/hook FAIL → trình finding + 2–3 lựa chọn kèm trade-off, user chọn.** KHÔNG tự sửa ngầm artifact. Ngoại lệ duy nhất được tự sửa: lỗi cú pháp thuần (YAML gãy, SVG không parse) — và vẫn phải báo đã sửa gì.
2. **Checkpoint quyết định bắt buộc giữ nguyên**: chọn concept, chọn phương án layout, duyệt danh sách đồ trước khi vẽ, duyệt phương án cắt dự toán. Không cơ chế nào nhảy qua các điểm này.
3. **Trade-off do user quyết**: rule FAIL nhưng user muốn giữ → ghi vào `accepted_tradeoffs` trong `00-project.yaml`; các lần kiểm sau bỏ qua mã đó (phân biệt "lỗi" với "lựa chọn").
4. **Hook cảnh báo, không chặn cứng** (warn-not-block): `PostToolUse` in finding để user thấy, không làm gãy thao tác.

## Collaborative protocol (mọi skill phải theo)

Hỏi theo **nhóm**, mỗi lần một nhóm (AskUserQuestion) → đưa **phương án kèm trade-off**, không hỏi trống → **user quyết** → **ghi file** → **xác nhận** lại ngắn gọn. Không dồn mọi câu hỏi một lúc; không tự quyết thay user ở điểm có tính thẩm mỹ/tiền bạc.

## Ngôn ngữ & đơn vị

- **Tiếng Việt** đầy đủ dấu cho mọi giao tiếp, mô tả, nội dung artifact. Thuật ngữ kỹ thuật & định danh code giữ nguyên gốc.
- **Độ dài**: cm (số nguyên). **Tiền**: triệu VND (hậu tố `_trieu`). **Màu**: hex 6 ký tự HOA `#RRGGBB`. **Ngày**: `YYYY-MM-DD`. Chi tiết: `schema.md` §0.
- Trường user không biết: `null` + note. **Không bịa số.**

## Cấu trúc & nguồn sự thật

- Mỗi dự án phòng: thư mục `designs/<slug>/` (slug kebab không dấu, do user đặt theo phòng — đây là giá trị domain tiếng Việt, KHÔNG đổi sang tiếng Anh).
- **Nguồn sự thật duy nhất** cho cấu trúc `00-project.yaml` + quy ước hệ toạ độ / bản lề cửa / palette: **`.claude/skills/interior/references/schema.md`**. Không định nghĩa lại các quy ước này ở nơi khác — chỉ trỏ tới.
- Chuẩn nghề (tỉ lệ, ánh sáng, lưu trữ, parti): `references/design-principles.md` (mã `KH-xx`).
- Reference khác: `ergonomics.md`, `furniture-sizes.md`, `styles.md`, `price-ranges-vn.md`. Template khung: `assets/`. Script kiểm: `interior/scripts/`.

## Pipeline & artifact

`interior-brief` → `interior-concept` → `interior-layout` → (`interior-render` ∥ `interior-budget`) → `interior-present`. Phụ thuộc & danh sách artifact: `schema.md` §4. Mỗi bước có **Gate trước khi set `status.*: done`** (chạy script liên quan + checklist). Trạng thái lưu ở `status` trong `00-project.yaml` (`pending | done | stale`).

## Kiểm tất định

- `scripts/check_project.py <thư mục dự án>` — validate yaml theo schema + bất biến §7 (hex, enum, cửa lọt tường).
- `scripts/check_layout.py <thư mục | file.svg>` — hình học SVG (tỉ lệ, chồng nhau, lọt ngoài, đè cung cửa) + KH-01.
- Tự chạy qua hook `PostToolUse` khi Write/Edit vào `designs/**` (`.claude/settings.json` → `hook_check.py`). Không phụ thuộc pyyaml.
