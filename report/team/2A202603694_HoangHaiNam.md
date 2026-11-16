# Báo cáo cá nhân — 2A202603694_HoangHaiNam

## 1. Thông tin thành viên

- Họ tên: Hoàng Hải Nam
- MSSV: 2A202603694
- Email: hoangnam26122003@gmail.com
- GitHub: hoangnam2612

## 2. Phần việc phụ trách

Shape C `orchestrator` ở giai đoạn CP2, trong `src/lab8/shapes/orchestrator.py`: dựng khung `run_claim` và luồng xử lý chính của orchestrator.

## 3. Đóng góp cụ thể

- Commit code: `9c379e7` (nhánh `HoangHaiNam-03694`, được ghép vào `main` qua pull request #1, commit `1591f90`). Commit này chỉ thay đổi `src/lab8/shapes/orchestrator.py`.
- Thay stub `not_implemented` bằng `run_claim` giữ nguyên chữ ký của đề, mở kết nối SQLite và đóng trong `finally`.
- Viết `_run` với các nhánh trả `RunResult` qua `finish`, mỗi nhánh ghi trace trước khi return:
  - `claim_id` không tồn tại: `failed`, `proposal_amount` 0;
  - thiếu `order_id`: `needs_info`, không ghi ledger;
  - investigator không thấy đơn hoặc principal không sở hữu đơn: `escalated`;
  - quote bằng 0: `denied`, không gọi `issue_refund`;
  - quote dương: gọi host với quote đầy đủ; host từ chối thì `denied`, xung đột số tiền thì `failed`, thành công thì `resolved`. `proposal_amount` luôn là quote đầy đủ.
- Tách hai hàm `_investigate` và `_call_host_refund` làm điểm nối cho CP3, để Tùng thay phần handoff và `crash_at` mà không phải đụng vào `_run`. Ở commit của mình, `_investigate` còn là chỗ giữ (`NotImplementedError("CP3")`) và `_call_host_refund` chưa truyền `crash_at`; hai chỗ này được Tùng hoàn thiện sau đó.
- Trace của orchestrator chỉ ghi các sự kiện `investigator` (đơn có nhìn thấy không, lý do, số policy), `quote`, `decision` và `refund_outcome` (`ok`, `reason`, `conflict`). Không ghi claim row, order row, `parent_secret`, header hay thông tin cá nhân.
- Commit `a2628b8` của mình chỉ thêm thư mục `.idea/` của IDE vào repo do nhầm; đây không phải phần việc của bài và nên xóa khỏi git.
- Thêm `src/tests/test_orchestrator_handoff_crash.py` (6 case): trace chứa đúng một handoff chỉ có tool đọc, không có `parent_secret`, `raw_headers`, `history`, và các file `<run_id>*` không chứa `CANARY_SECRET_` hay `Bearer`; C-002 (ticket ghi 5 ngày, order ghi 2 ngày) cho `denied` với quote 0; crash ở ba điểm (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`) rồi resume vẫn một dòng ledger và một audit `refund_committed`; gọi lại cùng claim không tạo refund thứ hai. Commit chứa file test: điền hash sau khi commit.

## 4. Bằng chứng

- Commit: `9c379e7`, pull request #1 (`1591f90`).
- Chạy trên nhánh `main` hiện tại, từ thư mục `src/`:
  - `python -m pytest -q -m student -o addopts= -k orchestrator`: **62 passed, 245 deselected**.
  - `python -m pytest -q`: **64 passed, 249 deselected** (cổng host, gồm 6 case test mới).
  - `python -m pytest -q tests/test_orchestrator_handoff_crash.py`: **6 passed**. Thử bỏ `crash_at=crash_at` khỏi lời gọi `issue_refund` thì 3 test crash fail; đã khôi phục code sau khi thử.
- Benchmark của cả nhóm (`src/reports/benchmark.json`): orchestrator pass 70/70 trial, cost/success 46.43 VND mô phỏng, trung bình 3.71 bước. Cao hơn workflow (27.86 VND); xem lý do chọn shape ở `report/team/decision_adr.md`.
- Các số trên là của orchestrator sau khi ghép CP2 và CP3, không riêng phần của mình.
- Môi trường chạy kiểm tra: Windows, Python 3.14.4. Tài liệu lab ghi Python 3.11–3.13.

## 5. Công cụ AI đã dùng

Hỗ trợ cho việc coding và phân tích yêu cầu bài toán giúp hiểu vấn đề và triển khai nhanh hơn.

## 6. Tự đánh giá

Đã dựng được khung xử lý của orchestrator và các nhánh trạng thái đúng contract; sau khi ghép CP3, shape qua toàn bộ 62 test student. Đã thêm bộ test cho orchestrator, kiểm handoff sạch và crash/resume qua `orchestrator.run_claim`, và test bắt được lỗi khi bỏ `crash_at`.
