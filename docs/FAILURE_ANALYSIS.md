# Camera failure diagnosis

About 48 hours before the November 2026 event, Chrome displayed `ERR_CONNECTION_REFUSED` because the Flask service failed during module-scope camera initialization. `systemctl` showed repeated restarts; `journalctl` identified `RuntimeError: No camera number 0 found`. After accounting for libcamera exclusive access, `dmesg` showed an IMX708 chip-ID read failure (`-5 / EIO`). Replacing the flex cable did not resolve it, while replacing the camera module restored operation.

Two faults must be separated: a hardware sensor/communication failure, and the application coupling that let a camera fault prevent the web server from starting. A graceful degraded mode remains pending.
