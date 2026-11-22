# Publication checklist

- [x] Sanitized version 20 application included in `src/booth20.py`.
- [x] Embedded default PIN and Wi-Fi password removed from the published variant.
- [x] Admin session cookie no longer contains the PIN.
- [x] Nested camera lock problem addressed in the published variant.
- [x] Anonymous direct JPEG access narrowed.
- [ ] Rotate actual PIN and Wi-Fi credentials on the deployed Raspberry Pi.
- [ ] Verify changed source on the physical hardware before deploying.
- [ ] Obtain guest consent before uploading photographs.
- [ ] Publish original 293-test suite after reviewing it for private data.
- [ ] Test remaining guest/session permissions, CSRF, and iOS IP-based fallback.
- [ ] Make a verified image backup of the Raspberry Pi.
- [ ] Decide whether to add an open-source license.

**This repository is documentation and a sanitized derivative, not a guaranteed drop-in replacement of the field-deployed system.**
