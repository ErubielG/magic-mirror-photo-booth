# Version 20 application

`booth20.py` is a **sanitized derivative** of the actual full version 20 Python source, not a rewrite or stub. Its large embedded HTML/CSS/JavaScript templates implement the guest phone interface, mirror kiosk, and admin console.

## Raspberry Pi dependencies

Use Raspberry Pi OS with system-provided `picamera2` and libcamera. Install Flask, Pillow and qrcode in a `--system-site-packages` virtual environment. NetworkManager AP and captive-portal configuration are separate from Python.

## Important

The original deployment used a different credential configuration. The published variant generates or loads a local PIN and has targeted security/lock changes. **Do not replace the live application without backing up and testing.**

See [running instructions](../docs/RUNNING.md), [security](../docs/SECURITY.md), and [source review](../docs/BOOTH20_SOURCE_REVIEW.md).
