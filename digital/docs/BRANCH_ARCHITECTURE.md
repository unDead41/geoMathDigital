# GeoMath Digital branches

| Branch | Role |
| --- | --- |
| `main` | Editable source, canonical original assets, tests and backend contracts |
| `main-digitalized` | Existing GitHub Pages snapshot; keep its current commit until an authorized publication |

Create a short-lived `feature/...`, `fix/...` or `chore/...` branch from current
`main` for new work. Verify the source, integrate the change, then retire its
temporary branch. Firmware and Flutter changes belong in their own repositories.

The 33 original non-primary branches were either already integrated, legacy
publication snapshots, or the single UI/UX concept commit consolidated during
cleanup. Their exact heads are in `maintenance/CLEANUP.json` and retained by
`archive/digital-before-cleanup-20261106` before retirement.

`branch-registry.json` now identifies only this repository, protects the two
active branches and has an empty rename plan. The existing rename utility
remains opt-in, defaults to dry run and verifies exact source/destination refs;
it cannot target the former Physical repository.

Historical repository split records live at
`../../docs/archive/repository-split-20261106/`. A restored historical branch
must be reviewed against current `main`; it does not become a new source owner.
