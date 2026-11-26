# Version 20 source review

The attached full source was inspected and a **sanitized derivative** was placed in `src/booth20.py`.

Confirmed source functionality includes Flask templates for kiosk, phone and admin; picamera2 still/preview modes; 15-second mirror ownership release; capture watchdog; NetworkManager AP integration, captive-portal probes; local print queue with 2×2 collages, sequential automatic CUPS dispatch, optional operator approval/rejection and manual Canon fallback.

## Targeted modifications

- Source-level default PIN and Wi-Fi password removed from public variant.
- Admin cookie separated from PIN.
- Direct access to JPEG photographs restricted by visit ownership/admin/local mirror use.
- Non-reentrant camera-lock reacquisition removed from the recovery path.

## Remaining limitations

- Camera construction/start is still module scoped, so loss of the camera can block web startup.
- In-memory queue, visits and pickup counter are not durable over restart.
- The source supports unattended printing through a configured CUPS queue when operator approval and manual mode are disabled. In manual print mode, approval marks a sheet ready for separate physical printing; neither that status nor a successful `lp` call alone proves a sheet was physically delivered.
- At the event, booth20 operated with manual printing and per-sheet approval disabled. The Raspberry Pi submitted sheets using Linux CUPS (`lp -d selphy`) over the PhotoBooth Wi-Fi network to the connected Canon SELPHY CP1500. No operator phone or manual print approval was involved. Reported paper depletion is approximate, not a print-total metric.
- Device-level security and end-to-end behavior need testing on actual hardware.
- The originally reported 293 tests were not included or rerun.
