# Version 20 source review

The attached full source was inspected and a **sanitized derivative** was placed in `src/booth20.py`.

Confirmed source functionality includes Flask templates for kiosk, phone and admin; picamera2 still/preview modes; 15-second mirror ownership release; capture watchdog; NetworkManager AP integration, captive-portal probes; local print queue with 2×2 collages and manual Canon handoff.

## Targeted modifications

- Source-level default PIN and Wi-Fi password removed from public variant.
- Admin cookie separated from PIN.
- Direct access to JPEG photographs restricted by visit ownership/admin/local mirror use.
- Non-reentrant camera-lock reacquisition removed from the recovery path.

## Remaining limitations

- Camera construction/start is still module scoped, so loss of the camera can block web startup.
- In-memory queue, visits and pickup counter are not durable over restart.
- Approval in manual print mode marks a file ready; it is **not** proof the Canon printer output a physical page.
- Device-level security and end-to-end behavior need testing on actual hardware.
- The originally reported 293 tests were not included or rerun.
