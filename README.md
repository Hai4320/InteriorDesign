# Interior Design Skills — bộ skill Claude Code tự thiết kế nội thất

Bộ skill cho [Claude Code](https://claude.com/claude-code) giúp bạn **tự thiết kế một căn phòng hoặc cả căn nhà** theo quy trình của interior designer chuyên nghiệp: từ phỏng vấn nhu cầu, chốt concept, vẽ mặt bằng 2D, sinh prompt ảnh phối cảnh, đến lập dự toán mua sắm.

Toàn bộ giao tiếp và hồ sơ bằng **tiếng Việt**, đơn vị cm/m, giá tham khảo VND.

## Demo

Xem dự án mẫu hoàn chỉnh tại [`designs/phong-ngu-mau/`](designs/phong-ngu-mau/) — phòng ngủ 3.5×4m, ngân sách 50 triệu:

- Mở [`06-presentation.html`](designs/phong-ngu-mau/06-presentation.html) trong browser để xem **design board** tổng hợp (palette, layout, prompt render, dự toán)
- Mở [`03-layout.svg`](designs/phong-ngu-mau/03-layout.svg) để xem floor plan tỉ lệ 1px = 1cm

## Cài đặt

```bash
git clone git@github.com:Hai4320/InteriorDesign.git
cd InteriorDesign
claude
```

Skill nằm trong `.claude/skills/` nên Claude Code tự nhận khi mở project. Gõ `/interior` để bắt đầu.

## Pipeline 5 bước + 1 bước tuỳ chọn

| Bước | Lệnh | Việc | Output |
|---|---|---|---|
| — | `/interior` | Orchestrator: xem trạng thái, dẫn vào bước kế | — |
| 1 | `/interior-brief` | Phỏng vấn nhu cầu, hướng dẫn đo đạc phòng | `00-project.yaml`, `01-brief.md` |
| 2 | `/interior-concept` | Đề xuất 2–3 concept (phong cách, bảng màu, vật liệu), bạn chọn | `02-concept.md` |
| 3 | `/interior-layout` | Vẽ floor plan SVG đúng tỉ lệ + kiểm tra ergonomics tự động | `03-layout.svg`, `03-layout.md` |
| 4 | `/interior-render` | Sinh prompt ảnh phối cảnh cho Midjourney / DALL-E / SDXL | `04-render-prompts.md` |
| 5 | `/interior-budget` | Dự toán theo giá VN, shopping list, checklist mua–lắp–nghiệm thu | `05-du-toan.md` |
| 6 | `/interior-present` | (tuỳ chọn) Gộp tất cả thành design board HTML để xem/in/share | `06-presentation.html` |

Thứ tự bắt buộc: brief → concept → layout. Render và dự toán cần layout, làm trước sau tuỳ ý. Mỗi skill tự kiểm tra prerequisite — gọi sai thứ tự sẽ được chỉ về bước đúng.

Mỗi phòng là một thư mục `designs/<ten-phong>/`; thiết kế cả nhà = nhiều thư mục chạy chung pipeline.

## Có gì hay

- **Layout kiểm chứng bằng số**: SVG vẽ tỉ lệ 1px = 1cm từ số đo thật của phòng bạn; tự động kiểm tra ~20 rule ergonomics (lối đi ≥60cm, khoảng mở tủ, cự ly xem TV...) và in bảng pass/fail tính từ toạ độ thật.
- **Dự toán bám giá Việt Nam**: 3 phân khúc bình dân/trung/cao cấp, tự so với ngân sách, vượt thì đề xuất phương án cắt kèm con số.
- **Hồ sơ là file thật trong repo**: YAML + Markdown + SVG + HTML — diff được, sửa tay được, share được.

## Cấu trúc repo

```
.claude/skills/
  interior/               # orchestrator + reference data dùng chung
    references/
      ergonomics.md       # tiêu chuẩn khoảng cách bố trí
      styles.md           # 10 phong cách + palette + vật liệu
      furniture-sizes.md  # kích thước chuẩn đồ nội thất
      price-ranges-vn.md  # khoảng giá VND theo phân khúc
  interior-brief/         # bước 1
  interior-concept/       # bước 2
  interior-layout/        # bước 3
  interior-render/        # bước 4
  interior-budget/        # bước 5
  interior-present/       # bước 6 (tuỳ chọn)
designs/                  # mỗi phòng một thư mục hồ sơ
  phong-ngu-mau/          # dự án mẫu hoàn chỉnh
```

## Tuỳ biến

- Thêm phong cách: sửa `.claude/skills/interior/references/styles.md`
- Cập nhật giá theo khảo sát của bạn: sửa `price-ranges-vn.md` (giá trong repo là khoảng ước tính 2025–2026)
- Thêm/sửa rule ergonomics: sửa `ergonomics.md` — skill layout tự dùng bảng mã rule trong đó

## Lưu ý

- Giá trong dự toán là **khoảng tham khảo**, luôn kiểm tra giá thực tế trước khi mua.
- Ảnh sinh từ prompt render là **minh hoạ cảm giác**, không phải bản vẽ kỹ thuật.
- Bộ skill thay được phần lớn việc tự mày mò, nhưng công trình đụng kết cấu/điện nước nên có người có chuyên môn kiểm tra.
