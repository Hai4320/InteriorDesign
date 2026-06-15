# Render prompts — Phòng khách (`phong-khach`)

> Bước 4/6 · Visualization · concept **"Nắng sớm Bắc Âu"** (Scandinavian) + layout 🅐.
> ⚠️ **Disclaimer:** ảnh sinh ra là **minh hoạ cảm giác** (mood, màu, ánh sáng, vật liệu) — KHÔNG phải bản vẽ kỹ thuật. Tỉ lệ và vị trí chính xác lấy theo `03-layout.svg`, không theo ảnh.

---

## Scene Facts (bắt buộc xuất hiện ở mọi prompt)

- **Phòng:** Scandinavian living room, ~30m², trần cao 2.8m, cảm giác sáng – thoáng – nhẹ.
- **Ánh sáng:** cửa sổ lớn (200×150cm) ở **tường Đông** → trong khung hình tổng thể là **bên phải**; **nắng buổi sáng ấm** (room.sun = Đông), rèm **voan trắng** lọc nắng dịu. Cửa ra vào ở tường Tây (bên trái).
- **Đồ chính (6+ món, vị trí tương quan từ layout 🅐):**
  - Sofa vải 3 chỗ **tựa tường Nam (xa)**, quay mặt vào phòng, **đầu phải sát cửa sổ** — góc đọc đón nắng.
  - **Đèn sàn arc** cạnh đầu phải sofa, hắt xuống đọc sách.
  - **Bàn trà thấp** gỗ trước sofa, đặt trên thảm.
  - **Thảm len dệt** sáng định vùng lounge dưới sofa.
  - **Bàn đa dụng gỗ** (làm việc + ăn) ở **góc Đông-Bắc**, cửa sổ bên phải; 1 ghế gỗ thanh.
  - **Kệ sách gỗ sáng đứng sàn** tựa tường Bắc, gần lối vào.
  - **Cây xanh chậu lớn** cạnh cửa sổ; vài bình gốm nhấn xanh.
  - Tất cả **đồ rời, chân gỗ hở thoáng, để thấp** (nhà thuê, không khoan tường, nhìn xuyên gầm → rộng).
- **Palette (gọi tên + hex):**
  - Nền `#F5F2EC` **trắng kem** — tường, trần, rèm voan.
  - Phụ `#D9CFC1` **be** — vải bọc sofa, thảm, gối nền.
  - Phụ `#B0A695` **greige** — rèm dày, đệm ghế.
  - Nhấn `#4A6FA5` **xanh dusty blue** — gối tựa, tranh, bình gốm (chỉ ~10%).
  - Vật liệu `#C9A66B` **gỗ sồi sáng** — chân đồ, kệ, mặt bàn, khung.
- **Vật liệu:** gỗ sồi/tần bì sáng, vải linen mộc, len dệt, voan trắng.
- **Style:** Scandinavian, minimal, ấm, nhiều ánh sáng tự nhiên.

---

## Góc 1 — Tổng thể (từ cửa nhìn vào)

*VI: Đứng ở cửa (tường Tây) nhìn vào — thấy sofa be tựa tường xa, cửa sổ nắng sáng bên phải, thảm + bàn trà giữa, kệ sách gỗ bên trái, sàn gỗ sáng liền mạch.*

**Midjourney v6:**
```
interior photography of a bright Scandinavian living room, ~30m², view from the doorway looking in, light oak wood floor, cream white walls #F5F2EC, beige linen 3-seat sofa #D9CFC1 with slim light-oak legs against the far wall, low oak coffee table on a light woven wool rug, arc floor lamp beside the sofa, large window on the right with sheer white voile curtains and soft warm morning sunlight, freestanding light-oak bookshelf on the left near entrance, tall potted plant by the window, dusty blue #4A6FA5 accent cushions, airy minimal open layout, low furniture with open legs, wide angle 24mm, natural morning light, photorealistic, high detail --ar 4:3 --style raw --v 6
```

