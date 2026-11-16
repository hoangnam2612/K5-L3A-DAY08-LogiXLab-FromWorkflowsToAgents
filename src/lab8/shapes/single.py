"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (README): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(
    conn: sqlite3.Connection,
    claim_id: str,
    *,
    seed: int,
    crash_at: str | None,
) -> RunResult:
    budget = Budget()
    run_id = make_run_id("single", claim_id, seed)
    trace = Trace(run_id)

    # 1. Đọc claim qua tool giới hạn dữ liệu.
    budget.add_tool(tool_cost())
    claim = get_claim_view(conn, claim_id)

    if not claim["found"]:
        trace.add("error", {"reason": "unknown_claim"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="unknown_claim",
        )

    # 2. Thiếu mã đơn: cần bổ sung thông tin.
    if not claim["order_id"]:
        trace.add("decision", {"status": "needs_info"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="needs_info",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="missing_order_id",
        )

    # MockLLM chi mo phong doc ticket; ket qua khong quyet dinh tien hay tool.
    # MockLLM hien co khong cung cap giao dien tra ve lua chon tool.
    complete(budget, seed=seed, purpose="parse", prompt=claim["ticket"])

    # 3. Lưu trạng thái giữa các lượt gọi decide().
    # Không lưu claim hoặc ticket vào trace.
    stage: dict[str, Any] = {
        "i": 0,
        "order_view": None,
    }

    def decide(seen: dict[str, Any]) -> dict[str, Any]:
        # Lượt đầu: yêu cầu đọc đơn hàng.
        if stage["i"] == 0:
            stage["i"] = 1
            trace.add("action", {"tool": "lookup_order"})

            return {
                "tool": "lookup_order",
                "args": {
                    "order_id": claim["order_id"],
                    "principal_id": claim["principal_id"],
                },
            }

        # Lượt hai: nhận kết quả đọc đơn.
        if stage["i"] == 1:
            order_view = seen["last_result"]
            stage["order_view"] = order_view

            trace.add(
                "order",
                {
                    "visible": order_view["visible"],
                    "reason": order_view.get("reason"),
                },
            )

            # Không xem được đơn: dừng vòng đọc.
            if not order_view["visible"]:
                return {"final": {"order_view": order_view}}

            # Xem được đơn: yêu cầu tính quote từ dữ liệu đơn.
            stage["i"] = 2
            trace.add("action", {"tool": "compute_compensation"})

            return {
                "tool": "compute_compensation",
                "args": {"order": order_view["order"]},
            }

        # Lượt ba: nhận quote và kết thúc vòng đọc.
        quote = seen["last_result"]
        trace.add("quote", quote)

        return {
            "final": {
                "order_view": stage["order_view"],
                "quote": quote,
            }
        }

    # Runtime tự đếm chi phí tool qua dispatch().
    # worker=True giới hạn tool được chọn vào allowlist đọc.
    out = run_react(
        conn,
        budget,
        observation={"claim": claim},
        decide=decide,
        max_steps=8,
        worker=True,
    )

    # 4. Nếu hết số bước mà chưa có final: thất bại.
    if out["stopped"] != "final":
        trace.add("error", {"reason": "step_cap"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="failed",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason="step_cap",
        )

    final = out["final"]
    order_view = final["order_view"]

    # 5. Đơn không tồn tại hoặc ngoài quyền xem: chuyển cấp.
    if not order_view["visible"]:
        trace.add("decision", {"status": "escalated"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="escalated",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=order_view.get("reason"),
        )

    quote = final["quote"]
    proposal = int(quote["amount_vnd"])

    # 6. Quote bằng 0: không gọi host hoàn tiền.
    if proposal <= 0:
        trace.add("decision", {"status": "denied"})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status="denied",
            proposal_amount=0,
            budget=budget,
            trace=trace,
            error_reason=quote.get("reason"),
        )

    # 7. Ngoài vòng ReAct, shape gọi host với quote đầy đủ.
    # Host kiểm approval và tự trừ tiền đã hoàn trước đó.
    outcome = issue_refund(
        conn,
        claim_id,
        proposal,
        crash_at=crash_at,
    )

    # Chỉ ghi thông tin cần thiết của kết quả host.
    trace.add(
        "refund_outcome",
        {
            "ok": outcome["ok"],
            "reason": outcome["reason"],
            "conflict": outcome["conflict"],
        },
    )

    # 8. Xung đột → failed; host từ chối → denied.
    if not outcome["ok"]:
        status = "failed" if outcome["conflict"] else "denied"
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=outcome["reason"],
        )

    return finish(
        conn,
        shape="single",
        claim_id=claim_id,
        seed=seed,
        status="resolved",
        proposal_amount=proposal,
        budget=budget,
        trace=trace,
        error_reason=None,
    )
