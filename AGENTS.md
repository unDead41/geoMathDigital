# geoMathDigital contributor guidance

- This repository owns web portal, browser game, 3D learning modules, PWA assets and Supabase backend source. Its `main` branch is this platform.
- Firmware, GPIO, RFID, LCD, UID/NVS, wiring and printable hardware resources belong only to `unDead41/geoMathPhysical`.
- Flutter/Dart source and Android projects belong only to `unDead41/geoMathApp`. Do not copy its application into this repo.
- Portal source stays under `digital/`. The source tree includes its existing dist modules, build tools and assets. Preserve 11 learning models, formulas, card roles, Duel protocol and offline sync.
- This repository owns shared Supabase schema, migrations and Edge Function source. App consumes its public versioned API. Never duplicate schema ownership in the App repository.
- Run existing Node tests, build, publication preparation and static checks. Source pushes do not imply backend deployment or Pages publication. Obtain authorization for those operations.
- Check working tree and remote branch before editing. Preserve unrelated work; use explicit refs and do not force-push.
- Run `python3 tools/check_repository_scope.py` before publication. Never import the mixed repository tree or merge another platform.
- These instructions supersede historical monorepo branch/path assumptions in archived planning/handoff documents. New work must use the repository named above and its current `main`.
