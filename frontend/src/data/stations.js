// Daftar stasiun ASLI hasil ekstraksi dari dataset (archive stations.csv,
// 230 stasiun / 127 kota / 21 provinsi). Lihat stations.json.
//
// Field metadata (id, name, city, state, status) adalah data nyata dari dataset.
// Sedangkan baseAqi & pollutants di sini masih MOCK — dihasilkan deterministik
// dari id stasiun agar grafik konsisten. Saat backend FastAPI / OpenAQ API siap,
// cukup ganti `mockMetrics()` dengan pemanggilan API tanpa mengubah komponen UI.
import stationsRaw from './stations.json'

export const DEFAULT_STATION_ID = 'DL002' // Delhi – Anand Vihar (sesuai contoh)

export const HORIZONS = [6, 12, 24]

export const POLLUTANT_UNITS = {
  'PM2.5': 'µg/m³',
  PM10: 'µg/m³',
  NO2: 'µg/m³',
  CO: 'mg/m³',
}

// Override agar beberapa stasiun penting cocok dengan contoh tampilan.
const METRIC_OVERRIDES = {
  DL002: { baseAqi: 247, pollutants: { 'PM2.5': 142, PM10: 210, NO2: 52, CO: 1.4 } },
}

function hashId(str) {
  let h = 2166136261
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return h >>> 0
}

// Metrik mock deterministik dari id stasiun.
function mockMetrics(id) {
  if (METRIC_OVERRIDES[id]) return METRIC_OVERRIDES[id]
  const h = hashId(id)
  const bit = (n) => ((h >> n) & 0xff) / 255 // pseudo 0..1
  const baseAqi = 58 + (h % 286) // 58..343
  const pm25 = Math.max(8, Math.round(baseAqi * (0.55 + bit(3) * 0.15)))
  const pm10 = Math.max(12, Math.round(baseAqi * (0.8 + bit(5) * 0.25)))
  const no2 = Math.round(18 + bit(7) * 46)
  const co = Math.round((0.4 + baseAqi / 300 + bit(11) * 0.4) * 10) / 10
  return { baseAqi, pollutants: { 'PM2.5': pm25, PM10: pm10, NO2: no2, CO: co } }
}

export const STATIONS = stationsRaw.map((s) => ({
  ...s,
  ...mockMetrics(s.id),
}))

const stationIndex = new Map(STATIONS.map((s) => [s.id, s]))

export function getStationById(id) {
  return stationIndex.get(id) || stationIndex.get(DEFAULT_STATION_ID) || STATIONS[0]
}

// Dikelompokkan per provinsi untuk <optgroup> pada dropdown.
export const STATIONS_GROUPED = (() => {
  const groups = new Map()
  for (const s of STATIONS) {
    if (!groups.has(s.state)) groups.set(s.state, [])
    groups.get(s.state).push(s)
  }
  return [...groups.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([state, stations]) => ({ state, stations }))
})()
