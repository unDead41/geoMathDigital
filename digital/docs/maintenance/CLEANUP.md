# Digital consolidation and cleanup

The 6 November 2026 cleanup consolidates the remaining UI/UX concept reference, moves original media to `digital/assets/`, and regenerates build output from source.

The active source is `main`. The existing `main-digitalized` Pages snapshot is retained. Other original branches are mapped in `CLEANUP.json` and preserved by [`archive/digital-before-cleanup-20261106`](https://github.com/unDead41/geoMathDigital/tree/archive/digital-before-cleanup-20261106).

Source JavaScript, CSS, geometry, backend SQL, email templates and the current reviewed module preserve their original bytes. Historical evidence remains attached to its original report; equal bytes in those records do not imply an unused runtime asset.

Run `npm ci` and `npm run verify` from `digital/`. The build creates the portal, module, media copies, PWA and compatibility HTML aliases. Those outputs are ignored on main; the current module pin and deployment email templates remain reviewed source inputs.

To restore an old branch, fetch the archive tag and create a new review branch from its recorded SHA. Rebase or port only the needed source change onto current main. Original branch names are historical; they do not become active again automatically.
