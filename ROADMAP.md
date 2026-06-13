# Kế hoạch cải thiện chất lượng output — bộ skill `interior`

> Tổng hợp từ deep-research đa nguồn (22 nguồn, 108 claim, verify đối kháng) + các lỗi thật phát hiện khi test bộ skill (15 + 8 finding qua 2 vòng dry-run, lỗi hex lệch giữa artifacts, comment bản lề lệch hình...).
>
> Ngày lập gốc: 2026-06-12. **Cập nhật theo research: 2026-06-13.**
> Trạng thái triển khai: **①②③⑤ xong (2026-06-13)** — ① schema/design-principles/assets/parti + SKILL.md gọn; ② scripts + hook `PostToolUse` + quality gate; ③ skill `interior-review` (3 modes, rubric design-crit); ⑤ `CLAUDE.md` (human-in-the-loop + collaborative protocol). ④⑥⑦ chưa.

## Nguyên tắc chung

- Vấn đề gốc: pipeline 6 bước phụ thuộc dây chuyền, dữ liệu truyền qua file tự do → lỗi lệch schema, lệch số liệu giữa artifact, model ẩu khi tính toạ độ.
- Hướng giải: chuyển từ "dặn dò trong SKILL.md" sang **cơ chế cứng** (schema, script, hook) ở những chỗ sai là hỏng dây chuyền; giữ linh hoạt ở phần sáng tạo (concept, render).
- Không bê về **quy mô studio** (đa agent thường trực, phân cấp, team commands, sprint/release) — xem quyết định dưới.

### Quyết định: mượn *vai* studio, không lấy *quy mô* studio

Cân nhắc "biến thành studio nhóm KTS đa agent" → **không**, cho studio runtime đầy đủ. Lý do: sai bài toán (pipeline cho 1 căn nhà của 1 user, nút thắt là đúng-khéo-hợp-ý chứ không phải throughput); pipeline **đã chuyên môn hoá theo bước** (concept=designer, layout=space-planner, budget=QS); chi phí thật (chạm session limit 2 lần chỉ với 1 deep-research → đa agent mỗi lần thiết kế là quá đắt/chậm cho công cụ cá nhân); và đa agent tự tranh luận chốt nội bộ **làm loãng quyền quyết của user** (mâu thuẫn human-in-the-loop) + dễ mất coherence.

Nhưng **mượn 2 vai studio** giá trị nhất:
- **Critic/principal độc lập** — vai studio chính thức của bộ skill, hiện thực ở ③ `interior-review`.
- **Concept panel** — *chỉ ở bước concept* (không gian sáng tạo rộng): vài hướng đối lập → critic chấm → tổng hợp. Nâng nhẹ `interior-concept` đang "2-3 concept" thành mini judge-panel.

Nguyên tắc chọn đa agent: chỉ đáng khi (a) không gian giải pháp rộng cần khám phá song song (→ concept), hoặc (b) cần góc nhìn độc lập bắt lỗi (→ critic). Kiểm tất định → dùng **script** (rẻ, chắc hơn agent); thực thi tuyến tính có spec rõ → **1 agent/bước**. Studio *dev-time* (workflow fan-out như deep-research, sinh nội dung `design-principles.md`) là công cụ thỉnh thoảng gọi, không phải kiến trúc thường trực.

### 3 tầng kiểm soát đầu ra — *"như một KTS thực thụ"*

Một output ra dáng kiến trúc sư cần kiểm soát 3 tầng, không chỉ tầng đúng/sai:

| Tầng | Câu hỏi | Cơ chế | Phủ ở |
|---|---|---|---|
| **1. Đúng** (correctness) | Sai số liệu/hình học không? | Schema + script tất định | ①② |
| **2. Khéo** (craft) | Đúng chuẩn nghề không? (tỉ lệ, ánh sáng, lưu trữ) | Thư viện chuẩn `design-principles.md` + script kiểm tỉ lệ | ①② |
| **3. Có ý đồ** (intent) | Có một parti xuyên suốt + lý do truy vết được không? | Trường `parti` + `rationale` bắt buộc; rubric design-crit | ①③ |

