# System architecture

The 40-inch LCD panel is driven by an M.NT68676.3 LVDS controller replacing the original MIR63A0 board. Raspberry Pi 4 supplies HDMI video; a Sony IMX708 connects over CSI-2. The existing MEGMEET PSU supplies 12 V to the controller and 24 V to the backlight; a buck converter provides 5 V for the Pi. **Verify all actual harness pinouts before servicing powered hardware.**

The Pi hosts Flask and a local NetworkManager shared-mode Wi-Fi access point. Guests use a QR code and browser without venue internet. The mirror and phone pages are separate interfaces to shared application state. Guest visits persist independently of short mirror ownership.

Printing is **not limited to an operator-assisted workflow**: each guest visit can request one vertical 4×6-inch sheet containing up to four selected images. The application creates a print job, queues jobs sequentially, and can dispatch them automatically through CUPS (`lp`) when a compatible queue is configured and optional operator approval is disabled. The operator can instead enable approval/rejection of jobs. A separate manual mode supports downloading a sheet and printing through Canon's phone app when the printer is not attached to CUPS.

At the November 14 event, the author reports guest-initiated physical printing and depletion of approximately 30–40 sheets of photo paper. The exact printer transport/configuration used at that event is not preserved in this repository, so the implemented CUPS path should not be represented as independently verified with the SELPHY CP1500.
