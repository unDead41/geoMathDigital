# GeoMath repository separation — 6 November 2026

Goal: keep ESP32, web/backend and Flutter development in three independent repositories.

- [x] Record all source branches and exact commits in `sources.json`.
- [x] Confirm Physical `main` already contains only firmware and its resources.
- [x] Review App UI/UX and AI divergence; verify the two overlapping Dart files merge cleanly.
- [x] Filter App history to Flutter code and App planning documents; preserve original feature branches and merge both latest feature heads.
- [x] Filter Digital history to the web portal, backend and its publishing assets; preserve feature branches.
- [x] Run the existing platform checks before publishing the assembled default branches.
- [x] Verify remote trees and branch maps, then archive the original mixed references and remove the migrated active branches from Physical with exact leases.
- [x] Update Physical versioned documentation, preserve `sharing`, and verify the three remote default branches.

Keep established source paths so build scripts, contracts and existing tests remain valid. App's bundled offline assets stay in App; the deployed Supabase backend and its source stay under Digital. Historical canonical SHA references remain provenance. Backend and Pages deployment settings are outside this source-only migration.

Review focus: no lost AI/UI changes; no firmware in App/Digital; no live web source in App; no dropped assets; no branch deletion before destination verification; no overwrite of a branch advanced by another session.

## Completion evidence

- Physical main: `4189dade7544f9e72d015ea18c738c3dac716bf7`, v2.0.3. Scope/version/native RGB checks passed; 79 integration cases plus the existing core/version suites.
- Physical sharing: `f05f266d7c0a941329f0e39cc4202fcecd7efabc`, 2.0.3-sharing.1. All firmware/entry blobs match main; updated text checksums and source SHA are retained.
- Verified Digital source: `8655dd17ffa693cd1e2df52c791c136fa6adeb2e`, v2.10.0. 541 tests, standalone build, publication preparation and static checks passed.
- Verified App source: `16e3e647c58aefbfc91f4ca8df7525cc0ad072ec`, 0.2.0+2. 674 Flutter tests passed (18 optional capture tests skipped), 60 Node contracts passed, Python tooling suites passed, analyzer/format passed and Android debug APK compiled.
- 31 Digital and 6 App feature branches are present in their respective repositories with platform-filtered history.
- All 37 migrated branches were retired from Physical only after destination verification and archive creation. Seven Physical branches remain.
- Original history is retained by `archive/mixed-before-20261106` at `33d3c37480d2d4d1bdeb6d9c3c206087937b8bff`.
- This completion update changes documentation only. No device run, hosted backend change or Pages publication is claimed.

Verification runs: [Physical](https://github.com/unDead41/geoMathPhysical/actions/runs/42200595389), [Digital](https://github.com/unDead41/geoMathDigital/actions/runs/42199903534), [App](https://github.com/unDead41/geoMathApp/actions/runs/42200158147), [branch retirement](https://github.com/unDead41/geoMathPhysical/actions/runs/42201797718).
