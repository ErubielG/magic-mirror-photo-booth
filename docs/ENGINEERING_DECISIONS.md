# Engineering decisions under a fixed event deadline

## Context

The software was developed remotely in Mazatlán while the original fitness mirror was physically located in California. Final physical integration and troubleshooting happened only a few days before a scheduled November 14, 2026 event. The deadline was not movable: the unit had to be usable by unfamiliar guests on that date.

This created a different risk profile from a product developed over a long roadmap. The immediate engineering objective was to establish a reliable end-to-end workflow under time and hardware-access constraints.

## Why the application remained a single Python file

The version 20 application contains roughly 6,000 lines, including Python logic and embedded HTML/CSS/JavaScript templates. It is monolithic. This increases coupling, complicates testing, and makes later changes harder to reason about.

A major refactor in the final days before the event could have introduced unverified regressions across the camera, Flask service, captive portal, guest sessions, printing, and kiosk display. Preserving the integrated, tested implementation was a pragmatic **short-term risk decision**, not an endorsement of the architecture as ideal.

## What was prioritized

1. Make the replacement LVDS controller, Raspberry Pi, camera, and power wiring work together.
2. Keep photo capture and retrieval usable for event guests with no app installation.
3. Separate short mirror ownership from longer-lived guest galleries to avoid unnecessary queueing.
4. Provide practical workarounds for mobile captive-portal behavior.
5. Support autonomous guest-initiated printing: one vertical 4×6-inch sheet containing up to four images per session, serial print dispatch, optional operator approval/rejection, and a separate manual fallback when required by the printer setup.
6. Recover from the sensor failure discovered during on-site commissioning and meet the event date.

## Known technical debt and lessons

- **Module-scope camera startup:** an IMX708 failure can prevent the server from binding. A degraded startup mode remains a priority.
- **Large monolithic source:** camera handling, state transitions, routing, HTML/CSS/JS templates, print work, and administration should be split after behavior is captured in tests.
- **Volatile state:** visits, pickup numbers, and print queue are largely in memory.
- **Session and security review:** photo access, guest identity and local admin actions require stronger review.
- **Operations data:** structured, durable capture and print-outcome logs are not yet available for the event.

## Low-risk modularization plan

First preserve the currently deployed image and capture the working interfaces in integration tests. Then extract one responsibility at a time: configuration; image processing and sheet composition; session-state machine; print queue; camera adapter; network probes; API routes; and browser templates/static assets. Preserve public endpoints and event behavior while validating each extraction on physical hardware.

The engineering claim is **not** “6,000 lines in one file is good architecture.” It is “under the final integration deadline, the developer prioritized a working system and accepted documented technical debt, then identified a safer modernization sequence.”

## Evidence boundaries

The photographs and deployment narrative document physical integration, actual images and real guest use. They do not measure uptime, confirmed print count, or total captures. See [field evidence](FIELD_EVIDENCE.md) and [testing](TESTING.md).
