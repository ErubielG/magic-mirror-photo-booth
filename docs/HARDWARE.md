# Hardware integration

- Repurposed lululemon Studio Mirror: 40-inch Full HD LVDS panel.
- Replacement M.NT68676.3 LCD driver (HDMI input, LVDS output).
- Raspberry Pi 4 (4 GB), Sony IMX708 camera.
- MEGMEET existing 12 V / 24 V PSU and 12 V-to-5 V buck converter.
- Canon SELPHY CP1500 4×6 dye-sub printer using manual print handoff.

During teardown, the CON5 harness had **red = ground** and **black = 12 V**, opposite common color conventions. Conductors were checked against silkscreen with a multimeter and individually insulated. Do not assume wire colors. Mains-side 120 V exposure is a significant service risk; unplug and verify safe state before opening. The project does not document new fusing or enclosure interlocks.
