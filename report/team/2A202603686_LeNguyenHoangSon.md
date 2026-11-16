# Báo cáo cá nhân — Lê Nguyễn Hoàng Sơn

## 1. Thông tin thành viên

- Họ tên: Lê Nguyễn Hoàng Sơn
- MSSV: 2A202603686
- Email: 26ai.sonlnh@vinuni.edu.vn
- GitHub: SonLNH19

## 2. Phần việc phụ trách

Phụ trách viết và kiểm thử phần B — single agent trong `src/lab8/shapes/single.py`.

## 3. Đóng góp cụ thể

- Viết `run_claim` để đọc claim, tra đơn hàng, tính số tiền hoàn và trả kết quả theo từng trường hợp.
- Dùng `run_react` với giới hạn 8 bước. Mỗi lượt đưa thông tin vừa đọc vào lời gọi MockLLM; đầu ra của MockLLM được dùng để chọn trong các tool đọc hợp lệ.
- Chỉ gọi `issue_refund` sau vòng ReAct, truyền quote đầy đủ và `crash_at` để host kiểm approval, trần hoàn tiền và chống ghi trùng.
- Viết test kiểm tra claim không bị xử lý theo số ngày trễ khách tự khai, trace không lộ secret, và kết quả MockLLM có ảnh hưởng đến thứ tự chọn tool đọc.
- Commit đã có: `881f9cc` (`Implement single agent claim handling`)..

## 4. Bằng chứng

- Đã chạy bộ test public cho single agent: **62 passed**.
- Đã chạy bộ test host sau lần chỉnh sửa gần nhất: **58 passed**.
- Test bổ sung nằm trong `src/tests/test_single_agent_review.py`.

## 5. Công cụ AI đã dùng

Dùng Codex để hỗ trợ rà soát code, chỉnh vòng ReAct và bổ sung test. Đã chạy lại test single agent; kết quả là 62 passed.

## 6. Tự đánh giá

Phần single agent đã xử lý đúng các tình huống trong bộ test public và giữ việc ghi tiền ở host. MockLLM của lab chỉ trả digest, nên cách chọn tool hiện tại là mô phỏng có thể lặp lại theo seed; chưa đánh giá được khả năng chọn tool của một model thật. Cần tiếp tục kiểm tra khi ghép với các phần còn lại của nhóm.
