# GeoMath repository ownership

Effective 6 November 2026.

- `geoMathPhysical`: firmware and physical learning hardware.
- `geoMathDigital`: portal, browser game, web modules, PWA and backend.
- `geoMathApp`: Flutter application and its bundled offline modules.

Each repository is independently editable and buildable. Sharing a public backend API does not require sharing a source checkout. App bundle provenance and historical source locks retain their original hashes. Rebuilding an exported bundle is an explicit pinned-source maintenance operation, separate from normal Flutter build/test.

Paths inside filtered history are intentionally retained. Original and filtered branch hashes appear in `migration/receipt.json`. Only platform-owned paths survive history filtering. Original mixed refs must be archived before their active Physical branches are retired. No source history on the original server is force-rewritten.

Do not follow historical prompts that identify firmware `main`, `geodecoder` or a Pages mirror as the current source owner. Use the ownership list above. Production deployment is unchanged.
