# Báo cáo cá nhân — Lê Nguyễn Hoàng Sơn

## 1. Thông tin thành viên

- Họ tên: Lê Nguyễn Hoàng Sơn
- MSSV: 2A202603686
- Email: 26ai.sonlnh@vinuni.edu.vn / hoangson199205@gmail.com
- GitHub: SonLNH19

## 2. Phần việc phụ trách

Triển khai shape B `single` trong `src/lab8/shapes/single.py` và viết test cho phần này. Shape dùng vòng ReAct để chọn các tool đọc; code gọi host ghi refund sau khi đã có quote.

## 3. Đóng góp cụ thể

- Commit code chính: `881f9cc` (`Implement single agent claim handling`) và `fc0cea7` (`Refine single agent read tool selection and report`).
- Đọc claim bằng `get_claim_view`. Thiếu mã đơn trả `needs_info`; không xem được đơn trả `escalated`. Số tiền được tính từ dữ liệu đơn bằng `compute_compensation`, không lấy số ngày trễ khách ghi trong ticket.
- Dùng `run_react` với giới hạn 8 bước và `worker=True` để chỉ gọi tool đọc. Mỗi lượt, `decide` nhận kết quả đọc gần nhất, đưa thông tin cần thiết vào MockLLM rồi dùng đầu ra của nó chọn một tool trong danh sách hợp lệ.
- Sau vòng ReAct, truyền quote đầy đủ và `crash_at` cho `durability.issue_refund`. Host kiểm approval, trần hoàn tiền và idempotency; `InjectedCrash` được truyền ra ngoài để kiểm tra crash/resume.
- Tạo `RunResult` và trace qua `finish`. Trace ghi hành động và kết quả cần kiểm tra, không ghi nguyên ticket hay claim.
- Thêm `src/tests/test_single_agent_review.py` để kiểm tra ticket khai sai số ngày trễ, đầu ra MockLLM ảnh hưởng đến tool đọc đầu tiên và prompt ở lượt sau có kết quả tra đơn.

## 4. Bằng chứng

- Commit code trên nhánh `2A202603686_LeNguyenHoangSon`: `881f9cc` và `fc0cea7`.
- Từ thư mục `src/`, lệnh `python -m pytest -q -m student -o addopts= -k "single and not workflow and not orchestrator and not swarm"` cho kết quả **62 passed, 244 deselected**. Bộ này gồm claim public, gọi lại cùng claim (T11) và crash/resume (T12).
- Lệnh `python -m pytest -q` cho kết quả **58 passed, 248 deselected**. Chạy riêng `tests/test_single_agent_review.py` cho kết quả **4 passed**.
- Chưa có kết quả hidden cho shape B; cần đối chiếu thêm khi nhóm chạy benchmark và chốt kiến trúc.

## 5. Công cụ AI đã dùng

Đã dùng Codex để rà soát yêu cầu, hỗ trợ chỉnh vòng ReAct, bổ sung test và soạn báo cáo. Kết quả được kiểm bằng các lệnh pytest ở mục 4; số liệu ghi theo kết quả chạy thực tế.

## 6. Tự đánh giá

Phần single agent đã qua toàn bộ test public riêng của shape và test bổ sung. MockLLM của lab chỉ trả digest, nên lựa chọn tool hiện là mô phỏng theo seed và kết quả quan sát, chưa phản ánh khả năng suy luận chọn tool của model thật. Nhóm cần kiểm tiếp trên benchmark và bộ hidden trước khi kết luận về kiến trúc.
