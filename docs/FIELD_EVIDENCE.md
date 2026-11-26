# Field evidence — November 2026

## Purpose

Four selected, consent-cleared photographs are now published in [the gallery](../assets/GALLERY.md). The images document a working prototype at an event and in mobile-interface testing. The full private event photo archive remains excluded. Separately from the photographs, the live event account records autonomous guest-requested printing: booth20 sent completed 4×6-inch sheets via CUPS (`lp -d selphy`) over the PhotoBooth Wi-Fi network to a Canon SELPHY CP1500 without manual approval or phone-based intervention. Approximate depletion of 30–40 photo sheets is an observational estimate, not a printer-confirmed successful print count.

## Evidence matrix

| Supplied photo | Visible evidence | What it supports | What it does not establish |
| --- | --- | --- | --- |
| Two finished event photos featuring the same two guests | Camera-generated frames with event caption bar | Actual image composition and multiple distinct captures | Total number of captures, image quality statistics, permission to publish |
| Person standing in front of the installed mirror at the party | Mirror in use at the event with other people nearby | Physical deployment and real guest interaction | Exact uptime, number of unique sessions |
| Photo of mirror running in a room during preparation | Full-height display with text, QR and mirror reflection | Integration of display, enclosure and on-screen onboarding | On-site concurrency, network stability, or security of visible QR |
| Framed portrait captured during setup | Result image with event-specific caption and framing | Real captured file and compositing output | Measured optical performance or total field capture volume |
| iPhone captive-portal photo viewer | Real handset displaying a photograph with save instructions | iOS browser viewer workflow was rendered on a phone | Successful save in every iOS version or secure file isolation |
| iPhone print-sheet selection dialog | Real handset showing up-to-four-photo selection | Mobile print-selection interface was present and usable as a visual flow | A sheet physically printed or was delivered to the guest |

## Time-limited engineering integration

The project's software was written remotely while the hardware was in California; the final days before the fixed-date event were used for physical integration, hardware diagnosis, and commissioning. The trade-off to retain a large integrated script should be evaluated with that context. See [engineering decisions](ENGINEERING_DECISIONS.md).

## What real operation contributes

The author's observation that guests used capture/download over the course of the evening is meaningful field evidence. A several-hour period of operation is different from a 12-second synthetic load simulation and should be recorded separately. Without logged service uptime, exact hours and error rates must not be inferred from the photos.

The original development records describe 293 automated checks, rendering checks and a load simulation on a different machine. Those are development-verification evidence, not direct field-use measurements.

## Further evidence to add

- A close-up photograph of the internal hardware and connections, with any private details reviewed
- A short video showing Wi-Fi connection, photo capture, guest gallery, and direct automatic CUPS printing to the CP1500; distinguish optional approval/manual modes from the event configuration
- Time range of event operation, clearly labeled as observed or derived from logs
- Distinct capture count from retained JPEG files, avoiding double-counting original and composited copies
- Print requests and physically completed print sheets, recorded as separate metrics

## Privacy

The author confirmed permission to publish the selected images of themselves and their family. No Wi-Fi connection QR image was included in the approved public gallery. Future media additions should undergo the same permission and credential review.
