# Schema & quy ước chung — nguồn sự thật duy nhất

> File này là **nguồn sự thật duy nhất** cho cấu trúc `00-project.yaml` và mọi quy ước hình học/đơn vị/màu dùng xuyên suốt bộ skill `interior`. Các SKILL.md chỉ được **trỏ tới file này**, không định nghĩa lại quy ước trong văn xuôi của chúng. Khi sửa quy ước, sửa ở đây — không sửa rải rác.
>
> Template điền sẵn (có placeholder): `../assets/project.yaml`. File này mô tả *luật*; assets cho *khung điền*.

## 0. Đơn vị & quy ước nền

- **Độ dài**: luôn `cm` (số nguyên). Không trộn mm/m.
- **Tiền**: triệu VND, trường hậu tố `_trieu` (vd `total_trieu: 50`). Khoảng giá ghi dạng `min–max` triệu.
- **Màu**: hex 6 ký tự hoa, có dấu `#` (vd `#EAE3D9`). Không dùng tên màu CSS, không 3 ký tự.
- **Ngày**: `YYYY-MM-DD`.
- Trường user không biết: ghi `null` + 1 note giải thích. **Không bịa số.**

## 1. Hệ toạ độ bản vẽ *(quy ước gốc — layout & render & present đều theo)*

- Nhìn từ trên xuống. Gốc `(0,0)` = **góc trên-trái lòng phòng**. Trục **x sang phải**, **y xuống dưới**. Tỉ lệ vẽ **1px = 1cm**.
- 4 tường đặt tên **N / E / S / W**: `N` = cạnh trên bản vẽ, `S` = dưới, `W` = trái, `E` = phải.
- ⚠️ **N/E/S/W chỉ là tên toạ độ vẽ, KHÔNG phải hướng la bàn.** Hướng nắng thật ghi riêng ở `room.sun`.
- `width_cm` = cạnh ngang (tường N/S); `depth_cm` = cạnh dọc (tường E/W).

### offset_cm (cho cửa & cửa sổ)
Luôn đo theo **chiều tăng của trục toạ độ trên tường đó**:
- Tường **N / S** (ngang): đo theo trục **x**, từ góc trái (x nhỏ) sang phải.
- Tường **E / W** (dọc): đo theo trục **y**, từ góc trên (y nhỏ) xuống dưới.

### swing (chiều mở cửa) — enum: `in-left | in-right | out-left | out-right`
- `in / out` = mở **vào trong phòng** / ra ngoài.
- `left / right` = phía **bản lề**, định nghĩa theo offset:
  - **`left`** = bản lề ở **đầu offset NHỎ** (đầu gần góc gốc của tường).
  - **`right`** = bản lề ở **đầu offset LỚN** (đầu xa góc gốc).
- Cung quét cửa trong SVG **xoay quanh điểm bản lề**. Ví dụ chuẩn: cửa tường S, `offset_cm: 20`, `width_cm: 80`, `swing: in-right` → bản lề ở đầu offset lớn `(100, 400)`, cánh quét vào trong phòng: `<path d="M 100 400 A 80 80 0 0 0 20 320">`.

## 2. Bảng màu concept (`concept.palette`) — quy ước 60-30-10

Đúng **5 mã hex**, gán vai trò rõ ràng:

| Khoá | Vai trò | Tỉ lệ | Số lượng |
|---|---|---|---|
| `nen` | màu nền (tường/sàn/đồ lớn) | 60% | 1 hex |
| `phu` | màu phụ | 30% | **2 hex** (mảng `[..,..]`) |
| `nhan` | màu nhấn (decor, điểm nhít) | 10% | 1 hex |
| `vatlieu` | màu vật liệu chủ đạo | — | 1 hex |

Hex trong `concept.palette` của yaml là **bản tóm tắt**; bản chi tiết (kèm mô tả dùng ở đâu) nằm trong `02-concept.md`. **Hai nơi phải khớp từng ký tự.** Khi lệch: artifact chi tiết (`02-concept.md`) là chuẩn, sửa yaml theo — và báo user.

## 3. Cấu trúc `00-project.yaml`

`R` = bắt buộc, `O` = tuỳ chọn. Skill ghi trường nào đánh dấu ở cột "ghi bởi".

