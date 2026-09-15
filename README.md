# NFCC revision C — compact review draft

Open `NFCC.kicad_pro` in KiCad 10. Revision C is the latest design. The earlier revision B, including the user's original copper logo, remains unchanged in `../revision-b/`.

## Requested changes

- Reduced the board from **100 × 80 mm to 90 × 70 mm**, reducing area by **21.25%**.
- Grouped both Micro USB-B sockets on the right edge. J1 is the MCU USB port; J2 is the debug bridge port. Their centres are **13 mm apart**. Confirm the actual cable overmoulds fit together during mechanical review.
- Increased the general copper-routing clearance from **0.127 to 0.20 mm**. All signal and power net classes use 0.20 mm clearance. The existing package-specific pad-to-pad rules remain: 0.127 mm within U10 and 0.15 mm within U3. These accommodate the fixed footprint geometry; they do not relax general trace spacing.
- Retained front/back GND pours, the internal GND plane and internal 3.3 V plane, with 27 deliberately placed ground stitching vias. Header-area cutouts remove isolated outer copper while retaining internal ground connections.
- Moved the user's logo to **front silkscreen**, as requested, and resized it to fit a 12 mm square without overlapping pads.
- Preserved PicoBlade telemetry/I²C ports, PWM male headers, and the XT60/Micro USB connector models. Repositioned the XT60 and debug circuitry to fit the smaller outline.
- Kept the MCU USB data paths adjacent on front copper with no signal vias. The debug USB routing uses two vias on D+; its impedance and skew still require review against the selected manufacturer stackup.

## Saved-board validation

`checks/final-drc.json`: **0 PCB rule violations, 0 unconnected items, 0 schematic parity issues** after zone refill.

`checks/final-erc.json`: **0 schematic errors, 21 existing warnings**. These include imported symbol/library differences, unspecified electrical pin types, supply naming and a dangling no-connect flag. All exported schematic pin-to-net mappings were checked against PCB pads with zero mismatches.

`checks/board-top.png` is the inspected 3D preview. `checks/routed-board.svg` shows the copper and silkscreen. Component placement is in `checks/final-components.csv`, and design-file hashes are in `checks/validated-sha256.json`.

## Retained electrical requirements

- 2S LiPo input: 8.4 V fully charged, with a 10 V design ceiling. This is a requirement, not a tested rating.
- Total 5 V load remains unspecified. Supply trace widths, capacitor/inductor selection, USB power limits and regulator thermal performance remain provisional.
- Previous working-schematic corrections remain: direct TPS54302 VIN-to-VBAT connection, a 10 kΩ enable pullup, a 73.2 kΩ / 10 kΩ feedback divider, and unified main 3.3 V supply naming.
- TELEM2 pins: 1 = 3.3 V, 2 = GND, 3 = TELEM_RX, 4 = TELEM_TX.
- I2C5 pins: 1 = 3.3 V, 2 = GND, 3 = I2C4_SCL, 4 = I2C4_SDA.
- XT60 J3 pins: 1 = GND, 2 = VBAT. Check the purchased connector and battery lead polarity during assembly review.

This remains a review draft, not a fabrication release. Finalize the load requirement, component ratings, power/USB electrical review and enclosure fit before fabrication. DRC does not establish circuit function, current capacity or controlled impedance. See the previous revision's README for part references and the original schematic corrections.

## Project contents

- `NFCC.kicad_pcb`, `NFCC.kicad_sch`, `NFCC.kicad_pro`, `NFCC.kicad_dru`: authoritative revision C design and rules.
- `NFCC.pretty`, `NFCC.kicad_sym`, `fp-lib-table`, `sym-lib-table`: local libraries.
- `NFCC.3dshapes`: connector and IC STEP models, with source/transform records.
- `checks`: validation, previews and intermediate work. Scripts are not an idempotent release build; rerunning them can overwrite the final board.

## Added IC models

Added body models for U3, U7, U8, U10 and U11 from online KiCad and EasyEDA libraries. U3 uses a generic DFN package; U10 uses a generic LGA model with its height adjusted to 0.7 mm. The other three come from exact-part catalog entries. These are visual models with documented dimensional approximations; see [model sources](NFCC.3dshapes/README.md).

`checks/model-validation.json` verifies that only model assignments changed in the board and every model path resolves. `checks/models-drc.json` records the DRC after model additions. `checks/before-models` preserves the previous board and affected footprint files.
