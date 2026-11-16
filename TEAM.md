# Team

## Thông tin nhóm

- Tên nhóm: LogiXLab (theo tên repo; nhóm xác nhận tên chính thức)
- Lớp: L3A
- Repo nhóm: [https://github.com/hoangnam2612/K5-L3A-DAY08-LogiXLab-FromWorkflowsToAgents](https://github.com/hoangnam2612/K5-L3A-DAY08-LogiXLab-FromWorkflowsToAgents)
- URL repo, nhánh nộp, commit chốt: URL ở trên; nhánh `main`; commit code và bằng chứng `431c4dc` (xem `report/team/decision_adr.md`).

## Thành viên

| STT | Họ tên       | MSSV        | Email                                                                | GitHub      | Vai trò  |
| ---: | ------------ | ----------- | -------------------------------------------------------------------- | ----------- | -------- |
| 1   | Phạm Văn Nam | 2A202603681 | [nampham2662@gmail.com](mailto:nampham2662@gmail.com) (email commit) | NamPham1012 | Workflow |
| 2   | Lê Nguyễn Hoàng Sơn | 2A202603686 | 26ai.sonlnh@vinuni.edu.vn | SonLNH19 | Single agent |
| 3   | Hoàng Hải Nam | 2A202603694 | hoangnam26122003@gmail.com (email commit) | hoangnam2612 | Orchestrator CP2 |
| 4   | Phạm Thanh Tùng | 2A202603695 | thanhtung23032003@gmail.com  | tunggthanhh | Orchestrator CP3 |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Phạm Văn Nam | Workflow | `d69e54f`, `dc55102` | Thêm `src/tests/test_workflow_run_id.py`; 63 test workflow pass |
| Lê Nguyễn Hoàng Sơn | Single agent | `881f9cc`, `fc0cea7` | Thêm/sửa `src/tests/test_single_agent_review.py`; 62 test student riêng của single pass |
| Hoàng Hải Nam | Orchestrator CP2 | `9c379e7` | Chưa thấy test do thành viên thêm/sửa trong lịch sử hiện có; cần bổ sung bằng chứng |
| Phạm Thanh Tùng | Orchestrator CP3 | `6c2bf8d` | Chưa có test cá nhân thêm/sửa; đã chạy bộ public orchestrator: 62 passed |

## Cá nhân

Mỗi thành viên bổ sung mục của mình và báo cáo riêng trong `report/team/`.

### 2A202603681_PhamVanNam

#### Phần việc phụ trách

- Shape A `workflow` — `src/lab8/shapes/workflow.py`.

#### Đóng góp cụ thể

- Triển khai quy trình xử lý claim, tính quote từ đơn hàng, gọi host để kiểm approval và ghi refund; xử lý retry, crash và trace.
- Commit code: `d69e54f` trên nhánh `PHAMVANNAM`.

#### Bằng chứng

- `python -m pytest -q -m student -o addopts= -k workflow`: 63 passed, 240 deselected.
- `python -m pytest -q`: 58 passed, 249 deselected trên nhánh `main` sau khi ghép các shape.
- Test mới `src/tests/test_workflow_run_id.py` bắt lỗi `run_id` không theo seed; đã sửa `workflow.py` và chạy lại xanh.
- Báo cáo riêng: [2A202603681_PhamVanNam.md](report/team/2A202603681_PhamVanNam.md).

### 2A202603686_LeNguyenHoangSon

#### Phần việc phụ trách

- Shape B `single` — `src/lab8/shapes/single.py`.

#### Đóng góp cụ thể

- Triển khai vòng ReAct giới hạn 8 bước với tool đọc, giữ ghi refund ở host.
- Commit `881f9cc`, `fc0cea7`; thêm/sửa `src/tests/test_single_agent_review.py`.

#### Bằng chứng

- Báo cáo riêng: [2A202603686_LeNguyenHoangSon.md](report/team/2A202603686_LeNguyenHoangSon.md).
- Bộ student hiện tại có 249/249 test pass; kết quả riêng của single ghi trong báo cáo cá nhân.

### HoangHaiNam — cần xác nhận MSSV

#### Phần việc phụ trách

- Orchestrator CP2 trong `src/lab8/shapes/orchestrator.py`.

#### Đóng góp cụ thể

- Commit triển khai `9c379e7` theo lịch sử Git. Chưa có bằng chứng test do cá nhân thêm/sửa.

#### Bằng chứng

- Bộ student hiện tại có 249/249 test pass; cần bổ sung báo cáo cá nhân và test của thành viên.

### 2A202603695_PhamThanhTung

#### Phần việc phụ trách

- Orchestrator CP3: handoff và chuyển `crash_at` vào host.

#### Đóng góp cụ thể

- Commit triển khai `6c2bf8d`: tạo handoff đã sanitize, giới hạn investigator ở tool chỉ đọc, và truyền `crash_at` vào host refund.

#### Bằng chứng

- `python -m pytest -q -m student -o addopts= -k orchestrator`: 62 passed, 251 deselected.
- Báo cáo riêng: [2A202603695_PhamThanhTung.md](report/team/2A202603695_PhamThanhTung.md).
- Cần bổ sung một test do cá nhân thêm hoặc sửa trước khi nộp, theo yêu cầu submission.
