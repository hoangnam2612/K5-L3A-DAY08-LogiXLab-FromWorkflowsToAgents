# Báo cáo cá nhân — Phạm Văn Nam

## 1. Thông tin thành viên

- Họ tên: Phạm Văn Nam
- MSSV: 2A202603681
- Email: [nampham2662@gmail.com](mailto:nampham2662@gmail.com) (
- GitHub:NamPham1012 

## 2. Phần việc phụ trách

Triển khai shape A `workflow` trong `src/lab8/shapes/workflow.py`. Đây là quy trình Python cố định để xử lý claim hoàn phí vận chuyển; model không quyết định số tiền hoặc ghi refund.

## 3. Đóng góp cụ thể

- Commit code: `d69e54f` (`workflow`). Commit này chỉ thay đổi `src/lab8/shapes/workflow.py`.
- Đọc claim qua `get_claim_view`, kiểm tra `order_id` và quyền xem đơn qua `lookup_order`; thiếu mã đơn thì trả `needs_info`, không xem được đơn thì trả `escalated`.
- Tính quote bằng `compute_compensation` từ dữ liệu đơn, không lấy số ngày trễ trong ticket. Quote bằng 0 trả `denied`; quote dương được chuyển nguyên số tiền cho `durability.issue_refund` để host kiểm approval, trần theo đơn và idempotency.
- Truyền `crash_at` vào host, để `InjectedCrash` tiếp tục nổi lên cho kịch bản crash/resume. Đóng kết nối SQLite trong `finally`.
- Tạo `RunResult` và trace qua `finish`; trace ghi quyết định, trạng thái nhìn thấy đơn và quote, không ghi nguyên claim/order hoặc thông tin riêng tư.
- Test đã thêm hoặc sửa: **chưa có trong commit `d69e54f`**. Cần bổ sung ít nhất một test có ý nghĩa trước khi chốt bài nhóm theo `SUBMISSION.md`.

## 4. Bằng chứng

- Commit: `d69e54f` trên nhánh `PHAMVANNAM`.
- Từ thư mục `src/`, lệnh `python -m pytest -q -m student -o addopts= -k workflow` cho kết quả **62 passed, 240 deselected**. Bộ này gồm các claim public, gọi lại cùng claim (T11) và crash/resume (T12).
- Lệnh `python -m pytest -q` cho kết quả **54 passed, 248 deselected** (cổng host). `python -m lab8.smoke` in `lab8.smoke pass`.
- Môi trường lần kiểm tra trên máy: Windows AMD64, Python 3.14.7. Tài liệu lab ghi Python 3.11–3.13; cần chạy lại trên phiên bản được hỗ trợ trước khi chốt nếu có thể.
- Run id và benchmark của cả nhóm: bổ sung từ `src/reports/benchmark.json` sau khi các shape còn lại hoàn thành.

## 5. Công cụ AI đã dùng

Đã dùng ChatGPT/Codex để audit yêu cầu lab và hỗ trợ soạn báo cáo cá nhân. Kết quả code được tự kiểm bằng smoke, 62 test workflow và cổng host nêu ở mục 4; số liệu trong báo cáo lấy từ kết quả lệnh đã chạy, không tự tạo.

## 6. Tự đánh giá

Đã triển khai workflow và qua toàn bộ test public riêng của shape này. Chưa thêm hoặc sửa test trong commit code và chưa có kết quả hidden; cần hoàn thành các bước đó cùng nhóm trước khi nộp.