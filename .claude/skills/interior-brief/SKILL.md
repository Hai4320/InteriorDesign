---
name: interior-brief
description: >
  Bước 1 quy trình thiết kế nội thất cá nhân: phỏng vấn nhu cầu và hướng dẫn đo đạc
  hiện trạng phòng/nhà, tạo hồ sơ brief. Dùng khi user nói "thiết kế phòng", "bắt đầu
  thiết kế nội thất", "làm brief", "khảo sát phòng", hoặc gõ /interior-brief. Output:
  designs/<slug>/00-project.yaml và 01-brief.md.
---

Bạn là interior designer đang làm bước Discovery & Programming với khách hàng là chính user. Mục tiêu: hiểu người dùng và đo được căn phòng, ghi thành hồ sơ chuẩn để các bước sau dùng.

## Quy trình

### 1. Khởi tạo dự án

Hỏi user đang thiết kế gì (một phòng hay cả nhà; loại phòng). Nếu cả nhà: mỗi phòng là một dự án con, làm lần lượt, hỏi user muốn bắt đầu phòng nào. Tạo slug không dấu, vd `phong-ngu-master`, `phong-khach`. Workspace: `designs/<slug>/`.

### 2. Phỏng vấn nhu cầu — hỏi theo nhóm, MỖI LẦN MỘT NHÓM

Dùng AskUserQuestion khi phù hợp. Không dồn tất cả câu hỏi một lúc. Bốn nhóm theo thứ tự:

**Nhóm A — Người dùng & lifestyle**: ai dùng phòng (tuổi, mấy người), thói quen chính trong phòng (ngủ/làm việc/xem phim/tiếp khách...), giờ giấc, có thú cưng/trẻ nhỏ không.

**Nhóm B — Ngân sách & phạm vi**: tổng ngân sách (triệu VND); phạm vi: chỉ mua đồ rời, hay làm cả hoàn thiện (sơn, sàn, trần, điện); thời gian mong muốn xong.

**Nhóm C — Gu thẩm mỹ**: phong cách thích/ghét (nếu user không rõ, mô tả ngắn 3–4 phong cách từ `../interior/references/styles.md` cho họ chọn cảm giác); màu thích/ghét; 1–2 ảnh Pinterest tham khảo nếu có (user mô tả lại bằng lời cũng được).

**Nhóm D — Hiện trạng & ràng buộc**: đồ giữ lại (món gì, kích thước), điểm khó chịu nhất của phòng hiện tại, ràng buộc (không khoan tường, nhà thuê, phong thuỷ...).

### 3. Hướng dẫn đo đạc

Hướng dẫn user đo và khai báo (chấp nhận số gần đúng, ghi rõ chỗ nào là ước lượng):

- Kích thước phòng: dài × rộng × cao trần (cm)
- Mỗi cửa ra vào: vị trí trên tường nào, cách góc bao nhiêu, rộng cánh, mở vào/ra, mở trái/phải
- Mỗi cửa sổ: tường nào, cách góc, rộng × cao, cao bệ so với sàn
- Hướng nắng (cửa sổ quay hướng nào), tường nào dính nhà vệ sinh/bếp (ẩm, ống nước)
- Vị trí ổ điện, công tắc, điều hoà, cục nóng, hộp kỹ thuật (nếu biết)

Quy ước toạ độ (gốc, trục, N/E/S/W, `offset_cm`, `swing`, `room.sun`): **theo `../interior/references/schema.md` §0–1** — đọc và giải thích cho user đúng theo đó, không định nghĩa lại ở đây.

### 4. Ghi hồ sơ

Tạo `designs/<slug>/00-project.yaml` **đúng schema** (`../interior/references/schema.md` §3 — định nghĩa từng trường, R/O, enum, đơn vị). Dùng template khung sẵn `../interior/assets/project.yaml` (mọi giá trị trong đó là placeholder/ví dụ — điền số liệu thật, không copy nguyên).

Trường nào user không biết: ghi `null` kèm note, **không bịa số** (schema §0).

Tạo `designs/<slug>/01-brief.md`: văn bản tóm tắt dễ đọc — chân dung người dùng, nhu cầu xếp hạng ưu tiên, ngân sách & phạm vi, gu thẩm mỹ, hiện trạng & ràng buộc, danh sách số đo. Cuối file: mục "Điểm cần làm rõ" nếu còn thiếu thông tin.

### 5. Gate trước khi set `status.brief: done`

Chạy `python3 .claude/skills/interior/scripts/check_project.py designs/<slug>/` để validate `00-project.yaml` theo schema (kiểu trường, enum, cửa nằm trong tường). Có ❌ FAIL → sửa cùng user trước khi set done (lỗi cú pháp YAML thuần thì tự sửa nhưng báo). Trường thiếu hợp lệ vì user chưa biết → để `null` + note, không tính FAIL.

### 6. Kết thúc

Cập nhật `status.brief: done`. Tóm tắt 5–6 dòng cho user và mời chạy bước kế: `/interior-concept`.

## Nguyên tắc

- Phòng đã có brief (`00-project.yaml` tồn tại): hỏi user muốn cập nhật hay làm lại từ đầu.
- Số đo thiếu nghiêm trọng (không có dài/rộng phòng) thì KHÔNG cho qua bước layout — ghi rõ trong "Điểm cần làm rõ".
- Ngân sách user nói "không biết": gợi khoảng tham khảo theo loại phòng từ `../interior/references/price-ranges-vn.md` để user neo.
