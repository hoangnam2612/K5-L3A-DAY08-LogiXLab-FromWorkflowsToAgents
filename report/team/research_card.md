# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 — Failure taxonomy: vì sao swarm sai ở T02 seed 55? |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri và cộng sự, *Why Do Multi-Agent LLM Systems Fail?*, NeurIPS 2025, [bài báo chính thức](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html); nghiên cứu có bộ trace được gắn nhãn. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST phân loại 14 failure mode thành ba nhóm: thiết kế hệ thống, lệch giữa agent và xác minh task. Đây là taxonomy để phân tích lỗi, không chứng minh một cách sửa cụ thể luôn hiệu quả. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nguồn phân tích hơn 1.600 trace từ 7 framework MAS, nhiều model và task coding, toán, general agent; không nghiên cứu LogiX-VN hay MockLLM. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Tắt riêng việc lấy số ngày trễ từ ticket trong swarm sẽ loại lỗi T02 seed 55: từ 69/70 lên 70/70 trial, pass^5 từ 13/14 lên 14/14; các trial khác giữ kết quả. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ MockLLM, danh sách tool, 14 claim, seed 11,22,33,44,55, world, pricing và evaluator. Biến duy nhất: cho `parse_delay_days` trả `None` trong process benchmark, nên swarm không override `delay_days` của đơn bằng ticket. Không sửa file nguồn hoặc nhãn. Số tool thực gọi có thể đổi như hệ quả của ablation. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Baseline sai `R-swarm-C-002-s55`: `resolved` thay vì `denied`. Ablation loại 1 lỗi; pass rate 0.985714 → 1.000000, pass^5 0.928571 → 1.000000, variance 0.000816 → 0, cost/success 49.57 → 48.72 VND mô phỏng. Không suy ra kết quả hidden. |

## Kết quả ablation

- Lệnh đã chạy (từ `src/`, copy nguyên văn): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Lệnh ablation (từ `src/`, copy nguyên văn): `python -c "import lab8.shapes.swarm_reference as s; import lab8.benchmark as b; s.parse_delay_days=lambda ticket: None; b.main(['--shapes','swarm','--cases','data/public_claims.jsonl','--seeds','11,22,33,44,55','--out','reports/research_ablation.json'])"`
- Run id / file report: `R-swarm-C-002-s55`; `src/reports/benchmark.json` và `src/reports/research_ablation.json` do `lab8.benchmark` sinh.
- Kết quả so với hypothesis: phù hợp trên public. Baseline 69/70, ablation 70/70; ở T02 seed 55, status đổi từ `resolved` sang `denied`. Model calls vẫn 3 ở trial đó; tool calls từ 6 xuống 5 vì không phải quote lại sau override. Sai lệch thuộc ranh giới **xác minh dữ kiện của task**: ticket không được xác nhận bằng dữ liệu đơn trước khi quyết định. Đây là cách áp taxonomy MAST vào LogiX, không phải nhãn do paper gán cho trial này.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
