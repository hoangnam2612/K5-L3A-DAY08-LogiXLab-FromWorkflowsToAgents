# Báo cáo cá nhân — Phạm Văn Nam

## 1. Thông tin thành viên

- Họ tên: Phạm Văn Nam
- MSSV: 2A202603681
- Email: [nampham2662@gmail.com](mailto:nampham2662@gmail.com)
- GitHub: NamPham1012

## 2. Phần việc phụ trách

Triển khai shape A `workflow` trong `src/lab8/shapes/workflow.py`. Đây là quy trình Python cố định để xử lý claim hoàn phí vận chuyển; model không quyết định số tiền hoặc ghi refund.

## 3. Đóng góp cụ thể

- Commit code: `d69e54f` (`workflow`). Commit này chỉ thay đổi `src/lab8/shapes/workflow.py`.
- Đọc claim qua `get_claim_view`, kiểm tra `order_id` và quyền xem đơn qua `lookup_order`; thiếu mã đơn thì trả `needs_info`, không xem được đơn thì trả `escalated`.
- Tính quote bằng `compute_compensation` từ dữ liệu đơn, không lấy số ngày trễ trong ticket. Quote bằng 0 trả `denied`; quote dương được chuyển nguyên số tiền cho `durability.issue_refund` để host kiểm approval, trần theo đơn và idempotency.
- Truyền `crash_at` vào host, để `InjectedCrash` tiếp tục nổi lên cho kịch bản crash/resume. Đóng kết nối SQLite trong `finally`.
- Tạo `RunResult` và trace qua `finish`; trace ghi quyết định, trạng thái nhìn thấy đơn và quote, không ghi nguyên claim/order hoặc thông tin riêng tư.
- Thêm `src/tests/test_workflow_run_id.py`: kiểm `run_id` và tên/nội dung trace phải khớp `seed`, đồng thời hai seed không dùng chung file trace. Test phát hiện workflow truyền nhầm `crash_at` vào `make_run_id`, làm cả seed 11 và 22 có hậu tố `sNone`; đã sửa thành truyền `seed`.

## 4. Bằng chứng

- Commit: `d69e54f` trên nhánh `PHAMVANNAM`.
- Từ thư mục `src/`, lệnh `python -m pytest -q -m student -o addopts= -k workflow` cho kết quả **63 passed, 240 deselected**. Bộ này gồm các claim public, gọi lại cùng claim (T11), crash/resume (T12) và test `run_id` mới.
- Test mới ban đầu fail với `R-workflow-C-002-sNone` thay vì `R-workflow-C-002-s11`; sau khi sửa, test pass.
- Lệnh `python -m pytest -q` cho kết quả **54 passed, 249 deselected** (cổng host). `python -m lab8.smoke` trước đó in `lab8.smoke pass`.
- Môi trường lần kiểm tra trên máy: Windows AMD64, Python 3.14.7. Tài liệu lab ghi Python 3.11–3.13; cần chạy lại trên phiên bản được hỗ trợ trước khi chốt nếu có thể.
- Run id và benchmark của cả nhóm: bổ sung từ `src/reports/benchmark.json` sau khi các shape còn lại hoàn thành.

## 5. Công cụ AI đã dùng

Đã dùng ChatGPT/Codex để đối chiếu yêu cầu lab, hỗ trợ soạn báo cáo và viết test bổ sung cho `run_id`. Kết quả được kiểm bằng smoke, 63 test workflow và cổng host nêu ở mục 4; số liệu trong báo cáo lấy từ kết quả lệnh đã chạy, không tự tạo.

## 6. Tự đánh giá

Đã triển khai workflow, thêm một test bắt được lỗi gắn sai `seed` vào `run_id`, và qua toàn bộ test public riêng của shape này. Chưa có kết quả hidden; nhóm cần kiểm tiếp trước khi nộp.
