"""Validate a Proteus verification evidence manifest.

The validator is intentionally independent of Proteus and uses only the
standard library, so it can run before a report is assembled.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STATUSES = {
    "constructed",
    "reopened",
    "structurally_verified",
    "runtime_verified",
    "blocked",
    "not_run",
}
RUNTIME_ERROR_FIELDS = ("error", "runtime_error", "exception", "errors")


class EvidenceError(ValueError):
    """Raised when a manifest makes an unsupported evidence claim."""


def _non_empty(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def validate(manifest: dict[str, Any], *, require_runtime: bool = False) -> dict[str, Any]:
    """Return a summary or raise :class:`EvidenceError` for invalid evidence."""
    if not isinstance(manifest, dict):
        raise EvidenceError("manifest must be a JSON object")
    if manifest.get("schema_version") != 1:
        raise EvidenceError("schema_version must be 1")

    stages = manifest.get("stages")
    if not isinstance(stages, list) or not stages:
        raise EvidenceError("stages must be a non-empty list")

    seen: set[str] = set()
    summary: dict[str, str] = {}
    for index, stage in enumerate(stages):
        if not isinstance(stage, dict):
            raise EvidenceError(f"stages[{index}] must be an object")
        name = stage.get("name")
        status = stage.get("status")
        if not isinstance(name, str) or not name.strip():
            raise EvidenceError(f"stages[{index}].name must be a non-empty string")
        if name in seen:
            raise EvidenceError(f"duplicate stage name: {name}")
        if status not in STATUSES:
            raise EvidenceError(f"{name}: unsupported status {status!r}")
        seen.add(name)
        summary[name] = status

        evidence = stage.get("evidence", [])
        if evidence and (not isinstance(evidence, list) or
                         not all(isinstance(item, str) and item.strip() for item in evidence)):
            raise EvidenceError(f"{name}: evidence must be a list of non-empty strings")

        if status == "runtime_verified":
            if name != "runtime":
                raise EvidenceError("runtime_verified is only valid for the runtime stage")
            if not evidence:
                raise EvidenceError("runtime: runtime_verified requires evidence")
            errors = [field for field in RUNTIME_ERROR_FIELDS
                      if _non_empty(stage.get(field))]
            if errors:
                raise EvidenceError(
                    "runtime: runtime_verified cannot include runtime errors: " + ", ".join(errors)
                )

    if require_runtime and summary.get("runtime") != "runtime_verified":
        raise EvidenceError(
            "runtime result required; status is " + repr(summary.get("runtime", "missing"))
        )
    return {"valid": True, "stages": summary, "runtime": summary.get("runtime", "missing")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--require-runtime", action="store_true",
                        help="fail unless the runtime stage is runtime_verified")
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = validate(manifest, require_runtime=args.require_runtime)
    except (OSError, json.JSONDecodeError, EvidenceError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
