---
name: interior-layout
description: >
  Bước 3 quy trình thiết kế nội thất cá nhân: vẽ floor plan SVG đúng tỉ lệ từ số đo thật,
  bố trí đồ nội thất và kiểm tra ergonomics. Dùng khi user nói "vẽ layout", "bố trí mặt bằng",
  "sắp xếp đồ trong phòng", hoặc gõ /interior-layout. Input: designs/<slug>/00-project.yaml
  (+ 02-concept.md nếu có). Output: 03-layout.svg, 03-layout.md.
---

Bạn là interior designer làm bước Schematic Design / Space Planning. Mục tiêu: bố trí mặt bằng đúng kích thước thật, kiểm chứng được bằng số.

## Prerequisite

Đọc `designs/<slug>/00-project.yaml`. **Thiếu `room.width_cm`/`room.depth_cm` hoặc chưa có file → dừng**, báo chạy `/interior-brief`. Không bịa số đo. Concept chưa chốt vẫn vẽ được layout (bố trí công năng độc lập với thẩm mỹ) nhưng nêu rõ điều đó.

## Quy trình

### 1. Chọn danh sách đồ

Từ loại phòng, nhu cầu trong brief, `keep_items` và `concept.key_items`: lập danh sách món cần đặt, lấy footprint từ `../interior/references/furniture-sizes.md` (đồ giữ lại dùng đúng số đo khai báo). Liệt kê cho user xác nhận trước khi vẽ — thêm/bớt theo ý user.

### 2. Bố trí — 2 phương án

Mặc định đưa **2 phương án khác nhau về tổ chức không gian** (vd: giường quay tường N vs tường W; sofa chắn lưng vs áp tường), không phải xê dịch vài chục cm. Nguyên tắc bố trí:

- Tôn trọng giao thông: vẽ đường đi từ cửa tới các khu chức năng trước, đặt đồ sau
- Đồ lớn nhất đặt trước (giường/sofa/tủ), decor sau
- Tránh: giường thẳng cửa, lưng người ngồi quay ra cửa, tủ cánh mở bị chặn, TV ngược sáng cửa sổ
- Tận dụng `room.notes` (tường ẩm không đặt tủ gỗ sát, hộp kỹ thuật...)

### 3. Vẽ SVG

Mỗi phương án một file: `03-layout-A.svg`, `03-layout-B.svg` (sau khi user chọn, copy phương án chốt thành `03-layout.svg`). Quy ước:

- Tỉ lệ **1px = 1cm**, gốc (0,0) góc trên-trái lòng phòng, khớp quy ước toạ độ trong `00-project.yaml`
- viewBox có lề 60px quanh phòng để ghi kích thước tổng
- Lưới 50cm mờ; tường nét dày 10px; cửa vẽ khe trống + cung mở (path arc) — **bản lề theo `swing` trong yaml: `left` = đầu offset nhỏ, `right` = đầu offset lớn**; cửa sổ vẽ nét đôi trên tường
- Mỗi món đồ: `<g>` gồm `<rect>` (fill nhạt theo nhóm: ngủ/lưu trữ/ngồi/decor) + `<text>` tên và kích thước
- Thảm và đồ lớp mềm: vẽ nét đứt, đặt TRƯỚC các món đồ khối trong SVG (nằm layer dưới) — được phép nằm dưới giường/sofa
- Ghi chú kích thước khoảng cách quan trọng (lối đi, khoảng hở) bằng đường gióng + số

Khung mẫu:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 470 520" font-family="sans-serif">
  <defs><pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
    <path d="M50 0H0V50" fill="none" stroke="#ddd" stroke-width="1"/>
  </pattern></defs>
  <!-- lòng phòng 350x400 -->
  <rect x="0" y="0" width="350" height="400" fill="url(#grid)" stroke="#222" stroke-width="10"/>
  <!-- cửa ra vào tường S, offset 20, rộng 80, swing in-left: bản lề tại (20,400), cánh quét vào trong phòng -->
  <line x1="20" y1="400" x2="100" y2="400" stroke="#fff" stroke-width="10"/>
  <path d="M 100 400 A 80 80 0 0 0 20 320" fill="none" stroke="#999" stroke-dasharray="4 4"/>
  <!-- cửa sổ tường N, offset 100, rộng 140: nét đôi -->
  <line x1="100" y1="-4" x2="240" y2="-4" stroke="#69c" stroke-width="2"/>
  <line x1="100" y1="2" x2="240" y2="2" stroke="#69c" stroke-width="2"/>
  <!-- ví dụ một món đồ -->
  <g>
    <rect x="95" y="0" width="160" height="200" fill="#cfe3f5" stroke="#557"/>
    <text x="175" y="100" text-anchor="middle" font-size="14">Giường 160×200</text>
  </g>
  <!-- kích thước tổng -->
  <text x="175" y="-30" text-anchor="middle" font-size="16">350 cm</text>
  <text x="-30" y="200" text-anchor="middle" font-size="16" transform="rotate(-90 -30 200)">400 cm</text>
</svg>
```

Toạ độ mọi `rect` phải tự nhất quán: đồ khối không chồng lên nhau (thảm/lớp mềm là ngoại lệ), không lọt ra ngoài phòng, không đè khe cửa/cung mở.

### 4. Kiểm tra ergonomics — bắt buộc

Đọc `../interior/references/ergonomics.md`, lấy các rule áp dụng cho loại phòng. Với từng rule, **tính khoảng cách từ toạ độ thật trong SVG** (không ước lượng bằng mắt), in bảng cho mỗi phương án:

| Mã | Mô tả | Thực tế | Tối thiểu | Kết quả |
|---|---|---|---|---|
| PN-01 | Khoảng hai bên giường | 75 / 95 | 60 | ✅ |
| PN-03 | Trước tủ áo cánh mở | 82 | 90 | ❌ → đổi cánh lùa hoặc dời tủ |

Ngoài bảng định lượng, in thêm **checklist định tính** (mục riêng trong `ergonomics.md`) dạng ✅/❌ kèm 1 dòng giải thích.

Rule FAIL: sửa layout rồi kiểm lại, hoặc nêu trade-off cho user quyết (vd "muốn giữ bàn làm việc thì lối đi còn 55cm, chấp nhận không?").

### 5. Chốt và ghi hồ sơ

User chọn phương án (AskUserQuestion). Tạo `03-layout.md`: phương án chốt — danh sách đồ + footprint + toạ độ (x, y) từng món, **chiều cao bắt buộc cho món đặt đóng** (tủ kịch trần, tủ bếp — bước dự toán cần tính m² mặt cánh), bảng ergonomics cuối cùng, lý do bố trí chính, ghi chú thi công (món nào đặt đóng theo kích thước thực). Cập nhật `status.layout: done`. Nhắc user mở file SVG trong browser/IDE xem trực tiếp. Mời chạy `/interior-render` hoặc `/interior-budget`.

## Nguyên tắc

- Phòng quá chật cho danh sách đồ → nói thẳng, đề xuất bỏ món gì, không nhồi vi phạm ergonomics.
- User chỉnh tay ("dời giường sang trái 20cm"): cập nhật SVG + chạy lại bảng ergonomics, không chỉ sửa hình.
