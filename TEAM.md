# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: [https://github.com/hoangnam2612/K5-L3A-DAY08-LogiXLab-FromWorkflowsToAgents](https://github.com/hoangnam2612/K5-L3A-DAY08-LogiXLab-FromWorkflowsToAgents)
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên       | MSSV        | Email                                                                | GitHub      | Vai trò  |
| ---: | ------------ | ----------- | -------------------------------------------------------------------- | ----------- | -------- |
| 1   | Phạm Văn Nam | 2A202603681 | [nampham2662@gmail.com](mailto:nampham2662@gmail.com) (email commit) | NamPham1012 | Workflow |
| 2   |              |             |                                                                      |             |          |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Phạm Văn Nam | Workflow | `d69e54f` (triển khai ban đầu); commit bổ sung test và sửa `run_id` trên nhánh `PHAMVANNAM` | Thêm `src/tests/test_workflow_run_id.py`; 63 test workflow pass |

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
- `python -m pytest -q`: 54 passed, 249 deselected.
- Test mới `src/tests/test_workflow_run_id.py` bắt lỗi `run_id` không theo seed; đã sửa `workflow.py` và chạy lại xanh.
- Báo cáo riêng: [2A202603681_PhamVanNam.md](report/team/2A202603681_PhamVanNam.md).
