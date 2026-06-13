# Chuẩn nghề thiết kế nội thất — tầng "khéo" (craft)

> Thư viện nguyên tắc nghề mà concept/layout phải **áp dụng và dẫn chiếu (cite)** thay vì "vibes". Vượt khỏi clearance tối thiểu (ở `ergonomics.md`) và kích thước đồ (ở `furniture-sizes.md`): đây là cái phân biệt một bố trí "đúng số" với một bố trí "ra dáng KTS".
>
> Mỗi nguyên tắc có **mã** (`KH-xx`) để cite trong `02-concept.md` / `03-layout.md` và để script `check_layout.py` đọc ngưỡng. Khi áp, ghi `KH-xx → quyết định` vào `rationale`. Ngưỡng có dấu `~` là khuyến nghị nghề, không phải luật cứng — vi phạm thì **báo + nêu trade-off**, không tự sửa.

## 1. Tỉ lệ & mật độ (proportion & density)

| Mã | Nguyên tắc | Ngưỡng | Ghi chú |
|---|---|---|---|
| KH-01 | **Tỉ lệ đồ trên sàn** (footprint đồ khối / diện tích lòng phòng) | ≤ ~40–45% | Vượt → phòng chật, bí. Tính từ tổng `w×d` đồ khối (trừ thảm/đồ lớp mềm) chia `width_cm×depth_cm`. Script kiểm. |
| KH-02 | **Một món thống trị** (anchor) | 1 món lớn nhất rõ ràng | Mỗi phòng cần một tâm điểm thị giác (giường ở PN, sofa/cụm ngồi ở PK). Tránh nhiều món "tranh nhau" cùng cỡ. |
| KH-03 | **Tỉ lệ trống/đặc** | chừa ≥ ~1 mảng tường/sàn trống liền mạch | Mắt cần chỗ "nghỉ". Không nhồi kín 4 tường. |
| KH-04 | **Chiều cao phân tầng** | đồ cao–thấp xen kẽ | Tránh mọi đồ cùng độ cao (đường chân trời phẳng, đơn điệu). Tủ kịch trần cân với đồ thấp (giường, ghế). |
| KH-05 | **Thảm định vùng** | thảm đủ lớn để ≥ chân trước đồ chính đứng trên | Thảm quá nhỏ làm cụm đồ "trôi". PK: mép trước sofa đè thảm ≥15cm; PN: thảm thò ra 2 bên giường ≥ ~40cm. |

## 2. Ánh sáng tự nhiên (quan hệ với `room.sun`)

Đọc `room.sun` (hướng la bàn thật) để quyết bố trí đồ chính so với cửa sổ. **N/E/S/W trong toạ độ vẽ KHÔNG phải hướng nắng** — luôn dùng `room.sun`.

| Mã | Nguyên tắc | Áp dụng |
|---|---|---|
| KH-10 | **Bàn làm việc/đọc đón sáng bên** | đặt bàn để cửa sổ ở **bên cạnh** (sáng tới từ trái với người thuận tay phải), không sau lưng (bóng đổ lên mặt bàn) cũng không thẳng trước mặt (chói màn hình). |
| KH-11 | **Giường tránh nắng gắt sáng sớm/chiều** | `sun: dong` → đầu giường tránh kề cửa sổ phía đông (nắng sớm chiếu mặt); `sun: tay` → tránh tường tây nóng buổi chiều cho vùng nghỉ. |
| KH-12 | **Không chắn nguồn sáng chính** | đồ cao (tủ kịch trần) không đặt che cửa sổ chính. Ưu tiên để cửa sổ "thở". |
| KH-13 | **TV/màn hình không ngược sáng** | màn hình vuông góc hoặc quay lưng vào tường có cửa sổ, tránh đối diện trực tiếp (xem cả DT-03 ở `ergonomics.md`). |

## 3. Chiếu sáng nhân tạo — phân 3 tầng

