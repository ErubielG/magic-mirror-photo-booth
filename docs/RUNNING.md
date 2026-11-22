# Running (Raspberry Pi only)

The source depends on Linux interfaces, Raspberry Pi `picamera2`/libcamera, Flask, Pillow and qrcode. It cannot be expected to run on an ordinary desktop computer without a mock camera.

Typical Python environment:

```bash
python3 -m venv --system-site-packages ~/booth-venv
~/booth-venv/bin/pip install flask 'qrcode[pil]'
~/booth-venv/bin/python src/booth20.py
```

Configure NetworkManager shared-mode AP, systemd service, and Chromium kiosk separately. Ensure Wi-Fi credentials correspond to the actual AP configuration; application QR settings alone do not configure NetworkManager.

**Do not deploy this published derivative onto the event Pi without saving the original and performing a dry-run.** Its authentication and camera-lock behavior changed during sanitization.
