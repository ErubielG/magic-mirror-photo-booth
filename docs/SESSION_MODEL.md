# Session model

Mirror ownership and a phone's gallery visit are independent. A person acquires the mirror only when requesting a capture; it is released following the configured 15-second inactivity window. Their visit remains active for roughly 20 minutes, allowing gallery browsing and print-sheet requests as another guest uses the mirror.

The version 20 implementation also has a 20-second capture/countdown watchdog. Late captures should be delivered to the original visit without re-acquiring the mirror.

**Known limitation:** while a guest still owns the mirror, download, discard and print actions can reset its inactivity clock. Moving photo-only operations outside the ownership clock is a future improvement. State, queue and visit mappings are in process memory and can be lost at restart.
