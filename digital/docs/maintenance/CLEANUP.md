# Digital consolidation and cleanup

The 6 November 2026 cleanup consolidates the remaining UI/UX concept reference, moves original media to `digital/assets/`, and regenerates build output from source.

The active source is `main`. The existing `main-digitalized` Pages snapshot is retained. Other original branches are mapped in `CLEANUP.json` and preserved by [`archive/digital-before-cleanup-20261106`](https://github.com/unDead41/geoMathDigital/tree/archive/digital-before-cleanup-20261106).

Source JavaScript, CSS, geometry, backend SQL, email templates and the current reviewed module preserve their original bytes. Historical evidence remains attached to its original report; equal bytes in those records do not imply an unused runtime asset.

Run `npm ci` and `npm run verify` from `digital/`. The build creates the portal, module, media copies, PWA and compatibility HTML aliases. Those outputs are ignored on main; the current module pin and deployment email templates remain reviewed source inputs.

To restore an old branch, fetch the archive tag and create a new review branch from its recorded SHA. Rebase or port only the needed source change onto current main. Original branch names are historical; they do not become active again automatically.

## Completion record

Cleanup is complete on 6 November 2026. The 35 original branches are now two active branches: `main` for source and `main-digitalized` for the existing Pages snapshot. The 33 consolidated original branches and three temporary audit/preparation branches were retired after exact-head and archive checks. The temporary histories are retained under [`archive/digital-cleanup-preparation-20261106`](https://github.com/unDead41/geoMathDigital/tree/archive/digital-cleanup-preparation-20261106).

[Clean-checkout verification](https://github.com/unDead41/geoMathDigital/actions/runs/42208690114) passed on source commit `7143ee89aaf08b04bf202f249b6d6873b4a32e69`: 543 portal tests and 341 module tests, with zero failures. Source scope, media parity, the module pin, publication preparation and a clean post-build Git diff also passed. [Branch retirement](https://github.com/unDead41/geoMathDigital/actions/runs/42209216607) completed successfully.

At that verified source commit, tracked files total 93,284,945 bytes, compared with 144,402,286 bytes before cleanup. These are working-tree source sizes; archived Git history is preserved. All 173 protected runtime/backend blobs and the three original media blobs retain their original identities. The Pages branch remains at `287155b5414a38e57d722446616228569b1ede68`.
