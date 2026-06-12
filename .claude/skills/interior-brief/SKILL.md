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

Quy ước toạ độ để bước layout dùng: gốc (0,0) là góc trên-trái của bản vẽ nhìn từ trên xuống, trục x sang phải, y xuống dưới; tường đặt tên N/E/S/W (N = cạnh trên bản vẽ). **N/E/S/W chỉ là tên toạ độ vẽ, không phải hướng la bàn** — hướng nắng thật ghi riêng vào `room.sun`. `offset_cm` của cửa/cửa sổ luôn đo theo **chiều tăng trục toạ độ** (x cho tường N/S, y cho tường E/W). `swing` của cửa: `in/out` + phía bản lề, trong đó `left` = bản lề ở đầu offset nhỏ, `right` = bản lề ở đầu offset lớn.

### 4. Ghi hồ sơ

Tạo `designs/<slug>/00-project.yaml` theo template (**mọi giá trị dưới đây là VÍ DỤ minh hoạ — điền số liệu thật của user, không copy nguyên**):

```yaml
project:
  slug: phong-ngu-master
  type: phong-ngu        # phong-khach | phong-ngu | bep-an | phong-tam | khac
  created: 2026-06-12
status:                  # cập nhật bởi từng skill khi xong
  brief: done
  concept: pending       # pending | done
  layout: pending
  render: pending
  dutoan: pending
  present: pending       # tuỳ chọn — design board HTML
room:
  width_cm: 350          # cạnh ngang bản vẽ (tường N/S)
  depth_cm: 400          # cạnh dọc bản vẽ (tường E/W)
  height_cm: 270
  doors:
    - wall: S
      offset_cm: 20      # cách góc trái/trên của tường đó
      width_cm: 80
      swing: in-left     # in/out + left/right
  windows:
    - wall: N
      offset_cm: 100
      width_cm: 140
      height_cm: 140
      sill_cm: 90
  sun: dong-nam          # hướng LA BÀN thật của cửa sổ chính (không phải N/E/S/W bản vẽ)
  notes: ["tường E giáp WC, có hộp kỹ thuật góc NE"]
budget:
  total_trieu: 50
  scope: do-roi          # do-roi | do-roi-va-hoan-thien
  timeline: "1 thang"
users: "vợ chồng 30 tuổi, làm việc tối tại phòng"
pain_points: ["thiếu chỗ cất đồ", "đèn trần chói khi đọc sách"]
style_hints:
  like: [scandinavian, japandi]
  dislike: [neo-classic]
  colors_like: [be, xanh]
  colors_dislike: [do]
keep_items:
  - {name: "nệm 1m6", w: 160, d: 200}
constraints: ["nhà thuê - hạn chế khoan tường"]
concept: null            # interior-concept ghi vào sau khi chốt
```

Trường nào user không biết: ghi `null` kèm note, đừng bịa.

Tạo `designs/<slug>/01-brief.md`: văn bản tóm tắt dễ đọc — chân dung người dùng, nhu cầu xếp hạng ưu tiên, ngân sách & phạm vi, gu thẩm mỹ, hiện trạng & ràng buộc, danh sách số đo. Cuối file: mục "Điểm cần làm rõ" nếu còn thiếu thông tin.

### 5. Kết thúc

Cập nhật `status.brief: done`. Tóm tắt 5–6 dòng cho user và mời chạy bước kế: `/interior-concept`.

## Nguyên tắc

- Phòng đã có brief (`00-project.yaml` tồn tại): hỏi user muốn cập nhật hay làm lại từ đầu.
- Số đo thiếu nghiêm trọng (không có dài/rộng phòng) thì KHÔNG cho qua bước layout — ghi rõ trong "Điểm cần làm rõ".
- Ngân sách user nói "không biết": gợi khoảng tham khảo theo loại phòng từ `../interior/references/price-ranges-vn.md` để user neo.
