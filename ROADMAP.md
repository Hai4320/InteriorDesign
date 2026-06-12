# Kế hoạch cải thiện chất lượng output — bộ skill `interior`

> Tổng hợp từ nghiên cứu [awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) và [claude-code-game-studios](https://github.com/donchitos/claude-code-game-studios), đối chiếu với các lỗi thật phát hiện khi test bộ skill (15 + 8 finding qua 2 vòng dry-run, lỗi hex lệch giữa artifacts...).
>
> Trạng thái: **kế hoạch — chưa triển khai**. Ngày lập: 2026-06-12.

## Nguyên tắc chung

- Vấn đề gốc: pipeline 6 bước phụ thuộc dây chuyền, dữ liệu truyền qua file tự do → lỗi lệch schema, lệch số liệu giữa artifact, model ẩu khi tính toạ độ.
- Hướng giải: chuyển từ "dặn dò trong SKILL.md" sang **cơ chế cứng** (schema, script, hook) ở những chỗ sai là hỏng dây chuyền; giữ linh hoạt ở phần sáng tạo (concept, render).
- Không bê về: phân cấp đa agent, team commands, sprint/release — quy mô studio, overkill cho pipeline cá nhân.

## Nguyên tắc xuyên suốt: Human-in-the-loop *(ưu tiên cao nhất)*

Mọi cơ chế trong plan này **kiểm và báo — không tự quyết**. Đây là thiết kế nội thất cho nhà của chính user; mọi quyết định có tính thẩm mỹ, ngân sách, hay sửa-dây-chuyền đều thuộc về user:

1. **Gate/script/hook fail → trình finding + 2-3 lựa chọn xử lý kèm trade-off, user chọn.** Không bao giờ tự sửa ngầm artifact rồi báo sau. Ngoại lệ duy nhất được tự sửa không cần hỏi: lỗi cú pháp thuần (YAML gãy, SVG không parse được) — và vẫn phải báo đã sửa gì.
2. **Checkpoint quyết định bắt buộc của pipeline giữ nguyên và được bảo vệ**: chọn concept, chọn phương án layout, duyệt danh sách đồ trước khi vẽ, duyệt phương án cắt dự toán. Không cơ chế tự động nào được nhảy qua các điểm này.
3. **Trade-off do user quyết**: rule ergonomics FAIL nhưng user muốn giữ (vd lối đi 55cm để giữ bàn làm việc) → ghi nhận thành ngoại lệ có chủ đích trong `00-project.yaml` (`accepted_tradeoffs`), các lần kiểm sau không báo lại — phân biệt "lỗi" với "lựa chọn".
4. **Hook cảnh báo, không chặn cứng** (warn-not-block): in finding để user thấy, không exit lỗi làm gãy thao tác user đang làm.
5. Collaborative protocol chuẩn (hỏi theo nhóm → đưa phương án có trade-off → user quyết → ghi file → xác nhận) viết thành luật trong CLAUDE.md (⑤) và mọi skill mới (③④⑥) phải theo.

## Lộ trình 6 giai đoạn

### ① Schema + tách templates *(nền móng — làm trước tiên)*

Pattern: `structured-output`, `specs/DESIGN.md`, progressive disclosure (Agent Skills spec).

| Việc | Chi tiết |
|---|---|
| Tạo `​.claude/skills/interior/references/schema.md` | Spec chính thức cho `00-project.yaml`: từng trường — kiểu, bắt buộc/optional, giá trị hợp lệ, quy ước (toạ độ, offset theo chiều tăng trục, swing left/right = phía bản lề, hex 6 ký tự...). Đây là nguồn sự thật duy nhất; SKILL.md chỉ trỏ tới. |
| Tạo `​.claude/skills/interior/templates/` | Tách khỏi body SKILL.md: `project.yaml` (template có placeholder `<...>`), `layout.svg` (khung mẫu), format chuẩn cho `01-brief.md`, `05-du-toan.md`, `06-presentation.html` (skeleton). |
| Gọn các SKILL.md | Body chỉ còn: prerequisite, quy trình, nguyên tắc; template/schema trỏ file. Mục tiêu mỗi SKILL.md ≤ 60 dòng. |
| Mỗi skill validate input theo schema trước khi chạy | Thêm 1 dòng bắt buộc vào mục Prerequisite của từng skill. |
| Đối chiếu spec chính thức | So format SKILL.md với [anthropics/skills](https://github.com/anthropics/skills) (spec + template chính thức) và [agentskills/agentskills](https://github.com/agentskills/agentskills) (progressive disclosure) — chỉnh frontmatter/cấu trúc cho chuẩn để sau cài được cross-agent và public được. |

Acceptance: lỗi kiểu "hex trong yaml lệch với 02-concept.md" bị chặn tại bước ghi; SKILL.md không còn chứa template dài; format khớp spec chính thức.

### ② Kiểm tra tất định: script + hooks *(giá trị cao nhất)*

Pattern: `verification-gates`, hooks path-scoped exit-early (game-studios).

| Việc | Chi tiết |
|---|---|
| `​.claude/skills/interior/scripts/check_layout.py` | Parse `00-project.yaml` + SVG: kiểm overlap đồ khối, lọt ngoài phòng, đè khe cửa/vùng quét cửa, đúng tỉ lệ 1px=1cm, đồng thời tính bảng ergonomics từ toạ độ thật (đọc rule từ `ergonomics.md`). Output bảng pass/fail. `interior-layout` bắt buộc chạy script này thay vì "tính tay". |
| `​.claude/skills/interior/scripts/check_project.py` | Validate `00-project.yaml` theo schema ①; kiểm chéo số liệu giữa artifacts (hex palette, danh sách đồ layout vs dự toán, tổng cộng dự toán đúng số học). |
| Hook `PostToolUse` (Write/Edit vào `designs/**`) | Tự chạy `check_project.py` trên file vừa ghi; exit 0 ngay nếu path không thuộc `designs/`. Cấu hình trong `.claude/settings.json`. |
| Quality gate cuối mỗi skill | Mỗi SKILL.md thêm mục "Gate trước khi set done": chạy script liên quan + checklist riêng (render: mọi scene fact có trong từng prompt; budget: cộng lại tổng 2 lần). Gate fail → trình finding + lựa chọn cho user (sửa theo đề xuất / user tự chỉnh / chấp nhận thành `accepted_tradeoffs`); `status: done` chỉ khi pass hoặc user chấp nhận có chủ đích. |

Acceptance: layout sai hình học không lọt qua gate mà user không biết; sửa tay file trong `designs/` cũng được hook báo; ngoại lệ user đã chấp nhận không bị báo lại.

### ③ Skill `interior-review` — LLM judge có mức độ

Pattern: `agentic-evaluators`, review modes (game-studios).

| Việc | Chi tiết |
|---|---|
| Skill mới `interior-review` | Chấm chéo toàn hồ sơ theo rubric: (a) nhất quán xuyên artifact — palette/đồ/số liệu khớp nhau giữa yaml/concept/layout/render/budget; (b) độ khớp brief — từng nhu cầu, ràng buộc, pain point của user có được giải quyết, ở đâu; (c) chất lượng từng artifact theo checklist riêng. Output: điểm + bảng finding `file | vấn đề | mức độ | đề xuất`. **Chỉ báo cáo — user duyệt từng finding (sửa/bỏ qua/chấp nhận) rồi mới được sửa file.** |
| 3 modes | `full` — toàn rubric; `lean` — chỉ (a) nhất quán số liệu (mặc định); `solo` — chỉ chạy script ②, không judge. |
| Vị trí trong pipeline | Tuỳ chọn, gợi ý chạy trước `interior-present`; orchestrator thêm vào bảng trạng thái. |

Acceptance: chạy `full` trên `phong-ngu-mau` phải bắt lại được loại lỗi từng gặp (hex lệch, mâu thuẫn quy ước).

### ④ Skill `interior-propagate` — lan truyền thay đổi

Pattern: `propagate-design-change` (game-studios).

| Việc | Chi tiết |
|---|---|
| Skill mới `interior-propagate` | Khi user đổi một quyết định đã chốt (đổi concept, dời tường, đổi ngân sách): xác định artifact hạ nguồn bị ảnh hưởng theo đồ thị phụ thuộc brief → concept → layout → render/budget → present, **trình bảng diff dự kiến từng file, user duyệt từng artifact (hoặc duyệt cả lô) trước khi cập nhật**; cập nhật bằng cách gọi lại flow của skill tương ứng, không làm lại từ đầu. Điểm chọn lại concept/layout nếu bị ảnh hưởng vẫn dừng hỏi user như pipeline gốc. |
| Ghi `status` dạng stale | Thêm trạng thái `stale` (ngoài `pending/done`) — artifact done nhưng nguồn phía trên đã đổi. Orchestrator hiển thị ⚠️. |

Acceptance: đổi palette trong concept → render prompts và presentation tự được đánh `stale` và cập nhật được bằng một lệnh.

### ⑤ CLAUDE.md — quy ước chung cấp repo

Pattern: chuẩn `AGENTS.md`, collaborative protocol (game-studios).

| Việc | Chi tiết |
|---|---|
| Tạo `CLAUDE.md` ở root | Gom quy ước đang lặp rải rác trong 7 SKILL.md: ngôn ngữ tiếng Việt, đơn vị cm/VND, hệ toạ độ + quy ước bản lề (trỏ `schema.md`), cấu trúc workspace `designs/<slug>/`, collaborative protocol chuẩn (hỏi theo nhóm → đưa 2-3 phương án có trade-off → user quyết → ghi file → xác nhận). |
| Dọn trùng lặp | Các SKILL.md xoá phần quy ước đã có trong CLAUDE.md, chỉ giữ phần đặc thù của bước. |

Acceptance: một quy ước chỉ tồn tại ở một chỗ; agent mở repo không cần đọc skill vẫn nắm luật.

### ⑥ Meta-test: golden sample regression

Pattern: `regression-protection`, `/skill-test` (game-studios).

| Việc | Chi tiết |
|---|---|
| `docs/TESTING.md` + skill `interior-test` (hoặc mục trong orchestrator) | `designs/phong-ngu-mau/` là golden fixture. Sau khi sửa bất kỳ SKILL.md/reference/script: chạy lại pipeline trên brief mẫu (câu trả lời giả lập cố định ghi trong TESTING.md), so output mới với golden — script ② pass, số liệu chính khớp, review ③ mode lean không ra finding mới. |
| Hook nhắc | `PostToolUse` khi Write/Edit vào `.claude/skills/**` → in nhắc "đã sửa skill — chạy interior-test trước khi dùng". |

Acceptance: sửa skill gây hỏng pipeline bị phát hiện trước khi user thật dùng phải.

### ⑦ Public bộ skill *(sau khi ①+② xong, tuỳ chọn)*

Bối cảnh: rà toàn bộ awesome-agent-harness — chưa có skill pack nào cho domain đời sống phi lập trình (mọi skill pack hiện có đều phục vụ vòng đời code). Niche trống → project có giá trị public.

| Việc | Chi tiết |
|---|---|
| Chuẩn hoá đóng gói | Đảm bảo cài được qua [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI (cross-agent: Claude Code, Codex, Cursor...) — phụ thuộc việc khớp spec ở ①. |
| README song ngữ | Thêm bản tóm tắt tiếng Anh vào README (đối tượng quốc tế tìm qua awesome list). |
| Submit PR vào awesome lists | [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) và [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills). |

Acceptance: người lạ clone repo (hoặc cài qua CLI) chạy được pipeline không cần hỏi.

## Repo tham khảo khi triển khai

- Cấu trúc skill stack nhiều bước: [gstack](https://github.com/garrytan/gstack), [compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
- Quality gates trong skill pack: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Artifacts file-based làm trạng thái pipeline: [planning-with-files](https://github.com/OthmanAdi/planning-with-files)
- Meta-factory sinh domain skills + validation: [revfactory/harness](https://github.com/revfactory/harness)
- Skill pack chính chủ cho domain hẹp (mẫu tổ chức): [google/skills](https://github.com/google/skills), [huggingface/skills](https://github.com/huggingface/skills)

## Thứ tự & phụ thuộc

```
① schema/templates ──► ② scripts/hooks ──► ③ review ──► ⑥ meta-test
                                      └──► ④ propagate
⑤ CLAUDE.md — độc lập, làm cùng ① là tiện nhất
⑦ public — cần ① (spec) + ② (chất lượng), làm sau cùng
```

Ước lượng: ①+② một phiên làm việc; ③+⑤ một phiên; ④+⑥ một phiên; ⑦ nửa phiên.

## Nguồn tham khảo

- [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) — taxonomy pattern: structured-output, verification-gates, agentic-evaluators, regression-protection
- [donchitos/claude-code-game-studios](https://github.com/donchitos/claude-code-game-studios) — cơ chế: hooks path-scoped, document templates, review modes, propagate-design-change, skill-test
- [Anthropic Agent Skills](https://github.com/anthropics/skills) — spec chính thức, progressive disclosure
- [AGENTS.md](https://github.com/agentsmd/agents.md) — chuẩn instructions cấp repo
