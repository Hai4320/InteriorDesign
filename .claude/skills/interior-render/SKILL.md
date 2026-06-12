---
name: interior-render
description: >
  Bước 4 quy trình thiết kế nội thất cá nhân: sinh prompt ảnh phối cảnh (Midjourney,
  DALL-E, Stable Diffusion) khớp concept và layout đã chốt. Dùng khi user nói "tạo prompt
  render", "sinh ảnh phối cảnh", "visualize phòng", hoặc gõ /interior-render. Input:
  designs/<slug>/02-concept.md + 03-layout.md. Output: 04-render-prompts.md.
---

Bạn là visualizer. Mục tiêu: prompt sinh ảnh bám sát concept (màu, vật liệu) và layout (đồ gì, đặt đâu, cửa sổ hướng nào) — không phải prompt chung chung "beautiful bedroom".

## Prerequisite

Đọc `00-project.yaml`, `02-concept.md`, `03-layout.md` của dự án. **Thiếu concept → dừng**, báo chạy `/interior-concept`. Thiếu layout: vẫn làm được nhưng cảnh báo ảnh sẽ không khớp bố cục thật, khuyên chạy `/interior-layout` trước.

## Quy trình

### 1. Dựng "scene facts" từ hồ sơ

Trước khi viết prompt, liệt kê facts buộc phải xuất hiện trong mọi prompt:

- Loại phòng + kích thước tương đối ("compact 14m² bedroom")
- Ánh sáng tự nhiên: **vị trí cửa sổ trong khung hình** lấy từ layout (tường N/E/S/W bản vẽ — đây chỉ là toạ độ vẽ); **chất lượng/góc nắng** lấy từ `room.sun` trong yaml (hướng la bàn thật — vd đông nam = nắng sáng ấm)
- 4–6 món đồ chính + vị trí tương quan (từ toạ độ layout: "bed against left wall, desk under window")
- Palette: gọi tên màu bằng lời + mã hex, vật liệu chủ đạo
- Style đã chốt

### 2. Viết 3–5 prompt theo góc máy

1. **Tổng thể** — từ cửa nhìn vào, thấy bố cục chính
2. **Góc hero** — cụm đồ quan trọng nhất (giường/sofa)
3. **Chi tiết vật liệu** — close-up texture (vải, gỗ, tường)
4. (tuỳ chọn) Góc ngược lại / ban đêm với đèn nhân tạo
5. (tuỳ chọn) Góc làm việc/khu phụ

Mỗi prompt theo cấu trúc: `[loại ảnh + style] + [scene facts cho góc này] + [vật liệu & màu] + [ánh sáng] + [camera & khung hình] + [chất lượng]`. Viết bằng tiếng Anh (model sinh ảnh hiểu tốt hơn), kèm 1 dòng dịch ý chính tiếng Việt.

### 3. Biến thể theo từng nền tảng

Với mỗi prompt, xuất 3 biến thể:

- **Midjourney v6**: prompt + `--ar 4:3 --style raw --v 6`; tham số góc rộng nội thất: thêm "wide angle 24mm"; tránh từ bị lọc.
- **DALL-E 3**: viết thành đoạn văn mô tả tự nhiên dài hơn (DALL-E ăn văn xuôi, không ăn tag).
- **SDXL**: tag-style, kèm **negative prompt** chuẩn nội thất: `blurry, distorted walls, warped furniture, extra windows, extra doors, lowres, watermark, text, people`.

### 4. Ghi hồ sơ

Tạo `04-render-prompts.md`: mục Scene Facts, các prompt theo góc máy (mỗi prompt đủ 3 biến thể + negative), mục "Cách dùng" ngắn (nơi dán, cách iterate: đổi seed, thêm/bớt 1 fact mỗi lần). Cập nhật `status.render: done`. Mời chạy `/interior-budget`.

## Nguyên tắc

- Ảnh sinh ra là minh hoạ cảm giác, không phải bản vẽ kỹ thuật — ghi rõ disclaimer này trong file.
- User có ảnh render rồi và muốn chỉnh ("muốn ấm hơn"): sửa đúng phần ánh sáng/màu của prompt, giữ nguyên scene facts.
