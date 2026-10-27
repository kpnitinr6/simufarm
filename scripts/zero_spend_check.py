"""Report a task declaration's zero-spend gate; never execute the task or call billing APIs."""

import json
import sys
from pathlib import Path

import yaml


def assess(task):
    check = task.get("zero_spend_check", {})
    allowed = (
        check.get("will_create_bill") is False
        and check.get("execution_class") == "local_only"
        and check.get("passed") is True
    )
    return {
        "task": task.get("id"),
        "allowed_local_preparation": allowed,
        "external_execution_authorized": False,
        "reason": "Local-only declared preparation"
        if allowed
        else "Unknown/external cost or approvals: blocked",
        "note": "Declaration check only; no action executed and no billing guarantee",
    }


if __name__ == "__main__":
    result = assess(yaml.safe_load(Path(sys.argv[1]).read_text()))
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["allowed_local_preparation"] else 2)
