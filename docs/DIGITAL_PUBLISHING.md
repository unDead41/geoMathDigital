# Penerbitan GeoMath Digital

Repository sumber: `unDead41/geoMathDigital`, branch `main`.
Sumber dibina dengan Node.js 22 dan dependency dalam `digital/package-lock.json`.

```powershell
Set-Location digital
npm ci
npm run verify
```

| Hasil build | Kegunaan |
| --- | --- |
| `digital/artifacts/GeoDecoder_Digital_V2.html` | Satu fail offline lengkap dengan audio dan modul |
| `digital/artifacts/pwa/` | Folder deploy lengkap: HTML, worker, manifest, ikon dan audio |
| `digital/module/GeoDecoder_Modul_V1.html` | Modul standalone yang dijana daripada sumber modul |
| `index.html` dan `.nojekyll` di akar | Entry offline terjana oleh `prepare:pages`, diabaikan Git pada branch sumber |

Pakej PWA mesti disalin secara lengkap apabila diterbitkan. Media asal berada
di `digital/assets/`; salinan output dan alias HTML dijana semula setiap build.

## Pages yang sedang digunakan

Tetapan disemak pada 6 November 2026: **Deploy from a branch**,
**`main-digitalized`**, **`/(root)`**.
URL: [GeoMath Digital](https://undead41.github.io/geoMathDigital/).
Snapshot disimpan pada commit `287155b5414a38e57d722446616228569b1ede68`
(penerbitan v2.10.0). Pembersihan source tidak menerbitkan snapshot baharu.

Kemas kini Pages dilakukan berasingan daripada push source, selepas pengesahan
dan kebenaran penerbitan. Backend/Edge Function dan migration juga mempunyai
aliran deploy berasingan. `npm run prepare:pages` hanya menyediakan fail lokal.

## Sejarah

Rekod penerbitan lama kekal dalam Git melalui tag
`archive/digital-before-cleanup-20261106`. Padanan branch, fail yang dikeluarkan
dan fingerprint aset terdapat dalam `digital/docs/maintenance/`.
