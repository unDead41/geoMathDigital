# geoMathDigital

GeoMath: web portal, browser game, 3D learning modules, PWA assets and Supabase backend source.

| Repository | Scope |
| --- | --- |
| [geoMathPhysical](https://github.com/unDead41/geoMathPhysical) | ESP32, RFID, LCD, wiring, printable resources |
| [geoMathDigital](https://github.com/unDead41/geoMathDigital) | Web portal, browser game, learning and backend |
| [geoMathApp](https://github.com/unDead41/geoMathApp) | Flutter app, Android, AI and offline assets |

## Run locally

```powershell
git clone https://github.com/unDead41/geoMathDigital.git
Set-Location geoMathDigital/digital
npm ci
npm test
npm run build
npm run prepare:pages
npm run check
```

The root `index.html` is the generated standalone entry. The complete editable portal is in `digital/`; Supabase migrations remain at `supabase/`. Existing Pages branches are retained as deployment snapshots. No hosted backend or Pages deployment is performed by this source migration.

## Source ownership

`main` is the development integration branch of **geoMathDigital**. Every feature branch in this repository must contain only this platform. Read `AGENTS.md` and `docs/REPOSITORY_SPLIT.md` before editing. The original source layout is retained so existing build/test paths work.

Historical documents and canonical SHA locks describe their original snapshots; they do not authorize development in another repository. Filtered feature history and exact original-to-new branch mappings are recorded in `migration/receipt.json`.
