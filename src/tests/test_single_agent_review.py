import json
from pathlib import Path

from lab8.shapes.single import run_claim


def test_single_uses_mock_without_trusting_ticket(public_db):
    # C-002 claims a longer delay than the order actually records.
    result = run_claim("C-002", seed=55, store_path=str(public_db))

    assert result.status == "denied"
    assert result.proposal_amount == 0
    assert result.model_calls == 1
    assert result.input_tokens > 0
    trace = json.loads(Path(result.trace_path).read_text(encoding="utf-8"))
    assert "CANARY_SECRET_" not in json.dumps(trace)
