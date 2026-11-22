# Security and privacy

**Publication:** the original uploaded file contained a fallback administrative PIN and a default Wi-Fi password. The published `src/booth20.py` substitutes local configuration/random PIN creation and a separate random admin cookie value. The actual device secrets have **not** been rotated automatically.

The published variant narrows access to `/fotos/<filename>`, but the application still needs a systematic authorization and CSRF review. Guest session tokens appear in route URLs and the original iOS recovery path can associate a visit with its client's IP; do not treat these as robust multi-user authentication. HTTP is local-only, not end-to-end encrypted.

Guest photographs and event runtime configuration must not be committed. Delete event media only after owner-approved backup and retention decisions. Before public release, test cross-session isolation, upload endpoints, admin permissions, physical network exposure and privacy handling.
