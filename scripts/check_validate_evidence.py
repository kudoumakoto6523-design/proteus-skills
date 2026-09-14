"""Self-check the evidence validator without requiring Proteus."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

from validate_evidence import EvidenceError, validate


blocked = {
    "schema_version": 1,
    "stages": [
        {"name": "sdf", "status": "structurally_verified", "evidence": ["c.sdf"]},
        {"name": "runtime", "status": "blocked", "error": "model error"},
    ],
}
assert validate(blocked)["runtime"] == "blocked"

runtime = {
    "schema_version": 1,
    "stages": [{"name": "runtime", "status": "runtime_verified", "evidence": ["run.json"]}],
}
assert validate(runtime, require_runtime=True)["runtime"] == "runtime_verified"

try:
    validate({
        "schema_version": 1,
        "stages": [{
            "name": "runtime",
            "status": "runtime_verified",
            "evidence": ["run.json"],
            "error": "SPICE singular matrix",
        }],
    })
except EvidenceError:
    pass
else:
    raise AssertionError("runtime errors must block runtime_verified")

with tempfile.TemporaryDirectory(prefix="proteus-evidence-") as directory:
    path = Path(directory) / "verification.json"
    path.write_text(json.dumps(blocked), encoding="utf-8")
    result = subprocess.run([sys.executable, str(Path(__file__).with_name("validate_evidence.py")), str(path)],
                            capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["runtime"] == "blocked"

print("evidence validator self-check passed")
