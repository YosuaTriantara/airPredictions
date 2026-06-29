# AIRA Frontend

Antarmuka web untuk **AIRA – Sistem Prediksi Kualitas Udara (AQI) di India**.
Dibangun dengan **Vue 3 + Vite**.

Frontend ini berisi 3 halaman:

| Halaman   | Route       | Isi |
|-----------|-------------|-----|
| Home      | `/`         | Hero, statistik, dan fitur utama sistem |
| Predict   | `/predict`  | Form prediksi AQI, kartu hasil dengan indikator paru-paru, grafik forecast, banner peringatan, dan kadar polutan |
| Histori   | `/histori`  | Tren AQI 24 jam terakhir & tren tahunan 2015–2020 |

> **Catatan data:**
> - Daftar stasiun di `src/data/stations.json` adalah **data asli** hasil ekstraksi
>   dari dataset (`stations.csv` — 230 stasiun / 127 kota / 21 provinsi). Field
>   metadata (id, name, city, state, status) nyata.
> - Nilai **AQI & polutan** masih **mock** (dihasilkan deterministik di
>   `src/data/stations.js` + `src/utils/chartData.js`). Saat backend FastAPI /
>   OpenAQ API siap, cukup ganti fungsi `mockMetrics()` & generator chart tanpa
>   mengubah komponen tampilan.

## Menjalankan

Butuh **Node.js 18+**.

```bash
cd frontend
npm install      # instal dependency
npm run dev      # jalankan dev server (http://localhost:5173)
```

## Build produksi

```bash
npm run build    # output ke folder dist/
npm run preview  # pratinjau hasil build
```

## Struktur

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── public/
│   └── favicon.svg
└── src/
    ├── main.js
    ├── App.vue
    ├── router/index.js
    ├── styles/main.css          # tema warna & gaya global
    ├── data/
    │   ├── stations.json        # 230 stasiun asli dari dataset (stations.csv)
    │   └── stations.js          # loader + metrik AQI/polutan (mock)
    ├── utils/
    │   ├── aqi.js               # kategori & logika AQI (skala CPCB India)
    │   └── chartData.js         # generator data grafik (mock)
    ├── components/
    │   ├── NavBar.vue
    │   ├── FooterBar.vue
    │   ├── BrandMark.vue        # logo AIRA (ikon angin)
    │   ├── HeroArt.vue          # ilustrasi awan + angin
    │   ├── LungsIcon.vue        # indikator kesehatan (paru-paru) berwarna sesuai AQI
    │   └── AreaChart.vue        # grafik area SVG kustom (tanpa dependensi)
    └── pages/
        ├── HomeView.vue
        ├── PredictView.vue
        └── HistoriView.vue
```

## Kategori AQI

Mengikuti skala **CPCB India** (sesuai dataset model):

| Kategori | Rentang | Warna |
|----------|---------|-------|
| Good          | 0–50    | hijau |
| Satisfactory  | 51–100  | hijau muda |
| Moderate      | 101–200 | kuning |
| Poor          | 201–300 | oranye |
| Very Poor     | 301–400 | merah |
| Severe        | 401+    | marun |

Indikator paru-paru pada halaman Predict ikut berubah warna mengikuti kategori
ini sebagai sinyal visual cepat terhadap dampak kesehatan.
