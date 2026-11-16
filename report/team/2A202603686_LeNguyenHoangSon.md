# Báo cáo cá nhân — MSSV_HoTen

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Lê Nguyễn Hoàng Sơn
- MSSV: 2A202603686
- Email: 26ai.sonlnh@vinuni.edu.vn
- GitHub: SonLNH19

## 2. Phần việc phụ trách

Phụ trách shape B — single agent, trong file `src/lab8/shapes/single.py`.

## 3. Đóng góp cụ thể

Commit chính (hash), test đã thêm hoặc sửa, quyết định kỹ thuật bạn đưa ra.

- Viết code phần B — single agent trong `src/lab8/shapes/single.py`.
- Dùng vòng ReAct tối đa 8 bước, giới hạn tool đọc và gọi host ghi refund sau vòng lặp.
- Truyền quote đầy đủ và `crash_at` vào `issue_refund`; để lỗi crash truyền ra ngoài.
- Bổ sung test kiểm tra lời gọi MockLLM được tính vào chi phí và không dùng số ngày trễ khách ghi sai để quyết định hoàn tiền.
- Commit chính: chưa tạo; bổ sung hash sau khi commit.

## 4. Bằng chứng

Link commit, tên test, run id hoặc trích đoạn report liên quan.

- Test single agent: **62 passed**.
- Test host trên repo nhóm: **55 passed**.
- Test bổ sung: `tests/test_single_agent_review.py::test_single_uses_mock_without_trusting_ticket`.

## 5. Công cụ AI đã dùng

Công cụ, dùng vào việc gì, và bạn đã tự kiểm tra kết quả thế nào (xem [RULES.md](../../RULES.md)).

Dùng Codex hỗ trợ rà soát, sửa code và bổ sung test. Tự chạy lại bộ test single agent, kết quả 62 passed.

## 6. Tự đánh giá