Tầng 3 là cái phân biệt KTS với người xếp đồ. Gu thẩm mỹ không tất định hoá được → kiểm soát tầng 2–3 = **rubric nghề (chủ quan → nửa-khách-quan) + grounding (chống bịa) + human-in-the-loop (user quyết gu)**. Harness không thay con mắt KTS; nó **ép quy trình của KTS**: có ý đồ, có lý do, tự phê bình, đối chiếu chuẩn.

## Nguyên tắc xuyên suốt: Human-in-the-loop *(ưu tiên cao nhất)*

Mọi cơ chế trong plan này **kiểm và báo — không tự quyết**. Đây là thiết kế nội thất cho nhà của chính user; mọi quyết định có tính thẩm mỹ, ngân sách, hay sửa-dây-chuyền đều thuộc về user:

1. **Gate/script/hook fail → trình finding + 2-3 lựa chọn xử lý kèm trade-off, user chọn.** Không bao giờ tự sửa ngầm artifact rồi báo sau. Ngoại lệ duy nhất được tự sửa không cần hỏi: lỗi cú pháp thuần (YAML gãy, SVG không parse được) — và vẫn phải báo đã sửa gì.
2. **Checkpoint quyết định bắt buộc của pipeline giữ nguyên và được bảo vệ**: chọn concept, chọn phương án layout, duyệt danh sách đồ trước khi vẽ, duyệt phương án cắt dự toán. Không cơ chế tự động nào được nhảy qua các điểm này.
3. **Trade-off do user quyết**: rule ergonomics FAIL nhưng user muốn giữ (vd lối đi 55cm để giữ bàn làm việc) → ghi nhận thành ngoại lệ có chủ đích trong `00-project.yaml` (`accepted_tradeoffs`), các lần kiểm sau không báo lại — phân biệt "lỗi" với "lựa chọn".
4. **Hook cảnh báo, không chặn cứng** (warn-not-block): in finding để user thấy, không làm gãy thao tác. *(Research xác nhận `PostToolUse` vốn KHÔNG chặn được — fire sau khi tool đã chạy, chỉ feed stderr về Claude. Đây đúng là cơ chế ta muốn. Ta CHỦ ĐÍCH không dùng `PreToolUse`+exit 2 dù nó chặn được.)*
5. Collaborative protocol chuẩn (hỏi theo nhóm → đưa phương án có trade-off → user quyết → ghi file → xác nhận) viết thành luật trong CLAUDE.md (⑤) và mọi skill mới (③④⑥) phải theo.

---

## Kết quả đối chiếu nghiên cứu *(2026-06-13)*

Deep-research verify các repo trong plan + tìm thêm. Tóm tắt cái ảnh hưởng tới plan (chi tiết & trích dẫn: phần "Nguồn" cuối file):

