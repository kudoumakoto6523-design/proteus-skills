# Proteus 8 Schematic Workflow Reference

## Startup and state confirmation

The executable is often located at `<PROTEUS_INSTALL_DIR>\\BIN\\ISIS.exe`; one example is `D:\\Proteus\\BIN\\ISIS.exe`. Start it with an explicit path when needed:

```powershell
Start-Process -FilePath 'D:\Proteus\BIN\ISIS.exe'
```

If the installation path differs, inspect the directory and use the actual executable. After Proteus opens, verify the title bar, project name, active page, and editor focus instead of assuming the schematic editor has focus.

## Safe interaction rhythm

Proteus mouse operations are sensitive to zoom, focus, and grid snapping. Use a short loop:

1. Create or open the project and verify that it is saved.
2. Place one functional block and check that device labels and pins are visible.
3. Wire that block's power, ground, and signals; zoom in to check endpoints.
4. Save before moving to the next block.

When the user is actively using the computer, announce “I am ready to switch to Proteus” and wait for permission. After the user confirms, switch windows and inspect the current state before clicking.

## Common commands

Keyboard shortcuts vary by Proteus version and layout. Treat the menu and toolbar as authoritative:

| Operation | Common method | Verify |
| --- | --- | --- |
| Pick a device | `P` or Pick Devices | Device picker appears |
| Place a device | Select it, then click the canvas | Device lands on the grid |
| Wire | Select the wire tool or start at a pin | Endpoints snap and junctions appear |
| Rotate | Rotate tool or context menu | Orientation changes; pin numbers do not |
| Edit properties | Double-click the device | Value, model, and simulation fields appear |
| Add power/ground | Power-terminal tool | A real named power net is present |
| Run simulation | Run/play control | Simulation enters a running state |
| Save | `Ctrl+S` or File → Save | No unsaved marker remains |

## Handoff checks

- Both `.pdsprj` and `.dsn` exist.
- The MCU program-file path is stable and accessible to the recipient.
- Reopening the project preserves devices, net labels, text, and page boundaries.
- Exported images come from the current Proteus canvas, not from a chat attachment or an external drawing tool.