**DALL-E 3:**
```
A photorealistic interior photo of a bright, airy Scandinavian living room about 30 square meters, seen from the doorway looking inward. The floor is light oak; walls and ceiling are warm cream white. Against the far wall sits a beige linen three-seat sofa with slim light-oak legs, facing into the room. In front of it is a low oak coffee table resting on a light woven wool rug. To the right is a large window with sheer white voile curtains, letting in soft warm morning sunlight that fills the room. An arc floor lamp leans over the right end of the sofa. On the left near the entrance stands a freestanding light-oak bookshelf. A tall potted plant sits by the window, and a few dusty-blue cushions and ceramic vases add gentle color accents. The furniture is low with open legs so the floor reads continuous and the space feels spacious. Calm, minimal, full of natural morning light.
```

**SDXL (tag-style):**
```
Scandinavian living room, view from doorway, light oak floor, cream white walls, beige linen 3-seat sofa, slim oak legs, low oak coffee table, light woven wool rug, arc floor lamp, large window on right, sheer white voile curtains, warm morning sunlight, freestanding oak bookshelf left, potted plant by window, dusty blue accent cushions, minimal, airy, low furniture open legs, wide angle 24mm, photorealistic, high detail
Negative prompt: blurry, distorted walls, warped furniture, extra windows, extra doors, lowres, watermark, text, people
```

---

## Góc 2 — Hero: góc đọc đón nắng (sofa + cửa sổ + đèn arc)

*VI: Cận cụm sofa đầu phải sát cửa sổ Đông, đèn sàn arc cong xuống, nắng sáng xiên qua voan, gối xanh dusty blue, cây xanh — đây là "nhân vật chính" của phòng.*

**Midjourney v6:**
```
interior photography, cozy reading nook in a Scandinavian living room, beige linen sofa #D9CFC1 with light-oak legs, right end of the sofa next to a large window with sheer white voile curtains, warm morning sunlight streaming through, arc floor lamp curving over the seat, dusty blue #4A6FA5 throw cushions, light-oak side surfaces #C9A66B, tall green potted plant by the window, light woven wool rug, cream white walls, calm minimal mood, wide angle 24mm, golden morning light, photorealistic, high detail --ar 4:3 --style raw --v 6
```

**DALL-E 3:**
```
A photorealistic close view of a cozy reading nook in a bright Scandinavian living room. The right end of a beige linen sofa with light-oak legs sits beside a large window dressed in sheer white voile curtains; warm morning sunlight streams through and lights the scene. An arc floor lamp curves gracefully over the seat. Dusty-blue throw cushions add a soft pop of color against the neutral fabric. A tall green potted plant stands by the window, and a light woven wool rug lies underfoot. Walls are warm cream white, wood tones are light oak. The mood is calm, minimal, and full of gentle golden morning light.
```

**SDXL (tag-style):**
```
cozy reading nook, Scandinavian living room, beige linen sofa, light oak legs, right end by large window, sheer white voile curtains, warm morning sunlight, arc floor lamp over seat, dusty blue throw cushions, light oak surfaces, tall potted plant, woven wool rug, cream white walls, minimal calm, wide angle 24mm, golden hour, photorealistic, high detail
Negative prompt: blurry, distorted walls, warped furniture, extra windows, extra doors, lowres, watermark, text, people
```

---

## Góc 3 — Chi tiết vật liệu (close-up texture)

*VI: Cận cảnh chất liệu — vải linen sofa, chân gỗ sồi sáng, thảm len dệt, gối linen xanh dusty blue. Khoe texture, không cần thấy cả phòng.*

**Midjourney v6:**
```
extreme close-up material detail, Scandinavian interior textures, natural beige linen upholstery #D9CFC1 weave, light oak wood leg #C9A66B grain, hand-woven wool rug #D9CFC1 texture, dusty blue #4A6FA5 linen cushion, soft warm morning side light raking across surfaces, shallow depth of field, tactile cozy minimal, macro photography, photorealistic, high detail --ar 4:3 --style raw --v 6
```