| Phát hiện (đã verify đối kháng) | Tác động lên plan |
|---|---|
| **anthropics/skills** (spec chính thức): skill = thư mục có `SKILL.md` + `scripts/` + `references/` + **`assets/`** (templates/resources); frontmatter chỉ bắt buộc `name` ≤64 ký tự + `description` ≤1024. | **①**: template đặt ở `assets/` (đúng spec) thay vì `templates/` mình đề xuất ban đầu — lợi cho cross-agent ⑦. `schema.md` để ở `references/` (đúng spec cho doc). |
| **gstack** (active, 23 skill) + **compound-engineering-plugin**: đều là pipeline phụ thuộc dây chuyền, **file-based state**, artifact stage trên feed stage dưới (vd gstack `/office-hours` sinh design doc cho mọi bước sau). | **②④**: xác nhận mô hình "file làm pipeline state + propagate xuống hạ nguồn" của ta là pattern đã được kiểm chứng thật. Copy được cách họ chain. |
| **aaddrick/claude-pipeline** *(mới — chưa có trong plan cũ)*: chuỗi stage tuần tự `setup→plan→implement→test→review→pr`, shell orchestrator truyền state qua **file path + JSON output** (đã verify 3-0). *(Các claim "14 JSON schema" và "gate đa tầng" KHÔNG verify được — đừng coi là chắc.)* | Repo tham khảo cho ①②③ — mô hình chain + truyền state qua file đã xác nhận. Đọc kỹ trước khi code ②③, nhưng kiểm lại con số schema/gate bằng mắt. |
| **Hooks Claude Code** (đã verify 3-0): `PostToolUse` fire SAU khi tool xong → **không chặn được** (tool đã chạy), chỉ feed stderr về Claude. Muốn CHẶN phải `PreToolUse` + exit 2 (exit 1 = không chặn). Hook hỗ trợ cả **"prompt" hook kiểu LLM-judge** (đánh giá bằng ngôn ngữ tự nhiên). | **②**: `PostToolUse` *chính là* cơ chế warn-not-block ta muốn — nó vốn không chặn, chỉ báo. Ta cố tình KHÔNG dùng `PreToolUse`+exit 2. **③**: prompt-hook LLM-judge là lựa chọn native cho khâu chấm. |
| **Domain design phi-code KHÔNG còn trống**: "I built **63 design skills** for Claude" (marieclairedean); "7 Claude Code design skills follow a **real design process**" (julian.oczkowski). | **⑦**: luận điểm cũ "niche trống" **sai**. Đổi sang **khác biệt hoá** — đọc đối thủ trước, định vị điểm riêng (tiếng Việt, giá VN, pipeline đo-đạc→SVG tỉ lệ thật). |
| **agentskills.io** + **agentskills/agentskills**: spec open cross-vendor (Claude Code/Cursor/Codex/Copilot/Gemini/Goose/OpenCode). | **⑦**: chuẩn để cài cross-agent có thật; bám `name`+`description` tối thiểu là cài được nhiều nơi. |
| **planning-with-files**: pattern file-state thật, NHƯNG **không** có completion gate (claim đó bị bác 0-3). | Đừng kỳ vọng cơ chế gate ở repo này; gate phải tự xây ở ②. |

*Đã verify xong (2 vòng, 17 claim confirmed). Còn vài claim bị 0-0 do hết phiên ở vòng cuối (chi tiết agentskills.io, số schema của claude-pipeline) — không ảnh hưởng quyết định kiến trúc. Lưu ý: claim "progressive disclosure 3 tầng token" bị bác (0-3) → đừng trích con số token cụ thể như thể là spec.*

---

## Lộ trình 7 giai đoạn

### ① Schema + tách templates *(nền móng — đang làm)*

Pattern: `structured-output`, `specs/DESIGN.md`, progressive disclosure (Agent Skills spec).

