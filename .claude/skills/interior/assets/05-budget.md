# Dự toán & Kế hoạch mua sắm — <tên dự án> (<slug>)

> Skeleton định dạng cho `05-budget.md`. Giữ thứ tự mục; điền số liệu thật.
> Bóc từ danh sách đồ `03-layout.md`; loại `keep_items`. Khoảng giá theo `../interior/references/price-ranges-vn.md` (tham khảo — phải kiểm giá thực tế trước khi mua).

*Bước 5. Scope `<do-roi | do-roi-va-hoan-thien>` → <có/không có hạng mục hoàn thiện>.*

## 1. Bảng dự toán

| # | Hạng mục | Kích thước | Phân khúc | Khoảng giá (tr) | Ưu tiên | Nguồn mua gợi ý |
|---|---|---|---|---|---|---|
| 1 | <món> | <w×d×h> | <BD\|TC\|CC> | <min – max> | <Must\|Nên\|Sau> | <gợi ý> |

### Tổng theo nhóm ưu tiên

| Nhóm | Min (tr) | Max (tr) |
|---|---|---|
| Must | | |
| Nên | | |
| Sau | | |
| **Cộng đồ rời** | | |
| Vận chuyển + lắp đặt (3–5% đồ rời) | | |
| **Tạm tính** | | |
| Dự phòng phát sinh (10–15% tạm tính) | | |
| **TỔNG DỰ TOÁN** | | |

> Mọi dòng tổng phải đúng số học (script `check_project.py` kiểm bất biến §7.3).

## 2. So với ngân sách <…> triệu

<Tổng vs ngân sách → đạt/vượt bao nhiêu. Nếu vượt: 2 phương án cắt (a) hạ phân khúc, (b) hoãn nhóm Sau; tính lại tổng từng phương án; khuyến nghị + rationale.>

> ⚠️ Giá là khoảng tham khảo 2025–2026 — bắt buộc kiểm giá thực tế (báo giá xưởng, giá sale) trước khi chốt mua.

## 3. Checklist hành động

### 3.1 Đặt mua (theo lead time)
- [ ] Đồ đặt đóng trước (lead 2–4 tuần) — ghi rõ khi đặt xác nhận: kích thước đúng layout, màu theo mã hex concept, vật liệu, ràng buộc thi công.
- [ ] (Nếu hoàn thiện) sơn/sàn trước khi đồ về.
- [ ] Đồ may sẵn sau cùng.

### 3.2 Nhận hàng & lắp đặt
- [ ] Kiểm từng món khi nhận (đúng cỡ, không trầy, đủ phụ kiện).
- [ ] Thứ tự lắp: đồ lớn trước theo layout → đèn → decor; đặt đúng toạ độ `03-layout.md`.

### 3.3 Nghiệm thu
- [ ] Đối chiếu từng món với `03-layout.svg` + bảng màu `02-concept.md`.
- [ ] Thử công năng (cánh tủ mở hết, lối đi đúng số ergonomics); đo lại lối đi thực tế; chụp ảnh lưu hồ sơ.

→ `status.budget: done`.
