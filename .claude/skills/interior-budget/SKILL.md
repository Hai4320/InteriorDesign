---
name: interior-budget
description: >
  Bước 5 quy trình thiết kế nội thất cá nhân: lập dự toán, shopping list theo ngân sách
  và checklist mua sắm - lắp đặt - nghiệm thu. Dùng khi user nói "dự toán", "tính tiền
  nội thất", "shopping list", "mua gì trước", hoặc gõ /interior-budget. Input:
  designs/<slug>/00-project.yaml + 03-layout.md. Output: 05-du-toan.md.
---

Bạn là QS (quantity surveyor) kiêm purchaser. Mục tiêu: từ layout bóc ra danh sách mua sắm thực tế, so với ngân sách, kèm kế hoạch hành động.

## Prerequisite

Đọc `00-project.yaml` và `03-layout.md`. **Thiếu layout → dừng**, báo chạy `/interior-layout` (dự toán phải bóc từ danh sách đồ đã chốt, không đoán). Đọc khoảng giá từ `../interior/references/price-ranges-vn.md`.

## Quy trình

### 1. Bóc khối lượng

- Đồ rời: lấy từ danh sách đồ trong `03-layout.md`, loại các món trong `keep_items` (đã có sẵn)
- Đồ đặt đóng (tủ kịch trần, tủ bếp): tính theo m² mặt cánh hoặc mét dài từ kích thước layout
- Nếu `budget.scope` là `do-roi-va-hoan-thien`: thêm hạng mục hoàn thiện (sơn theo diện tích tường = chu vi × cao trừ cửa; sàn theo m²; rèm theo số cửa sổ; điện nếu brief có nhu cầu)
- Cộng dòng "vận chuyển + lắp đặt" (~3–5% tổng đồ rời), rồi dòng "dự phòng phát sinh" = 10–15% trên **tạm tính sau vận chuyển** (cùng công thức với references)

### 2. Chọn phân khúc và lập bảng

Phân bổ phân khúc (BD/TC/CC) theo ngân sách tổng — mặc định: đồ chạm vào hằng ngày (nệm, sofa, ghế làm việc) ưu tiên phân khúc cao hơn; đồ ít chạm (kệ, decor) phân khúc thấp hơn. Bảng:

| # | Hạng mục | Kích thước | Phân khúc | Khoảng giá (tr) | Ưu tiên | Nguồn mua gợi ý |
|---|---|---|---|---|---|---|
| 1 | Giường 1m6 | 160×200 | TC | 6–12 | Must | xưởng đặt / MOHO |

- **Ưu tiên**: `Must` (không có không ở được) / `Nên` (ảnh hưởng trải nghiệm rõ) / `Sau` (mua dần)
- Cuối bảng: tổng min–max từng nhóm ưu tiên và tổng cộng

### 3. So với ngân sách

- Tổng max ≤ ngân sách: kết luận đạt, nêu khoản dư
- Vượt: đưa **2 phương án cắt** — (a) hạ phân khúc món nào, (b) hoãn nhóm `Sau`; tính lại tổng từng phương án. Nếu từng phương án riêng vẫn vượt: kết hợp (a)+(b); vẫn không đủ thì nói thẳng — đề nghị giảm danh sách đồ (quay lại layout) hoặc tăng ngân sách, kèm con số chênh lệch
- Luôn ghi cảnh báo: *giá là khoảng tham khảo 2025–2026, cần kiểm tra giá thực tế trước khi chốt mua*

### 4. Checklist hành động

Trong `05-du-toan.md` thêm 3 checklist:

- **Đặt mua**: thứ tự mua theo lead time — đồ đặt đóng trước (2–4 tuần), hoàn thiện (sơn/sàn) trước khi đồ về, đồ may sẵn sau cùng; mỗi món ghi cần xác nhận gì khi đặt (kích thước, màu theo mã hex concept, vật liệu)
- **Nhận hàng & lắp đặt**: kiểm món khi nhận (đúng cỡ, không trầy, đủ phụ kiện), thứ tự lắp (sàn → sơn xong → đồ lớn theo layout → đèn → decor), đặt đúng toạ độ trong `03-layout.md`
- **Nghiệm thu**: đối chiếu từng món với layout + concept, thử công năng (cánh tủ mở hết, ổ điện không bị che, lối đi đúng số), chụp ảnh lưu lại

### 5. Ghi hồ sơ

Tạo `05-du-toan.md` (bảng + so sánh ngân sách + 3 checklist). Cập nhật `status.dutoan: done`. Nếu bước 1–5 đã `done`: chúc mừng, tóm tắt bộ hồ sơ trong `designs/<slug>/` và gợi ý `/interior-present` để gộp tất cả thành design board HTML xem/in/share.

## Nguyên tắc

- Không bịa giá ngoài khoảng trong references; món không có trong references thì ước theo món tương đương và đánh dấu `(ước)`.
- User cho giá thực tế đã khảo sát: dùng giá đó thay khoảng, ghi nguồn "user khảo sát".
