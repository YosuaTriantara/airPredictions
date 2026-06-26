# Dataset Validation Report

## Dataset

- File: `data/raw/station_hour.csv`
## Ukuran Dataset

- Jumlah Baris : **2,589,083**
- Jumlah Kolom : **16**

## Validasi Kolom Penting

- Datetime : Tersedia
- Tipe Datetime : `datetime64[ns]`
- AQI : Tersedia

## Fitur Polutan Utama

- PM2.5
- PM10
- NO
- NO2
- NOx
- NH3
- CO
- SO2
- O3
- Benzene
- Toluene
- Xylene

## Struktur Dataset

| Kolom | Tipe Data | Missing Value |
|-------|-----------|--------------:|
| StationId | object | 0 |
| Datetime | datetime64[ns] | 0 |
| PM2.5 | float64 | 647689 |
| PM10 | float64 | 1119252 |
| NO | float64 | 553711 |
| NO2 | float64 | 528973 |
| NOx | float64 | 490808 |
| NH3 | float64 | 1236618 |
| CO | float64 | 499302 |
| SO2 | float64 | 742737 |
| O3 | float64 | 725973 |
| Benzene | float64 | 861579 |
| Toluene | float64 | 1042366 |
| Xylene | float64 | 2075104 |
| AQI | float64 | 570190 |
| AQI_Bucket | object | 570190 |
