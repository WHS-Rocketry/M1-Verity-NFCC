

## Current PCB validation

Open `NFCC.kicad_pro` in KiCad to load the project rules and bundled footprint library. The PCB includes the JLCPCB rule fixes and standard 2.54 mm GND / 5 V / PWM header spacing. See [change details](JLCPCB_FIXES.md).

Latest DRC: **0 violations, 0 unconnected items, 0 schematic parity issues**. Reports and a preview are in `checks/`. This is a prototype review design; a clean DRC does not establish production readiness. Power/load validation, final stackup and electrical/assembly review, and physical prototype testing remain necessary.

### Adjacent external connectors

The I²C and telemetry PicoBlade connectors are adjacent on the left edge, facing outward, with 12.2 mm between their centres. Their pin assignments are unchanged. The nearby battery-sense parts and I²C pullups were repositioned and the affected connections rerouted. The PWM headers retain 2.54 mm row spacing.
