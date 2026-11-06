# GeoMath repository separation — 6 November 2026

Goal: keep ESP32, web/backend and Flutter development in three independent repositories.

- [x] Record all source branches and exact commits in `sources.json`.
- [x] Confirm Physical `main` already contains only firmware and its resources.
- [x] Review App UI/UX and AI divergence; verify the two overlapping Dart files merge cleanly.
- [ ] Filter App history to Flutter code and App planning documents; preserve original feature branches and merge both latest feature heads.
- [ ] Filter Digital history to the web portal, backend and its publishing assets; preserve feature branches.
- [ ] Run the existing platform checks before publishing the assembled default branches.
- [ ] Verify remote trees and branch maps, then archive the original mixed references and remove the migrated active branches from Physical with exact leases.
- [ ] Update Physical versioned documentation, preserve `sharing`, and verify the three remote default branches.

Keep established source paths so build scripts, contracts and existing tests remain valid. App's bundled offline assets stay in App; the deployed Supabase backend and its source stay under Digital. Historical canonical SHA references remain provenance. Backend and Pages deployment settings are outside this source-only migration.

Review focus: no lost AI/UI changes; no firmware in App/Digital; no live web source in App; no dropped assets; no branch deletion before destination verification; no overwrite of a branch advanced by another session.