```
project:                 R
  slug          R  str   kebab không dấu, == tên thư mục designs/<slug>/
  type          R  enum  phong-khach | phong-ngu | bep-an | phong-tam | khac
  created       R  date  YYYY-MM-DD
status:                  R  — mỗi bước cập nhật khi xong; enum: pending | done | stale
  brief         R  enum  (stale: done nhưng nguồn phía trên đã đổi — xem propagate)
  concept       R  enum
  layout        R  enum
  render        R  enum
  dutoan        R  enum
  present       R  enum
room:                    R
  width_cm      R  int   cạnh ngang (tường N/S)
  depth_cm      R  int   cạnh dọc (tường E/W)
  height_cm     R  int   cao trần
  doors:        R  list  mỗi cửa:
    - wall        R  enum   N | E | S | W
      offset_cm   R  int    đo theo §1
      width_cm    R  int
      swing       R  enum   in-left | in-right | out-left | out-right (§1)
  windows:      O  list  mỗi cửa sổ:
    - wall        R  enum   N | E | S | W
      offset_cm   R  int
      width_cm    R  int
      height_cm   R  int
      sill_cm     R  int    cao bệ so với sàn
  sun           O  enum  hướng LA BÀN thật: bac|nam|dong|tay|dong-bac|dong-nam|tay-bac|tay-nam
  notes         O  list  ghi chú hiện trạng (tường ẩm, hộp kỹ thuật...)
budget:                  R
  total_trieu   R  int   triệu VND
  scope         R  enum  do-roi | do-roi-va-hoan-thien
  timeline      O  str
users           R  str   chân dung người dùng (ai, mấy người, thói quen)
pain_points     O  list  điểm khó chịu của phòng hiện tại
style_hints:             O
  like          O  list  tên style (đối chiếu references/styles.md)
  dislike       O  list
  colors_like   O  list
  colors_dislike O list
keep_items      O  list  đồ giữ lại: {name: str, w: int, d: int}  (w,d = cm)
constraints     O  list  ràng buộc (nhà thuê, không khoan tường, phong thuỷ...)
accepted_tradeoffs O list  ngoại lệ user CHỦ ĐÍCH chấp nhận (vd "PN-03 lối đi 55cm — giữ bàn làm việc").
                         Gate/script không báo lại các mã đã ghi ở đây. Mỗi mục: {ma|mo_ta, ly_do}.
concept:        O  obj | null   interior-concept ghi sau khi chốt:
  name          R  str
  parti         R  str   1 CÂU ý tưởng tổ chức chủ đạo — xem §6
  style         R  str   tên style
  palette       R  obj   {nen: hex, phu: [hex,hex], nhan: hex, vatlieu: hex}  (§2)
  materials     R  list  3–4 vật liệu chủ đạo
  key_items     R  list  5–7 món
```

## 4. Artifact của pipeline (trong `designs/<slug>/`)

| File | Bước ghi | Phụ thuộc |
|---|---|---|
| `00-project.yaml` | brief (concept/status cập nhật bởi bước sau) | — |
| `01-brief.md` | brief | — |
| `02-concept.md` | concept | brief |
| `03-layout-A.svg` / `-B.svg` / `03-layout.svg` / `03-layout.md` | layout | brief (+ concept) |
| `04-render-prompts.md` | render | concept (+ layout) |
| `05-du-toan.md` | budget | layout |
| `06-presentation.html` | present | brief + concept + layout |

## 5. Nhóm màu fill đồ trong SVG layout

Mỗi nhóm một fill nhạt nhất quán giữa các phương án: **ngủ** / **lưu trữ** / **ngồi** / **decor**. Thảm & lớp mềm vẽ nét đứt, đặt trước (layer dưới) các món khối.

## 6. Tầng ý đồ: parti & rationale *(yêu cầu "như KTS thực thụ")*

Để output có ý đồ nghề chứ không chỉ "xếp đồ vừa phòng":

- **`parti`** = **một câu** ý tưởng tổ chức chủ đạo mà mọi quyết định phải phục vụ. Bắt buộc ở **concept** (`concept.parti` trong yaml + nêu trong `02-concept.md`) và ở **layout** (nêu đầu `03-layout.md`). Ví dụ: *"Phòng tổ chức quanh trục ánh sáng cửa sổ — vùng ngủ ở phía tối, bàn làm việc đón sáng tự nhiên."* Không phải lặp tên style.
- **`rationale`** = decision log: mỗi quyết định lớn (bố trí, chọn vật liệu, cắt ngân sách) ghi `quyết định → phục vụ nhu cầu/site/chuẩn nào`. Viết trong artifact của bước (`02/03/05`), để review ③ và user truy vết được "vì sao". Một KTS thực thụ luôn defended được mọi lựa chọn.
- **Grounding**: concept/layout phải dẫn chiếu chuẩn nghề trong `design-principles.md` (tỉ lệ, ánh sáng, lưu trữ) + precedent điển hình, thay vì khẳng định cảm tính.

## 7. Bất biến phải đúng xuyên artifact *(script ② kiểm)*

1. Mọi hex trong `02-concept.md` == `concept.palette` trong yaml (từng ký tự).
2. Danh sách đồ trong `05-du-toan.md` (trừ `keep_items`) ⊆ danh sách đồ trong `03-layout.md`.
3. Tổng cộng dự toán = đúng tổng số học các dòng.
4. Mọi `rect` đồ khối trong SVG: không chồng nhau (thảm/lớp mềm ngoại lệ), không lọt ngoài phòng, không đè khe cửa/cung quét.
5. Tỉ lệ SVG 1px=1cm; kích thước phòng trong SVG == `room.width_cm`/`depth_cm`.
6. `status` chỉ nhận `pending | done | stale`.
