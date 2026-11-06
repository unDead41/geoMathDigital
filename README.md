# GeoMath Digital

Portal web GeoMath untuk permainan geometri, kelas, Duel dan pembelajaran 3D.
Sumber utama ialah branch **`main`** dalam repository ini.

## Jalankan projek

Gunakan Node.js 22 dan buka terminal VS Code pada folder repository:

```powershell
Set-Location digital
npm ci
npm run verify
```

`verify` membina projek daripada sumber, menguji portal dan modul, menyediakan
entry penerbitan serta menyemak aset. Untuk membina sahaja: `npm run build`.
Buka `digital/artifacts/GeoDecoder_Digital_V2.html` untuk pakej offline selepas
binaan, atau jalankan pelayan statik bagi `digital/artifacts/pwa/` untuk PWA.

## Struktur dan branch

| Lokasi | Pemilikan |
| --- | --- |
| `digital/dist/` | Modul JS/CSS dan template portal yang disunting; `app.bundle.js` ialah hasil build |
| `digital/module/src/` | Geometri, 11 model, makmal, nota dan studio pembelajaran |
| `digital/assets/` | Audio dan ikon asal bersama manifest checksum |
| `digital/design-system/` | Satu sumber token dan komponen reka bentuk |
| `digital/vendor/` | Modul pembelajaran yang dipin dan provenance |
| `digital/backend/`, `supabase/` | Backend, kontrak dan sejarah migration |
| `digital/docs/` | Panduan, konsep UI/UX dan bukti mengikut konteks |
| `docs/archive/` | Rekod pemisahan repository terdahulu |

Branch aktif selepas pembersihan: `main` untuk sumber dan `main-digitalized`
untuk snapshot Pages. Branch lama disimpan dalam tag arkib yang disenaraikan
dalam [laporan pembersihan](digital/docs/maintenance/CLEANUP.md).

Laman semasa: [GeoMath Digital](https://undead41.github.io/geoMathDigital/).
Sumber binaan bersih dan snapshot Pages mempunyai kitaran penerbitan berasingan;
lihat [panduan penerbitan](docs/DIGITAL_PUBLISHING.md).

## Panduan

- [Panduan Digital](digital/README.md)
- [Aset dan hasil build](digital/assets/README.md)
- [Kontrak UX](digital/UX-CONTRACT.md)
- [Backend](digital/backend/README.md)
- [Pemisahan repository](docs/REPOSITORY_SPLIT.md)

Firmware berada di [geoMathPhysical](https://github.com/unDead41/geoMathPhysical),
manakala aplikasi Flutter berada di [geoMathApp](https://github.com/unDead41/geoMathApp).
