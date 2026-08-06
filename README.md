# Proteus Schematic Design Skill

An open-source Codex skill for designing, inspecting, simulating, and documenting real electronic schematics in Proteus 8/ISIS.
## Things to Say
This is my first time uploading a skill, which is related to circut designing. There are many other simulation skills, while few focus on Proteus, which is widely used by college students majoring in EEE. Although the skill, right now, is primary, which does not contain skills to draw PCBs, or even dosen't have some necessary skills such as running the simulation, etc, its ability is up to our joint cooperation, up to all very talented developers who is willing to contribute their own idea. Thank you for your interest to this project. 
## What it does

This skill helps Codex:

- Open or continue a Proteus project without losing the user's current GUI state.
- Find and place STM32F103C8T6/C8T6 devices and common sensor, display, terminal, and power symbols.
- Build readable, editable power, reset, clock, sensor, LCD/OLED, UART, Bluetooth, and debug connections.
- Check junctions, net labels, floating pins, power mistakes, and simulation-model limitations.
- Prepare repeatable simulation inputs and export report-ready schematic figures from Proteus.

It explicitly keeps the circuit as a real Proteus schematic. A screenshot or externally drawn image is not treated as a substitute for editable components and wires.

## Repository layout

```text
proteus-schematic/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── proteus-workflow.md
├── README.md
├── DISCLAIMER.md
├── LICENSE
└── .gitignore
```

## Install for Codex

### From GitHub

In Codex, invoke `$skill-installer` and provide the GitHub URL for this skill directory, for example:

```text
https://github.com/<OWNER>/<REPOSITORY>/tree/main
```

If the skill is stored under a subdirectory, provide that subdirectory URL. The installer places it under the user's Codex skills directory.

### Manual installation

Copy this folder to the user skill directory:

```text
%USERPROFILE%\.codex\skills\proteus-schematic
```

Restart Codex if the new skill does not appear in the skill list. It can be invoked explicitly as `$proteus-schematic`, or selected implicitly when a request matches its description.

## Example prompts

```text
Use $proteus-schematic to continue the current STM32F103C8T6 Proteus schematic.
Use the Proteus skill to review the power, reset, sensor, LCD, and UART connections.
Draw the hardware circuit directly in Proteus and export a report-ready schematic figure.
```

## Proteus installation path

The skill treats `D:\Proteus\BIN\ISIS.exe` as an example only. Replace it with the actual Proteus installation directory on the target computer.

## Development and validation

Keep `SKILL.md` focused on workflow instructions. Put detailed, conditional procedures in `references/`. Before publishing changes, run the Codex skill validator:

```powershell
$env:PYTHONUTF8 = '1'
py -3 <CODEX_SKILL_CREATOR>\scripts\quick_validate.py .
```

Then test representative prompts involving: continuing a user-placed C8T6, wiring a sensor block, handling a missing simulation model, and exporting a report figure.

## Contact

Questions, suggestions, and contributions: [kudoumakoto6523@gmail.com](mailto:kudoumakoto6523@gmail.com)

## License and disclaimer

This project is released under the MIT License. Read [DISCLAIMER.md](DISCLAIMER.md) before using the workflow for hardware, simulation, coursework, or engineering decisions.
