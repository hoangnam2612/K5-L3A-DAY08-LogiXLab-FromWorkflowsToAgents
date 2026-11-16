# Báo cáo nhóm — Lab 8 LogiX-VN

Số liệu dưới đây đọc từ `src/reports/benchmark.json`, `src/reports/crash.json` và `src/reports/research_ablation.json` do công cụ lab sinh ra. Mọi lệnh chạy từ `src/`.

## 1. Thông tin nhóm

- Tên nhóm: LogiXLab (theo tên repo; nhóm xác nhận tên chính thức trong `TEAM.md`)
- Thành viên: xem `TEAM.md`
- Commit chốt cho code và bằng chứng: `431c4dc` (trùng `report/team/decision_adr.md`)

## 2. Mục tiêu và cách tiếp cận

Task là xử lý claim hoàn phí vận chuyển trên cùng world và chính sách bằng bốn kiến trúc A–D. Mục tiêu là chọn kiến trúc ít tự chủ nhất mà vẫn đạt độ đúng và an toàn. Nhóm triển khai A `workflow`, B `single` và C `orchestrator`; D `swarm` là đối chứng có sẵn. Host giữ quyền kiểm approval, trần theo đơn và idempotency, nên shape chỉ đưa quote đầy đủ, không ghi thẳng ledger. Thành viên phụ trách và commit nằm trong `TEAM.md` và các báo cáo cá nhân.

## 3. Giải pháp

- **Workflow:** đọc claim qua `get_claim_view`, kiểm `order_id` và quyền sở hữu đơn qua `lookup_order`, rồi tính quote từ dòng order bằng `compute_compensation`. Số ngày ghi trong ticket không quyết định tiền. Quote bằng 0 trả `denied`; quote dương chuyển nguyên cho `issue_refund`. Code kiểm soát số tiền và nhánh xử lý; không cần model để ghi tiền.
- **Single agent:** dùng `run_react` tối đa 8 bước để chọn các tool đọc hợp lệ, dùng MockLLM seeded cho lượt quyết định. Sau vòng đọc, code của shape lấy quote từ dữ liệu đơn và gọi host. Model không có quyền gọi tool ghi hoặc tự ấn định tiền hoàn.
- **Orchestrator:** tạo handoff bằng `make_handoff`, giới hạn `facts` và `allowed_tools` theo allowlist; investigator chỉ tra cứu đơn, policy và tính quote. Orchestrator nhận kết quả rồi gọi host; investigator không có tool ghi. Handoff đã sanitize mới được ghi trace.

Các shape dùng `finish` để trả `RunResult` và ghi trace JSON. Trace chỉ ghi quyết định, trạng thái nhìn thấy đơn, quote và kết quả host cần thiết; không dump claim/order thô, `parent_secret`, header, SĐT, địa chỉ, ghi chú nội bộ hay tên hàng. `crash_at` được chuyển cho host và `InjectedCrash` được ném tiếp để kiểm resume. T11/T12 trong ma trận student kiểm idempotency và crash theo shape.

## 4. Kết quả

Benchmark cùng 14 claim × 5 seed (70 trial/shape), world, giá mô phỏng và evaluator:

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Steps mean/p95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Workflow | 1.000 | 1.000 | 1.000–1.000 | 0 | 27.86 | 1.86 / 2 |
| Single | 1.000 | 1.000 | 1.000–1.000 | 0 | 36.32 | 5.17 / 6 |
| Orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0 | 46.43 | 3.71 / 4 |
| Swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 |

Swarm sai đúng một trial `R-swarm-C-002-s55`: `resolved` thay vì `denied` vì ticket khai trễ 5 ngày còn order ghi 2 ngày. Crash suite đạt **20/20**; ma trận student đạt **249/249** và cổng host đạt **58/58** tại thời điểm chạy. Bộ hidden chưa có nhãn để báo pass rate chính thức. ADR chọn workflow vì cùng pass public với B/C nhưng chi phí mô phỏng thấp hơn. Chi tiết quyết định: `report/team/decision_adr.md`.

Ablation R2 giữ nguyên claim, seed, MockLLM, tool registry, giá và evaluator, chỉ vô hiệu hóa việc swarm lấy ngày trễ từ ticket. Kết quả chuyển từ 69/70 lên 70/70, pass^5 từ 13/14 lên 14/14, cost/success từ 49.57 xuống 48.72 VND mô phỏng. File `src/reports/research_ablation.json` và lệnh tái lập nằm trong `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Workflow ban đầu truyền `crash_at` thay cho `seed` vào `make_run_id`, khiến nhiều lần chạy có hậu tố `sNone` và có thể ghi đè trace. Test `src/tests/test_workflow_run_id.py` bắt lỗi này; sau sửa, test và ma trận workflow xanh. Swarm cố ý tin ticket ở seed 55; nhóm giữ nguyên shape tham chiếu và kiểm bằng ablation thay vì sửa đối chứng. Trong lần rà soát orchestrator, nhóm thêm `import sqlite3` cho type annotation; test orchestrator vẫn xanh.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp, commit và test của từng người nằm trong bảng `TEAM.md` và file riêng `report/team/MSSV_HoTen.md`. Nhóm cần xác nhận đủ danh sách thành viên trước khi nộp.

## 7. Hạn chế và hướng cải thiện

MockLLM và chi phí mô phỏng không đại diện cho vận hành thực; latency là `unavailable`. Public chỉ có 14 claim, hidden 40 claim chưa được chấm ở đây. Bốn shape không gọi model/tool với số lần giống nhau, nên chênh chi phí không quy riêng cho topology. Nhóm sẽ đổi quyết định nếu hidden cho thấy workflow kém chính xác hoặc kém an toàn hơn một shape khác với mức tăng chi phí chấp nhận được.

## 8. Tài liệu tham khảo

- [Luật nghiệp vụ LogiX-VN](../../docs/business_rules.md), [contract kết quả và trace](../../docs/contracts.md), [cách đo metric](../../docs/metrics.md).
- Cemri và cộng sự, [*Why Do Multi-Agent LLM Systems Fail?*](https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html), NeurIPS 2025. Nhóm chỉ dùng taxonomy MAST để diễn giải lỗi LogiX, không coi kết quả paper là số đo của lab.
