# Canonical media

`audio/menu.mp3`, `audio/map.mp3` and `icons/icon.svg` are the original runtime
media. `manifest.json` locks their original bytes, SHA-256 and Git blob hashes.
The audio is user-supplied; its full tracks are retained.

`npm run build` creates development copies in `dist/assets/` and deployment
copies in `artifacts/pwa/`. Those copies are ignored by Git. Edit or replace
an original here deliberately, update its manifest fingerprint, then run the
asset tests. Never edit a generated media copy.

Teaching illustrations are rendered from the existing geometry modules.
Concept images live in `docs/uiux-redesign-concept/images/`; historical capture
evidence stays with its original report. The reviewed offline learning module
is pinned separately by `vendor/module-release.json`.