**DALL-E 3:**
```
A photorealistic extreme close-up of Scandinavian interior materials: the natural weave of beige linen sofa upholstery, the visible grain of a light-oak wooden leg, a hand-woven light wool rug, and a dusty-blue linen cushion resting against them. Soft warm morning light rakes across the surfaces, emphasizing texture. Shallow depth of field, tactile and cozy, minimal palette of cream, beige, light oak and a touch of dusty blue.
```

**SDXL (tag-style):**
```
close-up material detail, beige linen upholstery weave, light oak wood grain leg, hand-woven wool rug texture, dusty blue linen cushion, warm morning side light, shallow depth of field, tactile cozy minimal, macro, photorealistic, high detail
Negative prompt: blurry, distorted walls, warped furniture, extra windows, extra doors, lowres, watermark, text, people
```

---

## Góc 4 — Góc làm việc (bàn đa dụng góc Đông-Bắc)

*VI: Góc làm việc/ăn — bàn gỗ ở góc Đông-Bắc, cửa sổ E bên phải đón nắng sáng, ghế gỗ thanh, kệ sách gần đó, sạch gọn.*

**Midjourney v6:**
```
interior photography, work and dining corner in a Scandinavian living room, light-oak multipurpose table #C9A66B in the corner, large window on the right with sheer voile curtains and warm morning sunlight, slim light-oak chair, freestanding light-oak bookshelf nearby, cream white walls #F5F2EC, a laptop and a ceramic vase with dusty blue #4A6FA5 accent, minimal tidy desk, light wood floor, wide angle 24mm, bright natural morning light, photorealistic, high detail --ar 4:3 --style raw --v 6
```

**DALL-E 3:**
```
A photorealistic photo of a tidy work-and-dining corner in a bright Scandinavian living room. A light-oak multipurpose table sits in the corner with a large window to its right; sheer voile curtains diffuse warm morning sunlight across the desk. A slim light-oak chair is tucked in, and a freestanding light-oak bookshelf stands nearby. Walls are warm cream white, the floor is light wood. A laptop and a dusty-blue ceramic vase add a small accent of color. The mood is calm, minimal, bright and productive.
```

**SDXL (tag-style):**
```
work and dining corner, Scandinavian living room, light oak multipurpose table in corner, large window right, sheer voile curtains, warm morning sunlight, slim oak chair, freestanding oak bookshelf, cream white walls, laptop, dusty blue ceramic vase, minimal tidy, light wood floor, wide angle 24mm, bright natural light, photorealistic, high detail
Negative prompt: blurry, distorted walls, warped furniture, extra windows, extra doors, lowres, watermark, text, people
```

---

## Cách dùng

- **Dán prompt vào:** Midjourney (Discord/web), DALL-E 3 (ChatGPT/Bing), SDXL (Automatic1111, ComfyUI, Leonardo…). Mỗi góc đã có sẵn 3 biến thể đúng cú pháp từng nền.
- **Iterate đúng cách:** mỗi lần **chỉ đổi 1 thứ** rồi so sánh —
  - muốn **ấm hơn**: thêm `golden warm tone`, hạ về sáng sớm; muốn **mát/tỉnh hơn**: `neutral 3500K, midday light`.
  - giữ **scene facts cố định**, chỉ chỉnh phần ánh sáng/màu.
  - lặp **cùng seed** (Midjourney `--seed`, SDXL fix seed) để so sánh công bằng giữa các lần.
- **Bám hồ sơ:** nếu ảnh lệch (thừa cửa, đồ cao chắn cửa sổ, sai màu) → đó là ảo giác của model, lấy `03-layout.svg` + palette concept làm chuẩn, không sửa thiết kế theo ảnh.
