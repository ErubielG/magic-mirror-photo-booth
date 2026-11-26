# System architecture

The 40-inch LCD panel is driven by an M.NT68676.3 LVDS controller replacing the original MIR63A0 board. Raspberry Pi 4 supplies HDMI video; a Sony IMX708 connects over CSI-2. The existing MEGMEET PSU supplies 12 V to the controller and 24 V to the backlight; a buck converter provides 5 V for the Pi. **Verify all actual harness pinouts before servicing powered hardware.**

The Pi hosts Flask and a local NetworkManager shared-mode Wi-Fi access point. Guests use a QR code and browser without venue internet. The mirror and phone pages are separate interfaces to shared application state. Guest visits persist independently of short mirror ownership.

**Print architecture has two distinct paths.** At the November 14 event, guests requested one vertical 4×6-inch sheet containing up to four selected images through the captive portal. The booth composed and queued the sheet; an operator approved it in `/admin`, downloaded the composed file to a phone, and printed it over Wi-Fi using the Canon SELPHY app and CP1500. The Raspberry Pi did **not** send a print job directly to the CP1500. Separately, the software implements automatic sequential CUPS (`lp`) dispatch to a configured queue; during development this path was tested using `cups-pdf`, a virtual PDF printer, not a physical CP1500.

At the November 14 event, printing used the operator's phone as the bridge between the booth and CP1500. A precise phone/printer Wi-Fi association record was not preserved; the CP1500 may have joined the booth's guest network. The author recalls depletion of approximately 30–40 photo sheets; this is not a measured count of successful prints. Do not describe the event as direct CUPS-to-CP1500 printing.
