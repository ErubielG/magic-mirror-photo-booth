# System architecture

The 40-inch LCD panel is driven by an M.NT68676.3 LVDS controller replacing the original MIR63A0 board. Raspberry Pi 4 supplies HDMI video; a Sony IMX708 connects over CSI-2. The existing MEGMEET PSU supplies 12 V to the controller and 24 V to the backlight; a buck converter provides 5 V for the Pi. **Verify all actual harness pinouts before servicing powered hardware.**

The Pi hosts Flask and a local NetworkManager shared-mode Wi-Fi access point. Guests use a QR code and browser without venue internet. The mirror and phone pages are separate interfaces to shared application state. Guest visits persist independently of short mirror ownership.

Physical Canon SELPHY CP1500 printing requires an operator using Canon's phone app in the documented event configuration. A virtual CUPS PDF printer was used for development testing; CUPS integration is an alternate code path, not evidence of automatic SELPHY printing.