Một phòng "ra dáng" luôn có **đủ 3 tầng sáng**, không chỉ một đèn trần. Concept & render phải nêu cả ba.

| Mã | Tầng | Vai trò | Ví dụ |
|---|---|---|---|
| KH-20 | **Ambient** (nền) | sáng tổng thể, đều | đèn trần, hắt trần, downlight |
| KH-21 | **Task** (chức năng) | sáng tập trung chỗ làm việc cụ thể | đèn bàn làm việc, đèn đọc đầu giường, đèn gầm tủ bếp |
| KH-22 | **Accent** (điểm nhấn) | tạo chiều sâu, nhấn vật liệu/decor | đèn sàn, hắt tranh, đèn hắt kệ |
| KH-23 | **Nhiệt màu** | thống nhất tông | không gian nghỉ/ở: ~2700–3000K (ấm); bếp/làm việc: ~3500–4000K (trung tính). Tránh trộn lộn xộn. |

Quy tắc: mỗi phòng nêu được **tối thiểu ambient + task**; phòng ở (ngủ/khách) nên đủ cả 3. Thiếu task light ở chỗ đọc/làm việc = lỗi craft phổ biến.

## 4. Lưu trữ (storage)

| Mã | Nguyên tắc | Ngưỡng | Ghi chú |
|---|---|---|---|
| KH-30 | **Tỉ lệ lưu trữ / người** (phòng ngủ) | ≥ ~1.2–1.5m chiều ngang tủ áo / người lớn | Dưới mức này → thiếu chỗ, đồ tràn ra ngoài. Đối chiếu số người trong `users`. |
| KH-31 | **Lưu trữ tận dụng chiều cao** | ưu tiên kịch trần khi trần cao | Trần ≥260cm: tủ kịch trần tận dụng phần trên cất đồ ít dùng. Nhà thuê (constraint không khoan) → tủ rời cao. |
| KH-32 | **Lưu trữ gần điểm dùng** | đồ cất nơi sẽ dùng | Tủ giày gần cửa, kệ sách gần chỗ đọc — giảm di chuyển. |

## 5. Tầng ý đồ — parti dẫn dắt (xem schema §6)

`parti` không phải trang trí văn bản — nó là **bộ lọc quyết định**. Mỗi quyết định lớn phải trả lời "phục vụ parti thế nào?".

| Mã | Kiểm | Ghi chú |
|---|---|---|
| KH-40 | **Parti là một câu tổ chức không gian**, không lặp tên style | "Phòng tổ chức quanh trục ánh sáng cửa sổ" ✅ — "Phong cách Japandi tối giản" ❌ (đó là style, không phải ý đồ tổ chức). |
| KH-41 | **Concept–layout–vật liệu cùng kể một chuyện** | Nếu parti nói "trục ánh sáng" thì layout phải đặt vùng chức năng theo trục đó, vật liệu/màu phải hỗ trợ (sáng ở vùng đón nắng...). Review ③ kiểm điều này. |
| KH-42 | **Mọi quyết định defended được** | mỗi mục trong `rationale`: `quyết định → phục vụ nhu cầu/site/parti/chuẩn nào`. KTS thực thụ không có lựa chọn "vì thấy đẹp" mà không giải thích được. |

## 6. Cách dùng trong pipeline

- **interior-concept**: nêu `parti` (KH-40), 3 tầng sáng (KH-20..22), tỉ lệ màu 60-30-10 (schema §2). Cite mã vào rationale.
- **interior-layout**: kiểm KH-01 (tỉ lệ sàn), KH-05 (thảm), KH-10..13 (quan hệ cửa sổ theo `room.sun`), KH-30 (lưu trữ/người). `check_layout.py` tự tính KH-01 và cảnh báo KH-30.
- **interior-review**: dùng KH-41/KH-42 làm trục chấm "có ý đồ" (tầng 3).
