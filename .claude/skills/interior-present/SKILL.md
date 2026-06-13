---
name: interior-present
description: >
  Bước 6 (tuỳ chọn) quy trình thiết kế nội thất cá nhân: gộp toàn bộ hồ sơ thiết kế
  thành design board HTML một trang — palette hiển thị màu thật, layout SVG nhúng inline,
  prompt render có nút copy, bảng dự toán — để xem, in hoặc share. Dùng khi user nói
  "design board", "trang trình bày", "xuất hồ sơ thiết kế", "tổng hợp hồ sơ", hoặc gõ
  /interior-present. Input: toàn bộ artifacts trong designs/<slug>/. Output: 06-presentation.html.
---

Bạn là designer làm bước Presentation. Mục tiêu: một file HTML tự chứa, mở phát thấy toàn bộ hồ sơ — thứ mà file markdown rời rạc và mã hex không truyền tải được.

## Prerequisite

Đọc toàn bộ `designs/<slug>/`. **Tối thiểu cần brief + concept + layout `done`** — thiếu thì dừng, báo chạy bước còn thiếu. Validate `00-project.yaml` theo `../interior/references/schema.md` trước khi chạy. Render/dự toán chưa có: vẫn làm, bỏ section tương ứng và ghi chú "chưa thực hiện" kèm lệnh skill để bổ sung.

## Yêu cầu kỹ thuật file HTML

- **Một file tự chứa**: CSS inline trong `<style>`, JS vanilla trong `<script>`, không CDN/font ngoài (dùng system font stack). Mở offline được.
- `lang="vi"`, charset UTF-8, responsive (max-width ~960px, căn giữa).
- **In được**: `@media print` — ẩn nút bấm, `page-break-before` giữa các section lớn, SVG không tràn trang.
- Màu chủ đạo của chính trang lấy từ palette concept (nền trang = màu nền concept pha ~50% trắng, heading = màu nhấn) — trang trình bày tự nó phải mang không khí concept.

## Cấu trúc trang (theo thứ tự)

1. **Header**: tên concept + tên dự án, loại phòng, kích thước rộng × sâu × cao = `room.width_cm` × `room.depth_cm` × `room.height_cm`, ngày lập dự án (`project.created`), ngân sách, scope. Một dòng trạng thái pipeline (✅/⬜ từng bước).
2. **Concept**: mô tả cảm xúc; **palette swatches** — mỗi màu một ô lớn (≥80px) màu thật kèm mã hex + vai trò (nền 60% / phụ 30% / nhấn 10% / vật liệu); danh sách vật liệu + key items; moodboard keywords (mỗi keyword một chip, kèm ghi chú "tìm trên Pinterest").
3. **Layout**: SVG phương án chốt nhúng **inline** (copy `<svg>` từ `03-layout.svg`, bỏ XML prolog nếu có); nếu tồn tại cả `03-layout-A.svg`/`-B.svg` thì thêm nút toggle A/B (JS ẩn/hiện, đánh dấu phương án chốt) — **khi nhúng nhiều SVG, đổi tên mọi `id` trùng nhau trong `<defs>`/pattern (hậu tố `-A`/`-B`) và sửa `url(#...)` tương ứng**, mỗi phương án kèm bảng ergonomics riêng của nó; dưới SVG: bảng ergonomics pass/fail, phần định tính = các mục "Lý do bố trí" + "Ghi chú thi công" + mọi cảnh báo ⚠️ trong `03-layout.md`; chú giải màu nhóm đồ.
4. **Render prompts** (nếu có): mỗi góc máy một card — tên góc, prompt chính (= biến thể đầu tiên trong file nguồn, thường Midjourney) trong `<pre>` + nút "Copy" (`navigator.clipboard.writeText`, fallback `execCommand` cho `file://`), các biến thể còn lại thu gọn trong `<details>`.
5. **Dự toán** (nếu có): bảng hạng mục y theo `05-budget.md`; dòng tổng min–max in đậm; banner so ngân sách 3 trạng thái — max ≤ ngân sách: nền xanh nhạt; min ≤ ngân sách < max: nền vàng nhạt, ghi cả hai vế + chênh cận trên; min > ngân sách: nền đỏ nhạt + số chênh; kèm tóm tắt phương án cắt nếu có; 3 checklist hành động trong `<details>`.
6. **Footer**: ngày xuất board (ngày chạy skill), ghi chú "giá là khoảng tham khảo, ảnh render là minh hoạ cảm giác", đường dẫn các file nguồn trong `designs/<slug>/`.

## Quy trình

1. Xác định dự án (nhiều dự án → hỏi user), đọc artifacts.
2. Dữ liệu lấy **nguyên văn từ artifacts**, không sáng tác lại — HTML chỉ là lớp trình bày. Số liệu (tổng dự toán, kết quả ergonomics) phải khớp 100% file nguồn. Hai nguồn mâu thuẫn nhau (vd hex trong yaml lệch với `02-concept.md`): ưu tiên artifact chi tiết của bước đó hơn yaml tóm tắt, và **báo user về discrepancy** để sửa nguồn.
3. Viết `designs/<slug>/06-presentation.html`.
4. Cập nhật `status.present: done` trong `00-project.yaml` (thêm key nếu chưa có).
5. Báo user mở file trong browser; nhắc Ctrl/Cmd+P để xuất PDF share.

## Gate trước khi set `status.present: done`

Chạy `python3 .claude/skills/interior/scripts/check_project.py designs/<slug>/` để chắc nguồn nhất quán trước khi gộp. Tự kiểm: số liệu trên board (palette hex, tổng dự toán, kết quả ergonomics, kích thước phòng) khớp 100% file nguồn; SVG nhúng không vỡ. Phát hiện discrepancy → báo user sửa NGUỒN, không "vá" trong HTML.

## Nguyên tắc

- Artifact nguồn đổi (layout sửa, dự toán cập nhật) → trang này phải sinh lại; ghi chú điều này ở footer.
- Không nhúng ảnh ngoài/base64 nặng — board là văn bản + SVG + swatch, nhẹ và mở tức thì.
