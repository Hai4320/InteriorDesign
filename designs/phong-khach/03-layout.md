# Layout — Phòng khách (`phong-khach`)

> Bước 3/6 · Space Planning · phương án chốt: **🅐 "Làm việc đón nắng phía Bắc · Lounge quây phía Nam"**
> File hình: `03-layout.svg` (mở trong browser/IDE để xem trực tiếp). Phương án thay thế lưu ở `03-layout-A.svg` / `03-layout-B.svg`.

## Parti (nhắc lại — KH-40)

> **Cả phòng mở quanh trục cửa sổ Đông — không có gì cao chắn nắng, mọi bề mặt sáng để dội ánh sáng buổi sáng đi khắp phòng.**

Bố trí này tách phòng thành 2 vùng theo chiều sâu (Bắc–Nam), cả hai đều mở về cửa sổ Đông ở giữa tường E; lối vào (cửa W) đổ thẳng vào khoảng trống trung tâm giàu ánh sáng.

## Quy ước bản vẽ

Nhìn từ trên xuống, gốc (0,0) góc trên-trái, x sang phải, y xuống dưới, 1px=1cm. Tường: **N** trên, **S** dưới, **W** trái (có cửa), **E** phải (có cửa sổ). Cửa sổ Đông là nguồn sáng thật (`room.sun: dong`).

## Danh sách đồ — footprint & toạ độ

| Món | Nhóm | Rộng×Sâu (cm) | Toạ độ (x, y) góc trên-trái | Cao (cm) | Ghi chú |
|---|---|---|---|---|---|
| Kệ sách đứng sàn | lưu trữ | 80×30 | (40, 0) | ~190 | tựa tường N, gần lối vào & vùng làm việc |
| Bàn đa dụng (làm việc + ăn) | làm việc | 140×70 | (300, 30) | 75 | góc Đông-Bắc, cửa sổ E ở bên phải |
| Ghế làm việc | ngồi | 60×60 | (340, 110) | — | footprint khi cất; kéo ra về phía Nam |
| Sofa 3 chỗ | ngồi | 210×90 | (230, 500) | 80 | tựa tường S, quay mặt lên N; đầu phải sát cửa sổ |
| Bàn trà | ngồi | 110×55 | (280, 410) | 40 | trước sofa |
| Đèn sàn arc | decor | 35×35 | (450, 460) | 150–180 | cạnh đầu phải sofa, hắt xuống đọc sách |
| Cây xanh chậu lớn | decor | Ø45 | tâm (470, 430) | — | cạnh cửa sổ, đón nắng |
| Thảm len | lớp mềm | 290×200 | (180, 400) | — | định vùng lounge; mép trước sofa đè thảm (KH-05) |

*Không có món đặt đóng kịch trần/kịch tường trong phương án này — toàn đồ rời (phù hợp nhà thuê, không khoan tường). Kệ sách là đồ rời đứng sàn.*

## Bảng ergonomics cuối cùng (tính từ toạ độ thật)

| Mã | Mô tả | Thực tế | Tối thiểu | Kết quả |
|---|---|---|---|---|
| LT-01 | Lối đi chính (cửa W → trung tâm phòng) | ~160cm | 60 | ✅ |
| LT-03 | Khoảng trống trước cửa (cung mở bán kính 90) | 90 + trống | 90 | ✅ |
| PK-01 | Sofa ↔ bàn trà | 35 | 35 | ✅ *(đạt tối thiểu; dưới khuyến nghị 40–45 — có thể đẩy bàn trà thêm 5–10cm)* |
| PK-04 | Khoảng trống quanh cụm sofa (ra vào chỗ ngồi) | 60+ | 45 | ✅ |
| PN-06 | Khoảng kéo ghế làm việc (về phía Nam) | ~240cm | 75 | ✅ |
| KH-01 | Tỉ lệ đồ-trên-sàn | 14% | ≤45% | ✅ *(script tự tính)* |

### Checklist định tính

- **DT-02** Người ngồi không quay lưng thẳng ra cửa: ✅ — sofa quay mặt lên N (lưng tựa tường S); người ở bàn làm việc quay mặt lên N, cửa ở tường W bên trái, không sau lưng.
- **DT-03** TV không ngược sáng: ✅ — không có TV (nhu cầu là đọc/làm việc).
- **DT-04** Cánh cửa/cánh tủ mở hết hành trình không vướng: ✅ — cung quét cửa W (bán kính 90, vùng x0–90 / y255–345) hoàn toàn trống; kệ sách mở mặt mở.
- **DT-05** Đồ gỗ không kê sát tường ẩm: ✅/N/A — chưa khai báo tường ẩm (xem `room.notes`).
- **KH-12** Không chắn nguồn sáng chính: ✅ — không đặt đồ cao ở tường E; cửa sổ "thở".
- **KH-10** Bàn làm việc đón sáng bên: ⚠️ — cửa sổ E ở **bên phải** người ngồi (lý tưởng là bên trái cho người thuận tay phải, tránh bóng tay viết). Có thể **lật bàn** để cửa sổ sang trái nếu thấy vướng; với laptop/đọc thì sáng phải vẫn tốt.

## Rationale (decision log — KH-42)

| Quyết định | Phục vụ |
|---|---|
| Tách 2 vùng Bắc (làm việc) – Nam (lounge), trung tâm để trống | → parti "phòng mở quanh trục cửa sổ"; nỗi đau **"chật"** giải bằng khoảng trống trung tâm liền mạch (KH-03). |
| Sofa tựa tường S, quay mặt lên N, đầu phải sát cửa sổ E | → đọc sách trên sofa đón nắng bên phải (parti); KH-02 sofa làm anchor; DT-02 lưng tựa tường, không quay ra cửa. |
| Đèn sàn arc + cây đặt cạnh cửa sổ | → tầng task/accent cho góc đọc (KH-21/22); cây đón nắng. |
| Bàn làm việc ở góc Đông-Bắc, không kê tường E | → đón sáng tự nhiên (KH-10) mà vẫn để cửa sổ thở (KH-12). |
| Toàn đồ rời đứng sàn, không kệ treo | → ràng buộc **nhà thuê + không khoan tường**; KH-31. |
| Bảng màu sáng (concept) + đồ chân thoáng, để thấp | → nỗi đau **"tối"**: bề mặt sáng dội nắng; nhìn xuyên gầm đồ làm sàn liền mạch. |

## Ghi chú thi công

- **Không có hạng mục đặt đóng** theo kích thước thực trong phương án này — tất cả là đồ rời mua sẵn, thuận cho nhà thuê.
- Khi mua, ưu tiên: sofa **chân gỗ hở** (nhìn xuyên gầm → rộng), kệ sách **đứng sàn không cần khoan**, đèn arc + đèn bàn thay cho đèn âm trần (không can thiệp trần nhà thuê).
- Khoảng sofa↔bàn trà đang ở mức tối thiểu 35cm — nếu muốn duỗi chân thoải mái hơn, đẩy bàn trà về phía cửa sổ thêm 5–10cm (vẫn trong thảm).
- **Cần đo lại trước khi mua**: vị trí ổ điện cho bàn làm việc (góc Đông-Bắc) — nếu thiếu ổ gần đó, tính phương án dây/ổ kéo dài (nhà thuê, không đi dây âm).
