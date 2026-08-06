---
name: proteus-schematic
description: Design, inspect, simulate, and export real electronic schematics in Proteus 8/ISIS. Use when the user mentions Proteus, ISIS, STM32 schematics, STM32F103C8T6/C8T6, sensor wiring, hardware circuit diagrams, or asks to draw the circuit directly in Proteus. Preserve an editable Proteus schematic; never substitute an image for the circuit.
---

# Proteus Schematic Design

## Goal

Build an editable, inspectable Proteus project that can be continued or simulated. Reuse the user's current project and canvas whenever possible. Create a new project only when explicitly requested. Save the Proteus project and export a clean schematic image only when the task needs a report figure.

## Before editing

1. Confirm the Proteus version, active window, project name, and project path. A common Windows installation is `<PROTEUS_INSTALL_DIR>\\BIN\\ISIS.exe`; one known example is `D:\\Proteus\\BIN\\ISIS.exe`.
2. Treat messages such as “done,” “I placed the C8T6,” or “you can switch” as a ready GUI state. Switch to Proteus only after the user allows it, inspect the existing canvas, and continue from the next missing step. Do not duplicate parts or clear the project.
3. Confirm the MCU, supply voltage, clock source, reset circuit, sensor interfaces, communication links, and debug connector from the firmware, datasheets, or project notes. Mark uncertain pins as pending confirmation rather than guessing.
4. Plan the page before wiring: place the MCU and power near the center, group sensors by signal flow, and keep communication/debug connectors at the edge. Prefer readable horizontal/vertical wiring with minimal crossings.

## Create or open a project

### Create a new project

1. Start `ISIS.exe` and choose File → New Project (or the equivalent command for the installed version).
2. Use the user's requested working directory. Avoid spaces and non-ASCII characters in the project filename when possible.
3. Keep the default schematic. Create a PCB layout only when the task requires it.
4. Save and verify that a project file (commonly `.pdsprj`) and a schematic file (commonly `.dsn`) exist.

### Continue an existing project

Open the `.pdsprj` with File → Open Project when available. If only a `.dsn` exists, open it and save it as a project. Save once before editing so subsequent GUI actions are attached to the intended copy.

## Find and place devices

1. Use the device picker (often `P`, or the toolbar command) to open Pick Devices.
2. Search by full part number or a functional keyword, for example `STM32F103C8T6`, `DHT11`, `OLED`, `LCD`, `crystal`, `terminal`, or `VIRTUAL TERMINAL`.
3. Check the preview for pin names, pin numbers, footprint, and simulation model. Similar search results may be PCB-only symbols and may not simulate.
4. Place the MCU, connectors, and power first; then place sensors, displays, indicators, and test instruments. Arrange each functional block immediately rather than stacking all parts in one area.
5. Rotate or mirror devices to keep pin names readable. Move reference designators and values away from wires when necessary.

## STM32/C8T6 hardware checklist

Use this as a review checklist, not as an unverified pin map:

- Connect `VDD/VDDA` to the project's specified digital/analog supply and `VSS/VSSA` to ground. Place local decoupling capacitors.
- Connect `NRST` to the intended reset network or reset connector, including pull-up/filter parts when required.
- Give `BOOT0` a defined ground, pull-up, or jumper state; do not leave it floating. Handle other boot pins according to the exact package and boot mode.
- Add an external crystal and load capacitors only when the firmware uses an external clock. Do not add a crystal without evidence.
- Reserve SWD (`SWDIO`, `SWCLK`, `NRST`, `3V3`, `GND`) or the required UART programming/debug connector.
- Mark deliberately unused pins with no-connect markers or the project's documented treatment. Do not accidentally wire them to a supply or signal.

## Wiring rules

1. Finish power and ground before signal wiring. Start each wire at a known pin and finish it on the intended pin; verify the connection marker before moving on.
2. Use horizontal/vertical routes. Split long or crowded routes with unique net labels such as `WIND_PULSE`, `RAIN_IN`, and `UART_TX`.
3. Use Proteus power terminals/power symbols for supply nets. Plain text such as `3V3` is not a power connection. Match the power symbol name to the actual voltage.
4. Confirm junctions at branches. Crossing lines without a junction are not connected. Replace excessive crossings with clear net labels.
5. Zoom in and inspect every completed block: wire endpoints must snap to pins, adjacent pins must not be shorted, dangling wire ends must be intentional, and supply/ground must not be shorted.
6. Do not place screenshots, photos, or externally drawn pictures into Proteus as a circuit. A report may use an image exported from Proteus, but the project itself must contain real editable devices and wires.

## Environmental monitoring project grouping

For a project with wind speed, temperature/humidity, rainfall, LCD/OLED, and a PC/serial link, group the schematic into the following blocks and derive exact interfaces from the firmware:

- Wind speed: pulse, frequency, or analog voltage input; document range, signal conditioning, and MCU timer/capture channel.
- Temperature/humidity: one-wire, I2C, or another digital interface; document pull-ups, supply voltage, and timing constraints.
- Rain detection: switch, pulse, or analog input; document debouncing, pull-up/pull-down, and the measurement unit.
- LCD/OLED: I2C, SPI, or parallel interface; document address/chip-select, reset, and backlight supply.
- PC link: UART, USB-UART, or Bluetooth serial; document crossed TX/RX, common ground, and logic-level compatibility.

If Proteus lacks a model for a physical sensor, use a terminal, signal generator, pulse source, or logic switch as a clearly labelled simulation substitute. Do not label the substitute as the real sensor.

## Inspection and simulation preparation

1. Save the project. Check the MCU program-file path, clock frequency, and simulation model properties. STM32 simulation depends on the available model and firmware; a schematic alone does not guarantee a runnable simulation.
2. Build repeatable test inputs with logic switches, pulse sources, signal generators, or virtual terminals.
3. Run the available ERC/electrical-rule check. Fix power-drive, floating-pin, short-circuit, and multiple-output errors first. Document intentional warnings before ignoring them.
4. Test one variable at a time: for example, hold temperature/humidity constant, vary the wind pulse frequency, and toggle the rainfall input while observing the LCD and serial output.
5. Debug in this order: power → ground → reset/clock → interfaces → signal processing → display/PC output.

## Report figures and handoff

1. Fit the page and zoom so the MCU, sensors, interfaces, and power are legible. Export both an overall diagram and detail views when one page is too dense.
2. Use Proteus's own export, print, or high-resolution capture function. Caption the figure as a Proteus schematic and identify the main devices and interfaces.
3. Keep the original `.pdsprj`/`.dsn` files alongside any PNG. Save again before export so the figure and project match.
4. Record the verification status: project opens, devices remain editable, key nets are connected, simulation runs or does not run, and which parts use substitute models.

## Troubleshooting

- **STM32F103C8T6 is missing:** check the device libraries, try a precise or family-level search, and document any model/package difference.
- **A part can be placed but cannot simulate:** check for a simulation model and program file. If unavailable, use a clearly labelled substitute or limit the result to schematic documentation.
- **A wire looks connected but the signal is dead:** zoom in, check endpoint snapping and junctions, redraw from the pin, or use a unique net label.
- **The user is working in another window:** announce the intended switch and wait for permission. Never seize the window without permission.
- **A shortcut, symbol, or pin is uncertain:** use the menu, datasheet, firmware, or project documentation; preserve the current project and ask for confirmation instead of guessing.

## Reference

Read [proteus-workflow.md](references/proteus-workflow.md) for the detailed interaction rhythm, common commands, startup example, and handoff checklist.
