# Proteus Skills

[简体中文](README.md) | **English**

<p align="center">
  <img src="images/stm32-hold.gif" alt="按住点灯" width="31%" />
  <img src="images/stm32-toggle.gif" alt="单击切换" width="31%" />
  <img src="images/stm32-dual.gif" alt="双按键独立点灯" width="31%" />
</p>



[![MIT Licensed](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE)

Let AI agents create, edit, and verify real Proteus circuit projects through Python.

**Undergraduates, particularly those studying Electrical Engineering(EE), often find themselves struggling with Proteus simulations. Today, we’re introducing Proteus skills! This skill allows AI to carry out Proteus simulations. Don’t let tedious wiring and layout hold back the brilliant ideas in your head!**

Proteus Skills provides workflows for schematic editing, microcontroller simulation, button and switch control, and waveform extraction. Agents use [proteus-automatic-api](https://github.com/kudoumakoto6523-design/Proteus_automatic_package) to deliver editable `.pdsprj` projects, verification scripts, and actual simulation results.

This repository contains the skill instructions and reference examples. The Python library is maintained separately; the agent checks and installs it from the official GitHub repository during initial setup. The repositories do not need to be adjacent.

This tool is functional, but there are numerous areas that require refinement. If you are also struggling with simulation and would like to use AI to solve this problem, please contact me at: `kudoumakoto6523@gmail.com`
## Requirements

- **Windows**, with Proteus and the device models required by your circuit installed.
- **Python 3.10+**, preferably 3.12. The agent checks the interpreter and helps install it if missing. You do not need to obtain library source code or a wheel first.
- **Codex**: the instructions below cover installing and invoking the skill in Codex.

The workflows have been verified with **Python 3.12 / Proteus 8.16 SP3 (8.16.36097)**. Timed simulation and interactive controls require supported Proteus DLL versions; compatibility with other builds has not been verified. Proteus software, models, official samples, and third-party firmware are not bundled with this skill; this repository provides only original demo firmware.

## Installation

### 1. Install the skill

Send this request in Codex:

```text
Use $skill-installer to install https://github.com/kudoumakoto6523-design/proteus-skills
The repository root is the skill directory. Install it with the name proteus-skills.
```

Alternatively, download this repository and place `SKILL.md`, `agents/`, `references/`, `scripts/`, and `LICENSE` together in a folder named `proteus-skills` under Codex's `$CODEX_HOME/skills/`. The default location is `~/.codex/skills/proteus-skills/`. The installed entry point should be `proteus-skills/SKILL.md`. Keep `examples/stm32/` as well when running the repository demos.

### 2. Ask the agent to prepare the environment and start

After installing the skill, send this request in your next message:

```text
Use $proteus-skills. I only have Proteus installed. Check Python and the library first;
if needed, install proteus-automatic-api from the official GitHub repository specified
by the skill, verify it, and continue with my task.
Create an STM32 project where pressing a button turns an LED on and releasing it turns it off.
```

The agent runs the setup script bundled with the skill. If the library is missing, it creates a virtual environment in the task directory, resolves the latest default-branch commit from the [official GitHub repository](https://github.com/kudoumakoto6523-design/Proteus_automatic_package), checks the package name and API, and installs that commit's source ZIP. Git is not required, and installation does not wait for a PyPI release. The agent then verifies imports, records the version and commit, and continues the circuit task in the same run. It does not stop at installation instructions or wait for you to install the library manually.

A working installation is reused. To update, ask the agent to update `proteus-automatic-api` from the official GitHub repository and verify it; a newer commit can be installed even if its version number is unchanged. See the [installation workflow](references/distribution.md#首次安装与更新) for commands, old-package migration and offline installation.


## Before you start

Provide the agent with the project or template, the Proteus executable location, and an output directory. For MCU tasks, also provide the firmware and target pins. Creating a circuit requires a template containing the relevant device definitions; the resistor and capacitor example uses the official `Rescap.pdsprj` sample.

Use actual paths on your machine. Outputs belong in your working directory. The library's built-in paths do not automatically adapt to every installation; see [SKILL.md](SKILL.md#环境与版本) for path parameters and known limitations.



## Capabilities

| Task | Supported workflow |
| --- | --- |
| Project editing | Create or open supported `.pdsprj` files; edit components, properties, positions, wires, and terminals; save and reopen for verification |
| Connectivity checks | Query devices and pins, export native Proteus SDF netlists, and verify network connections |
| MCU simulation | Inspect and load ELF / HEX firmware; start, stop, pause, and run for a specified duration; read supported GPIO logs |
| Buttons and switches | Bind binary controls, press, release, or toggle them, and continue simulation to verify downstream responses |
| Waveform extraction | Export CSV data from existing graphs and probes, and read voltage, current, and sampled values |

All Proteus operations use the public `proteus_automatic_api` API, which drives real Proteus processes for netlists and simulation. Agents must not fill API gaps with Computer Use, OCR, screen coordinates, or other GUI automation. Unsupported operations are reported explicitly. Recording tools only capture passively.

## Known limitations

- Structural editing supports recognized single-user-sheet projects with CDB v7 and FILEVER 840/847. Rewriting projects with unknown objects, multiple sheets, or multi-unit structures may be rejected.
- Finding a device in the library does not establish that it can be imported or simulated. Automatic routing covers a limited set of orthogonal paths.
- Six types of binary controls are supported. They share 10 actuator key slots, using two slots per control, for a maximum of five controls. Existing bindings reduce the available capacity.
- Analog measurements require existing graphs and probes. There is no general ERC, arbitrary graph or probe creation, general live pin-voltage reading, or schematic image export API.


## Repository contents

The skill instructions and detailed workflow references are currently written in Chinese.

| File | Purpose |
| --- | --- |
| [examples/stm32](examples/stm32) | Original firmware sources, HEX files, and build scripts for the three button and LED scenarios |
| [images](images) | Shared directory for the README demo GIFs |
| [scripts/ensure_library.py](scripts/ensure_library.py) | Check, install or update the library and return the Python path for the task |
| [SKILL.md](SKILL.md) | Agent entry point, task selection, operation order, and verification requirements |
| [agents/openai.yaml](agents/openai.yaml) | Display name and short description in Codex |
| [references/api-workflows.md](references/api-workflows.md) | Examples for project editing, netlists, firmware, and measurements |
| [references/interactive-controls.md](references/interactive-controls.md) | Button and switch binding, timing, and response verification |
| [references/distribution.md](references/distribution.md) | Library installation, version matching, migration, and separate distribution conventions |
| [references/evidence-contract.md](references/evidence-contract.md) | Evidence rules for structural checks, runtime checks, and blocked results |

### Verification evidence

An exported SDF or a successful reopen does not prove that a simulation ran.
Before delivery, validate an evidence manifest with
`py -3.12 scripts/validate_evidence.py verification.json`; add
`--require-runtime` when a real runtime result is required. The validator
rejects `runtime_verified` when runtime errors are present and preserves
`blocked` / `not_run` as explicit outcomes.

## License

The original skill documentation and examples in this repository are licensed under the [MIT License](LICENSE). The Python library is distributed separately. Proteus software, device models, third-party samples, and firmware remain subject to their respective licenses.
