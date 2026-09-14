# Verification Evidence Contract

Proteus projects can be structurally valid while a simulation still fails. Keep
these claims separate in every delivered verification manifest.

## Statuses

- `constructed`: the project or artifact was written.
- `reopened`: the saved project was reopened with the public API.
- `structurally_verified`: components, pins, connections, or an SDF export were
  checked. This does not prove that the circuit can run.
- `runtime_verified`: a real simulation ran and the expected output was
  observed. This status requires runtime evidence and must not coexist with a
  runtime error.
- `blocked`: the stage was attempted but could not be completed because of a
  model, version, license, or API limitation.
- `not_run`: the stage was not attempted.

## Manifest shape

Use a JSON file with a `schema_version`, an optional `environment`, and a list
of uniquely named `stages`:

```json
{
  "schema_version": 1,
  "project": "counter.pdsprj",
  "environment": {
    "proteus": "8.16.36097",
    "python": "3.12",
    "library": "proteus-automatic-api 0.2.0"
  },
  "stages": [
    {
      "name": "sdf",
      "status": "structurally_verified",
      "evidence": ["artifacts/counter.sdf"]
    },
    {
      "name": "runtime",
      "status": "blocked",
      "error": "SPICE singular matrix",
      "evidence": ["logs/runtime.txt"]
    }
  ]
}
```

`runtime_verified` is only valid when the `runtime` stage has non-empty
evidence and no `error`, `runtime_error`, `exception`, or `errors` field. A
blocked or unrun runtime stage is an honest result; it is not a failed report.

Validate a manifest before delivery:

```powershell
py -3.12 scripts/validate_evidence.py verification.json
py -3.12 scripts/validate_evidence.py --require-runtime verification.json
```

The second command is appropriate for a deliverable that promises a real
runtime result. The validator never upgrades a structural result to a runtime
result.
