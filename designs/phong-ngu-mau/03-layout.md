# Layout — Phòng ngủ master (phong-ngu-mau)

*Bước 3 (Space Planning). Phòng 350×400×270 cm (~14 m²). Tỉ lệ SVG 1px = 1cm, gốc (0,0) góc trên-trái lòng phòng. Footprint lấy từ `furniture-sizes.md`; nệm 160×200 là đồ giữ lại.*

**Parti.** Phòng tổ chức quanh trục ánh sáng cửa sổ Đông Nam — vùng ngủ lùi vào phía trong yên tĩnh, bàn làm việc bám cửa sổ đón sáng tự nhiên (KH-10). Phương án chốt phục vụ trục này.

## Phương án chốt: **A — đầu giường tựa tường W** (user chọn)

### Danh sách đồ + toạ độ (x, y = góc trên-trái rect; đơn vị cm)

| Món | Footprint (r×s) | Toạ độ (x, y) | Chiếm | Ghi chú |
|---|---|---|---|---|
| Giường 1m6 (khung phẳng) | 200×160 (xoay ngang) | (0, 130) | x 0–200, y 130–290 | đầu tựa tường W; khung KHÔNG viền (viền +5/chiều thì cuối giường còn 77, vẫn đạt) |
| Tab đầu giường N | 40×45 | (0, 85) | x 0–40, y 85–130 | kề đầu giường |
| Tab đầu giường S | 40×45 | (0, 290) | x 0–40, y 290–335 | mép gần nhất cách tâm bản lề cửa (100,400) = 88.5 > 80 → ngoài cung mở |
| Đèn sàn washi Ø30 | Ø30 | tâm (60, 108) | x 45–75, y 93–123 | đèn đọc sách đầu giường, thay đèn tường (không khoan) |
| Bàn làm việc | 120×60 | (225, 0) | x 225–345, y 0–60 | góc NE; mép trái lọt 15cm dưới cửa sổ (bệ 90 > mặt bàn 75); cách tường E 5cm |
| Ghế công thái học | 60×60 | (255, 60) | x 255–315, y 60–120 | vị trí cất |
| Tủ quần áo cánh lùa | 65×180 (xoay dọc) | (282, 145) | x 282–347, y 145–325 | tựa tường E, **chừa khe 3cm chống ẩm** (tường giáp WC); cao 220 |
| Cây xanh chậu gốm Ø45 | Ø45 | tâm (317, 367) | x 294.5–339.5, y 344.5–389.5 | góc SE |
| Thảm dệt 160×230 | lớp soft | trải dưới 2/3 chân giường, mép Đông ~x 270 | — | lớp dưới giường, không vẽ rect riêng để bản vẽ không "chồng đồ" |

Kiểm hình học: mọi rect nằm trong 0–350 × 0–400, không chồng nhau, không đè khe cửa (x 20–100, tường S) và cung mở r=80.

### Bảng ergonomics PA-A (tính từ toạ độ thật)

| Mã | Mô tả | Thực tế | Tối thiểu | Kết quả |
|---|---|---|---|---|
| PN-01 | Bên giường phía N (y: 130 − 0, dải x 75–200 thoáng) | 130 | 60 | ✅ (≥ khuyến nghị 75) |
| PN-01 | Bên giường phía S (y: 400 − 290) | 110 | 60 | ✅ |
| PN-02 | Cuối giường → mặt tủ lùa (x: 282 − 200) | 82 | 60 | ✅ (dưới khuyến nghị 90 một chút) |
| PN-04 | Trước tủ áo cánh lùa (x: 282 − 200) | 82 | 60 | ✅ |
| PN-05 | Giường không thẳng cửa, đầu tựa tường đặc | đầu tựa tường W; cửa (tường S) nhìn vào cạnh giường, không thẳng trục giường | — | ✅ |
| PN-06 | Khoảng kéo ghế bàn làm việc (y: 145 − 60, tới mép tủ) | 85 | 75 | ✅ |
| LT-01 | Lối đi chính cửa → bàn/tủ (chỗ hẹp nhất: chân giường ↔ tủ) | 82 | 60 | ✅ |
| LT-03 | Vùng quét cửa r=80 quanh bản lề (100,400) trống | vật gần nhất (tab S, góc 40,335) cách 88.5 | 80 | ✅ |

