# Added IC model sources

Downloaded 2026-09-15. All model files are stored in this project and referenced with `${KIPRJMOD}` in both the PCB and local footprint library. STEP files are unmodified; transforms are stored in the KiCad model assignments.

| Reference | Part | Model source |
| --- | --- | --- |
| U3 | LD39200PU33R | [KiCad generic DFN-6 package](https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/master/Package_DFN_QFN.3dshapes/DFN-6-1EP_3x3mm_P0.95mm_EP1.7x2.6mm.step) |
| U7 | BMP581 | [EasyEDA exact-part listing C5362283](https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/13dde21fc63a4ff9b98e25478c074390) |
| U8 | W25N01GVZEIG | [EasyEDA exact-part listing C907645](https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/aec8523d94b0445a92ea7d52b60254c2) |
| U10 | IIS2MDCTR | [KiCad generic LGA-12 package, height adjusted](https://gitlab.com/kicad/libraries/kicad-packages3D/-/raw/master/Package_LGA.3dshapes/LGA-12_2x2mm_P0.5mm.step) |
| U11 | 24CW1280T-I/OT | [EasyEDA exact-part listing C2061808](https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/de83a77687e64788a98e316d865b3813) |

## Fit and limitations

- **U3:** 3 × 3 mm, 0.95 mm pitch; 0.87 mm model height. Generic body and exposed-pad representation; not manufacturer-certified CAD.
- **U7:** 2 × 2 mm metal-lid body and matching ten-land layout. Model height 0.801 mm; Bosch specifies 0.75 mm nominal. Catalog visualization, not exact mechanical signoff.
- **U8:** 8 × 6 mm WSON body, 1.27 mm pitch; pin 1 at upper left. Overall model extents 8.02 × 6 × 0.811 mm, including terminals/marking.
- **U10:** 2 × 2 mm, 0.5 mm pitch, four lands on left/right and two top/bottom. Z scale 0.6829268293 adjusts 1.025 mm source body to 0.7 mm overall. This also scales land thickness; approximate visual envelope only.
- **U11:** SOT-23-5, 0.95 mm pitch. Rotated 90 degrees to put three leads on left and pin 1 upper left; lifted 0.75 mm to put terminal undersides on board. Model height 1.151 mm.

Model-only edits preserve all copper, placements, pads, nets, zones, rules and schematic data. Top-view inspection confirms body orientation and terminal placement. All model paths resolve. Holes, test pads, the solder jumper and silkscreen artwork intentionally have no body models.

Sources are catalog/package visualizations, not certified manufacturer tolerance models. Consult the component package drawings for final enclosure clearances. Original KiCad model copyright/license notices remain inside those STEP files. EasyEDA files retain original content/markings; no new redistribution license is asserted. Source hashes and transforms are recorded in `model-sources.json`.
