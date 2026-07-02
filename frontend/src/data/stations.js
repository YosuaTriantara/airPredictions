// Konstanta terkait tampilan AQI/polutan. Daftar stasiun & metriknya sudah
// TIDAK di-mock lagi di sini — diambil langsung dari backend FastAPI lewat
// `src/composables/useStations.js` (daftar stasiun) dan `src/services/api.js`
// (pengukuran & prediksi).
export const HORIZONS = [6, 12, 24]

export const POLLUTANT_UNITS = {
  'PM2.5': 'µg/m³',
  PM10: 'µg/m³',
  NO2: 'µg/m³',
  CO: 'mg/m³',
  NO: 'µg/m³',
  NOx: 'µg/m³',
  SO2: 'µg/m³',
  O3: 'µg/m³',
}