**PA-A: 8/8 PASS, 0 FAIL.**

> ⚠️ LT-03 tính theo bản lề tại x=100 đúng như **ví dụ mẫu trong SKILL interior-layout** cho chính cửa này ("offset 20, rộng 80, mở vào-trái" → arc tâm (100,400)). Nếu thực tế bản lề ở phía x=20 thì tab S lọt vùng quét (cách 65 < 80) → **kiểm tra bản lề thật trước khi lắp; nếu bản lề trái, bỏ tab S hoặc thay bằng ghế đôn di động**.

## Phương án B (bị loại): đầu giường tựa tường N (dưới cửa sổ)

Toạ độ: giường (95,0) 160×200 · tab (45,0) & (260,0) 45×40 · tủ lùa (283,200) 65×180 · bàn (130,340) 120×60 quay mặt vào tường S · ghế (160,280) 60×60 · đèn sàn tâm (40,240) Ø30 · **không còn chỗ đạt chuẩn cho cây**.

| Mã | Mô tả | Thực tế | Tối thiểu | Kết quả |
|---|---|---|---|---|
| PN-01 | Hai bên giường (95−0 / 350−255) | 95 / 95 | 60 | ✅ |
| PN-02 | Cuối giường → ghế cất (280 − 200) | 80 | 60 | ✅ |
| PN-04 | Trước tủ lùa, đoạn y 340–380 bị bàn chặn (283 − 250) | 33 | 60 | ❌ → 1/3 dưới tủ khó dùng |
| PN-05 | Chân giường quay về tường S có cửa; dải cửa x 20–100 chớm trùng mép giường x 95–100; đầu giường che cửa sổ (bệ 90) | gần thẳng cửa | — | ❌ |
| PN-06 | Kéo ghế (340 − 200) | 140 | 75 | ✅ |
| LT-01 | Lối chính cửa → giường bên W, hẹp nhất tại đèn sàn (95 − 55) | 40 | 60 | ❌ → phải bỏ đèn/đổi tuyến |
| LT-03 | Vùng quét cửa trống (bàn cách mép quét 30) | trống | 80 | ✅ |

**PA-B: 4/7 PASS, 3 FAIL** (sửa được phải hy sinh đèn đọc + chấp nhận giường gần thẳng cửa + đầu giường che cửa sổ) → loại.

## Lý do bố trí chính (PA-A)

1. Đầu giường tựa tường W đặc (không cửa sổ, không giáp WC) — ngủ kín gió, đạt PN-05; hai bên giường đều ≥110/130 cho 2 vợ chồng.
2. Bàn làm việc góc NE cạnh cửa sổ Đông Nam: sáng tự nhiên buổi sáng, tối làm việc không quay lưng ra cửa.
3. Tủ lùa (không cánh mở) đặt tường E: tiết kiệm khoảng mở cánh ở phòng hẹp, chừa khe 3cm vì tường giáp WC.
4. Đèn sàn + tranh dựa + thảm: zero khoan tường, đúng ràng buộc nhà thuê.

## Ghi chú thi công

- **Tủ lùa 180×65×220 đặt đóng dạng đứng rời (freestanding)**, KHÔNG bắt vít vào tường — mang đi được khi trả nhà; đo lại thực tế khe tường E trước khi đặt.
- Khung giường chọn loại phẳng không viền để giữ đúng footprint 200×160.
- Xác nhận vị trí ổ điện trước khi chốt mép bàn làm việc (brief còn thiếu thông tin này).

→ `status.layout: done`. **Mở `03-layout.svg` trong browser/IDE để xem trực tiếp.** Bước kế: `/interior-render` hoặc `/interior-budget`.
