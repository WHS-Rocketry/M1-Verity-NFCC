

## Current PCB validation

Open `NFCC.kicad_pro` in KiCad to load the project rules and bundled footprint library. The PCB includes the JLCPCB rule fixes and standard 2.54 mm GND / 5 V / PWM header spacing. See [change details](JLCPCB_FIXES.md).

Latest DRC: **0 violations, 0 unconnected items, 0 schematic parity issues**. Reports and a preview are in `checks/`. This is a prototype review design; a clean DRC does not establish production readiness. Power/load validation, final stackup and electrical/assembly review, and physical prototype testing remain necessary.