| Việc | Trạng thái / Chi tiết |
|---|---|
| `​.claude/skills/interior/references/schema.md` | ✅ **Đã tạo.** Spec chính thức cho `00-project.yaml`: từng trường (kiểu, R/O, enum), quy ước toạ độ/offset/swing, palette 60-30-10, hex 6 ký tự, enum status (`pending\|done\|stale`), `accepted_tradeoffs`, bảng bất biến xuyên artifact. **+ trường tầng-ý-đồ: `parti` (1 câu ý tưởng tổ chức, bắt buộc cho concept & layout) và `rationale` (decision log truy vết).** Nguồn sự thật duy nhất; SKILL.md chỉ trỏ tới. |
| `​.claude/skills/interior/references/design-principles.md` *(mới — tầng "khéo")* | Chuẩn nghề để skill áp & **cite**, vượt khỏi clearance tối thiểu: tỉ lệ/proportion phòng, chiến lược ánh sáng tự nhiên (quan hệ giường/bàn với cửa sổ theo `room.sun`), phân tầng chiếu sáng nhân tạo (ambient/task/accent), tỉ lệ lưu trữ / người, tỉ lệ đồ-trên-sàn (≤~40-45%). Concept/layout phải dẫn chiếu nguyên tắc + precedent điển hình thay vì "vibes". |
| `​.claude/skills/interior/assets/` *(đổi từ `templates/` → `assets/` theo spec)* | `project.yaml` (template placeholder), `layout.svg` (khung mẫu — sửa luôn comment bản lề `in-left`→`in-right` cho khớp hình), skeleton `01-brief.md`, `05-budget.md`. (`06-presentation.html` skeleton: hạ ưu tiên — node cuối, ít rủi ro lệch.) |
| Gọn các SKILL.md | Body chỉ còn: prerequisite, quy trình, nguyên tắc; template/schema trỏ file. Mục tiêu mỗi SKILL.md ≤ 60 dòng (hiện brief 104, layout 90 vượt). |
| Mỗi skill validate input theo schema trước khi chạy | Thêm 1 dòng vào mục Prerequisite của từng skill: "validate `00-project.yaml` theo `schema.md`". |
| Frontmatter chuẩn spec | Đối chiếu [anthropics/skills](https://github.com/anthropics/skills): `name` ≤64 ký tự kebab == tên thư mục, `description` ≤1024. (Hiện đã gần đúng — rà lại.) |

Acceptance: lỗi kiểu "hex trong yaml lệch với 02-concept.md" bị chặn tại bước ghi; SKILL.md không còn chứa template dài; frontmatter khớp spec → cài cross-agent được.

### ② Kiểm tra tất định: script + hooks *(giá trị cao nhất)*

Pattern: `verification-gates`, hooks path-scoped exit-early. Tham khảo: **aaddrick/claude-pipeline** (14 JSON schema gate).

| Việc | Chi tiết |
|---|---|
| `​scripts/check_layout.py` | Parse `00-project.yaml` + SVG: overlap đồ khối, lọt ngoài phòng, đè khe cửa/cung quét, tỉ lệ 1px=1cm; tính bảng ergonomics từ toạ độ thật (đọc rule từ `ergonomics.md`). **+ tỉ lệ nghề (tầng "khéo"): tỉ lệ đồ-trên-sàn ≤~40-45%, lưu trữ/người, quan hệ đồ chính với hướng cửa sổ** (đọc `design-principles.md`). Output bảng pass/fail. `interior-layout` bắt buộc chạy thay vì "tính tay". |
| `​scripts/check_project.py` | Validate `00-project.yaml` theo `schema.md`; kiểm chéo bất biến §7 của schema (hex palette yaml vs `02-concept.md`, đồ layout vs dự toán, tổng dự toán đúng số học). Bỏ qua mã trong `accepted_tradeoffs`. |
| Hook `PostToolUse` (Write/Edit vào `designs/**`) | Tự chạy `check_project.py` trên file vừa ghi; exit sớm nếu path không thuộc `designs/`. `PostToolUse` bản chất không chặn (tool đã chạy) → in finding qua stderr về Claude = đúng warn-not-block. Cấu hình trong `.claude/settings.json`. |
| Quality gate cuối mỗi skill | Mỗi SKILL.md thêm "Gate trước khi set done": chạy script liên quan + checklist riêng. Gate fail → trình finding + lựa chọn (sửa theo đề xuất / user tự chỉnh / chấp nhận thành `accepted_tradeoffs`); `status: done` chỉ khi pass hoặc user chấp nhận có chủ đích. |

Acceptance: layout sai hình học không lọt qua gate mà user không biết; sửa tay file trong `designs/` cũng được hook báo; ngoại lệ user đã chấp nhận không bị báo lại.

### ③ Skill `interior-review` — LLM judge có mức độ *(vai "critic/principal" của studio)*

Pattern: `agentic-evaluators`, reviewer-agent đa tầng (claude-pipeline).

| Việc | Chi tiết |
|---|---|
| Skill mới `interior-review` — **rubric design-crit** | Đóng vai director phê bình như buổi crit KTS, không chỉ soi số liệu. Rubric: (a) nhất quán xuyên artifact; (b) độ khớp brief — từng nhu cầu/ràng buộc/pain point giải quyết ở đâu; (c) **parti có rõ & layout/concept/vật liệu có cùng kể một câu chuyện không**; (d) **circulation, hierarchy ánh sáng/màu, tỉ lệ** đối chiếu `design-principles.md`; (e) chất lượng từng artifact. Output: điểm + bảng finding `file \| vấn đề \| mức độ \| đề xuất`. **Chỉ báo cáo — user duyệt từng finding rồi mới sửa.** |
| (Tuỳ chọn) prompt-hook LLM-judge | Research xác nhận Claude Code hỗ trợ "prompt" hook đánh giá bằng ngôn ngữ tự nhiên — có thể dùng cho mode `lean` tự động cảnh báo nhất quán số liệu mà không cần viết script bóc tách phức tạp. Vẫn warn-not-block. |
| 3 modes | `full` — toàn rubric; `lean` — chỉ (a) nhất quán số liệu (mặc định); `solo` — chỉ chạy script ②, không judge. |
| Vị trí | Tuỳ chọn, gợi ý chạy trước `interior-present`; orchestrator thêm vào bảng trạng thái. |

Acceptance: chạy `full` trên `phong-ngu-mau` bắt lại được loại lỗi từng gặp (hex lệch, comment bản lề lệch hình).

### ④ Skill `interior-propagate` — lan truyền thay đổi

Pattern: `propagate-design-change`; file-state chain (gstack, compound-engineering — đã verify).

| Việc | Chi tiết |
|---|---|
| Skill mới `interior-propagate` | Khi user đổi quyết định đã chốt (đổi concept, dời tường, đổi ngân sách): xác định artifact hạ nguồn bị ảnh hưởng theo đồ thị phụ thuộc (§4 schema), **trình bảng diff dự kiến từng file, user duyệt từng artifact (hoặc cả lô) trước khi cập nhật**; cập nhật bằng cách gọi lại flow skill tương ứng. Checkpoint chọn lại concept/layout vẫn dừng hỏi. |
| `status: stale` | Đã thêm vào enum trong `schema.md` (artifact done nhưng nguồn phía trên đã đổi). Orchestrator hiển thị ⚠️. |

Acceptance: đổi palette trong concept → render prompts + presentation tự đánh `stale` và cập nhật được bằng một lệnh.

### ⑤ CLAUDE.md — quy ước chung cấp repo

Pattern: chuẩn `AGENTS.md`, collaborative protocol.

| Việc | Chi tiết |
|---|---|
| Tạo `CLAUDE.md` ở root | Gom quy ước chung: ngôn ngữ tiếng Việt, đơn vị cm/VND, **trỏ `schema.md`** cho hệ toạ độ + bản lề (không lặp lại nội dung), cấu trúc `designs/<slug>/`, collaborative protocol chuẩn. |
| Dọn trùng lặp | Các SKILL.md xoá quy ước đã có trong CLAUDE.md/schema.md, chỉ giữ phần đặc thù của bước. |

Acceptance: một quy ước chỉ tồn tại ở một chỗ; agent mở repo không cần đọc skill vẫn nắm luật.

### ⑥ Meta-test: golden sample regression

Pattern: `regression-protection`, `/skill-test`.

| Việc | Chi tiết |
|---|---|
| `docs/TESTING.md` + skill `interior-test` | `designs/phong-ngu-mau/` là golden fixture. Sau khi sửa SKILL.md/reference/script: chạy lại pipeline trên brief mẫu (câu trả lời giả lập cố định trong TESTING.md), so output mới với golden — script ② pass, số liệu chính khớp, review ③ mode lean không ra finding mới. |
| Hook nhắc | `PostToolUse` khi Write/Edit vào `.claude/skills/**` → in nhắc "đã sửa skill — chạy interior-test trước khi dùng". |

Acceptance: sửa skill gây hỏng pipeline bị phát hiện trước khi user thật dùng phải.

### ⑦ Publish bộ skill *(sau khi ①+② xong)*

**Mục tiêu: publish bộ skill thành sản phẩm cài được — KHÔNG phải submit awesome list.** Người lạ phải cài và chạy được pipeline mà không cần hỏi.

Bối cảnh: research cho thấy **đã có skill pack thiết kế** (marieclairedean 63 skills, julian 7 design skills) → không phải "first-mover", phải **khác biệt hoá**. Điểm riêng: tiếng Việt, khoảng giá thị trường VN, pipeline đi từ đo-đạc thật → SVG đúng tỉ lệ → kiểm ergonomics định lượng (đa số skill design khác dừng ở moodboard/style).

| Việc | Chi tiết |
|---|---|
| **Đọc đối thủ trước** | Đọc marieclairedean & julian.oczkowski xem họ tổ chức pipeline thế nào; chốt 2-3 điểm khác biệt làm luận điểm cho phần giới thiệu. |
| Khớp spec để cài được | Frontmatter + cấu trúc thư mục đúng [anthropics/skills](https://github.com/anthropics/skills) (phụ thuộc ①). Mỗi skill là 1 thư mục `SKILL.md` + `scripts/`/`references/`/`assets/` → cài được cross-agent (Claude Code, Cursor, Codex...). |
| Đóng gói cài đặt | Cung cấp đường cài: clone repo + script/instruction đặt skill vào đúng thư mục agent; (tuỳ chọn) cài qua [vercel-labs/skills](https://github.com/vercel-labs/skills) / [agentskills](https://github.com/agentskills/agentskills) CLI. Cân nhắc đóng dạng **Claude Code plugin** để cài 1 lệnh. |
| README hướng publish | Mô tả rõ: cài thế nào, chạy pipeline thế nào, điểm khác biệt. Bản tiếng Anh nếu nhắm người dùng quốc tế. Có ảnh/demo `06-presentation.html` mẫu. |
| Đăng ký nơi phân phối | Publish lên kênh để người dùng tìm & cài: registry skill (agentskills.io) và/hoặc Claude Code plugin marketplace. *(Awesome list chỉ là kênh discovery phụ — không phải mục tiêu; bỏ qua nếu không muốn.)* |

Acceptance: người lạ cài bộ skill theo README (clone/CLI/plugin) và chạy trọn pipeline trên phòng của họ mà không cần hỏi; phần giới thiệu nêu được điểm khác biệt so với skill pack design có sẵn.

## Thứ tự & phụ thuộc

```
① schema/templates ──► ② scripts/hooks ──► ③ review ──► ⑥ meta-test
                                      └──► ④ propagate
⑤ CLAUDE.md — độc lập, làm cùng ① là tiện nhất
⑦ publish — cần ① (spec) + ② (chất lượng), làm sau cùng
```

Ước lượng: ①+② một phiên; ③+⑤ một phiên; ④+⑥ một phiên; ⑦ nửa phiên.

## Repo tham khảo khi triển khai

- ⭐ **Pipeline chain truyền state qua file/JSON** (đọc trước khi code ②③): [aaddrick/claude-pipeline](https://github.com/aaddrick/claude-pipeline) — chuỗi `setup→plan→implement→test→review→pr` (đã verify). Con số "14 schema" + gate đa tầng chưa verify, kiểm lại bằng mắt.
- **Pipeline chain + file-state** (đã verify): [garrytan/gstack](https://github.com/garrytan/gstack), [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin)
- **Spec chính thức + cấu trúc thư mục** (đã verify): [anthropics/skills](https://github.com/anthropics/skills), [agentskills/agentskills](https://github.com/agentskills/agentskills)
- **Hooks** (đã verify): [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
- **Đối thủ domain design** (đọc cho ⑦): marieclairedean "63 design skills", julian.oczkowski "7 design skills"
- Artifacts file-based làm pipeline state: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) *(lưu ý: không có gate)*
- Cấu trúc skill stack nhiều bước / quality gates: [donchitos/claude-code-game-studios](https://github.com/donchitos/claude-code-game-studios), [addyosmani/agent-skills] *(đang chờ verify)*

## Nguồn tham khảo

- Deep-research nội bộ 2 vòng (22 nguồn, verify đối kháng, **17 claim confirmed**) — 2026-06-13.
- [Picrew/awesome-agent-harness](https://github.com/Picrew/awesome-agent-harness) — taxonomy: structured-output, verification-gates, agentic-evaluators, regression-protection
- [donchitos/claude-code-game-studios](https://github.com/donchitos/claude-code-game-studios) — hooks path-scoped, document templates, review modes, propagate-design-change, skill-test
- [Anthropic Agent Skills](https://github.com/anthropics/skills) + [agentskills.io](https://agentskills.io/home) — spec chính thức, progressive disclosure, cross-agent
- [AGENTS.md](https://github.com/agentsmd/agents.md) — chuẩn instructions cấp repo
