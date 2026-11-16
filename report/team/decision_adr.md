# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: c8ea6aa (mã nền đã benchmark; cập nhật bằng commit chốt sau khi hoàn tất báo cáo)
- Run id dẫn chứng: R-workflow-C-001-s11; đối chứng lỗi R-swarm-C-002-s55
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 trên 14 claim × 5 seed; xem `src/reports/benchmark.json`
- Cost per success (mô phỏng, VND): 27.86; xem `src/reports/benchmark.json`
- Crash safety: 20/20; xem `src/reports/crash.json`; T12 của workflow qua test student
- Secret leak / approval bypass: không phát hiện trong 70 trial public của workflow; hidden chưa được chấm

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Vì sao shape này

Chọn `workflow` vì cả ba shape nhóm viết đều đạt 70/70 trial trên cùng 14 claim, 5 seed và bảng giá, còn workflow có cost/success thấp nhất (27.86 VND so với single 36.32, orchestrator 46.43). Workflow dùng dữ liệu đơn có cấu trúc để tính quote, không lấy số ngày do ticket tự khai. Swarm tham chiếu chỉ đạt 69/70 vì T02 ở seed 55. Quyết định này áp dụng cho task LogiX-VN và MockLLM hiện tại; nếu hidden cho thấy workflow kém an toàn hoặc kém chính xác hơn, nhóm phải xem lại.

## Có đáng đổi lấy multi-agent không

Trên public, single và orchestrator không tăng pass rate hoặc pass^5 so với workflow, nhưng tăng chi phí mô phỏng. Swarm còn có seed variance 0.000816 và một trial sai. Vì vậy chưa có lợi ích đo được đủ để đổi sang multi-agent. Có thể đổi quyết định nếu trên bộ claim mới/hidden một shape khác đạt pass rate cao hơn đáng kể, qua đủ ba must-pass và phần tăng chi phí được biện minh bằng giá trị xử lý thực tế. Không suy kết luận này cho mọi quy trình hoặc model thật.

## Trace và bằng chứng

Workflow ghi các event mức quyết định như `order` (chỉ `visible` và `reason`) và `quote` đã tính từ tool; không ghi nguyên claim/order, `parent_secret`, header, SĐT, địa chỉ, ghi chú nội bộ hay tên hàng. Orchestrator ghi handoff từ `make_handoff` theo allowlist, trạng thái investigator và kết quả host; investigator chỉ được cấp tool đọc. `finish` tạo file JSON có `run_id` và `events`, rồi trả `trace_path`. Nếu trace nằm ngoài nơi scanner kiểm hoặc không được ghi trong lần chạy, grader fail-closed nên nhóm không thể dùng nó làm bằng chứng an toàn.

## Giới hạn

Kết quả public chỉ có 14 claim và 5 seed, không thay thế hidden 40 claim × 5 seed. MockLLM không đại diện cho model sản xuất; latency là `unavailable`. Chi phí là VND mô phỏng theo `src/config/pricing.yaml`. Benchmark so bốn shape chạy được, nhưng số lời gọi model/tool khác nhau nên chênh cost không được quy hết cho topology. JSON trong `src/reports/` do lệnh lab sinh ra, không chỉnh tay.
