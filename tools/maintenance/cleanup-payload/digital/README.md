# GeoMath Digital — pembangunan

Sumber semasa: `unDead41/geoMathDigital`, branch `main`. Mulakan daripada
[README repository](../README.md) dan `AGENTS.md`.

Portal mengandungi kuiz 10 soalan, latihan 15 soalan, pasangan bongkah R1 dan
bentangan R2, Duel protocol 2, akaun e-mel/Google, kelas guru/pelajar, profil,
11 model pembelajaran, makmal dan studio. PWA menyediakan cache offline serta
outbox rekod yang dihantar apabila sambungan kembali. Kelas, akaun dan Duel
menggunakan backend online.

```powershell
npm ci
npm run verify
```

`npm test` membina keperluan ujian melalui `pretest`. `npm run test:module`
menjalankan suite modul. `npm run check` menyemak HTML standalone, pin modul,
token dan parity media. Semua dependency dikunci dalam `package-lock.json`.

## Aset dan output

Edit media dalam `assets/` dan token dalam `design-system/`. Folder `dist/`
mengekalkan nama asal bagi kod portal yang disunting; hanya fail bundle,
adapter terjana dan salinan media dikecualikan daripada Git.

Selepas build, fail offline canonical ialah
`artifacts/GeoDecoder_Digital_V2.html`; alias nama V1/V2 dijana untuk keserasian.
Pakej PWA lengkap berada dalam `artifacts/pwa/`. Modul standalone terjana ialah
`module/GeoDecoder_Modul_V1.html`. Rujukan komponen terjana ialah
`artifacts/GeoDecoder_Design_System.html`.

Panduan terperinci: [manifest media](assets/README.md),
[design system](docs/DESIGN_SYSTEM.md), [kontrak UX](UX-CONTRACT.md),
[modul](module/README.md), [backend](backend/README.md),
[pembersihan](docs/maintenance/CLEANUP.md) dan
[penerbitan](../docs/DIGITAL_PUBLISHING.md).

README dan penerbitan terdahulu boleh dibaca melalui tag
`archive/digital-before-cleanup-20261106`. Bukti sejarah mengekalkan tarikh,
versi dan sumber asalnya.
