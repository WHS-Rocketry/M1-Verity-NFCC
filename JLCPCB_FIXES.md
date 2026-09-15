# JLCPCB rule fixes — 2026-09-15

Applied to `M1-Verity-NFCC-main/NFCC.kicad_pcb` and its project libraries. Open `NFCC.kicad_pro` to load the custom rules and project-local footprints.

## Changes

- Enlarged silkscreen text to at least 1.0 mm with at least 0.15 mm strokes. Repositioned I2C, TELEM2, PWM and C63 labels for spacing.
- Moved the GND via beside SW6 from (120.523126, 62.943099) to (120.65, 62.90) mm and moved its attached track endpoint. This increases clearance to the switch's non-plated locating hole beyond the imported 0.50 mm requirement.
- Rebuilt the missing `NFCC.pretty` project library from all 102 embedded footprints, including the existing model assignments.
- Preserved the imported rules and added explicit rules to retain 0.20 mm general track clearance, check 0.15 mm SMD pad spacing, and separate component PTH annular rings (0.15 mm minimum) from via annular rings (0.10 mm minimum).
- Removed old per-pad clearance overrides from U3 and U10 so they cannot bypass the current rules. U10's pad width along its 0.50 mm pitch changed from 0.3556 to 0.3400 mm; pad length remains 0.3810 mm. Adjacent pad spacing increases from 0.1444 to 0.1600 mm. Positions, pin mapping and connectivity remain unchanged. This is a small land-pattern adjustment; the footprint remains subject to normal assembly review.
- Refilled copper pours using the corrected rules and set compliant defaults for future silkscreen text.

## Validation

Initial DRC: 314 warnings (107 text-thickness, 104 text-height, 100 missing-library, two reports of the same hole-spacing issue, and one silkscreen overlap). No unconnected items or schematic parity issues.

The subsequent override audit exposed U10 pad-spacing violations that had been masked by local clearance overrides. These were corrected geometrically, without exclusions or reduced rule severities.

Final DRC, including warnings and schematic parity: **0 violations, 0 unconnected items, 0 schematic parity issues**. See `checks/latest-drc.json` and `checks/latest-validation.json`. Component positions, all pin-to-net mappings, 3D model assignments and the schematic were preserved.

Prior files are backed up in the local working project; Git history preserves repository versions. The change does not establish circuit functionality, load capacity, controlled impedance or fabrication release readiness. The selected JLCPCB rules assume a routed, four-layer board with 1 oz copper; stackup and production options still need to match the order.

## Rule source

[JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), checked 2026-09-15: legend requirements, SMD pad spacing and multilayer 1 oz component-hole annular rings. Existing imported requirements were retained where more conservative. The imported file's TODO comments describe checks that are not implemented by that file; this is not a complete JLCPCB DFM certification.

## PWM header spacing correction

PWM_SIG2 now sits at Y=126.84 mm, giving 2.54 mm pitch between all three GND / +5 V / signal rows. Reconnected the signal traces, rerouted PWM_5/6/7 locally, and added one PWM_7 through via. The mating header footprints share an inner courtyard boundary and one outer silkscreen outline. No rule clearances or severities were reduced.
