# Báo cáo cá nhân — Phạm Thanh Tùng

## 1. Thông tin thành viên

- Họ tên: Phạm Thanh Tùng
- MSSV: 2A202603695
- Email: thanhtung23032003@gmail.com
- GitHub: tunggthanhh

## 2. Phần việc phụ trách

Triển khai phần CP3 của shape C `orchestrator` trong `src/lab8/shapes/orchestrator.py`: tạo handoff cho investigator, giới hạn investigator ở các tool chỉ đọc, và bảo đảm luồng refund xử lý đúng khi crash.

## 3. Đóng góp cụ thể

- Commit chính: `6c2bf8d` — `Implement orchestrator investigation and crash refund`.
- Tạo handoff qua `make_handoff` với facts rỗng và các tool chỉ đọc `lookup_order`, `lookup_policy`, `compute_compensation`; không chuyển claim thô, header hay secret sang investigator.
- Ghi handoff đã sanitize vào trace bằng `safe_dump`, sau đó gọi `run_readonly_investigators` với `principal_id` của claim.
- Gọi `issue_refund` ở host với full quote và tham số `crash_at`. Nếu `InjectedCrash` xảy ra, trace được flush và exception được ném lại để crash suite kiểm tra cơ chế resume/idempotency.
- Kiểm tra riêng shape orchestrator bằng `python -m pytest -q -m student -o addopts= -k orchestrator`, kết quả 62 passed.

## 4. Bằng chứng

- Commit: `6c2bf8d` trên nhánh `PhamThanhTung-03695`.
- File thay đổi: `src/lab8/shapes/orchestrator.py`.
- Test public orchestrator: 62 passed, 240 deselected.
- Crash suite của nhóm: `src/reports/crash.json`, `crash_safety` = 20/20.

## 5. Công cụ AI đã dùng

Đã dùng Codex để đọc contract, đối chiếu implementation với shape tham chiếu, và kiểm tra test. Kết quả được xác nhận lại bằng pytest và crash suite; không dùng AI để thay thế kiểm thử.

## 6. Tự đánh giá

Phần CP3 bảo đảm investigator không có quyền ghi và host là thành phần duy nhất gọi refund. Điều cần bổ sung trước khi nộp là liên kết một test do cá nhân thêm hoặc sửa vào bảng đóng góp trong `TEAM.md`, theo yêu cầu submission.
