import { HORIZONS } from '../data/stations.js'

// Generator pseudo-acak deterministik agar grafik konsisten setiap render
// untuk stasiun yang sama (tidak berubah-ubah saat komponen re-render).
function seeded(seed) {
  let s = seed % 2147483647
  if (s <= 0) s += 2147483646
  return () => {
    s = (s * 16807) % 2147483647
    return (s - 1) / 2147483646
  }
}

function hashString(str) {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = (h * 31 + str.charCodeAt(i)) % 2147483647
  }
  return h
}

function clamp(v, min, max) {
  return Math.min(max, Math.max(min, v))
}

// Tren AQI 24 jam terakhir: pola harian dengan dua puncak (pagi & malam) + noise.
export function generate24h(station) {
  const rand = seeded(hashString(station.id) + 7)
  const base = station.baseAqi
  const points = []
  const labels = []
  for (let h = 1; h <= 24; h++) {
    const morning = Math.exp(-Math.pow((h - 8) / 3, 2))
    const evening = Math.exp(-Math.pow((h - 20) / 3, 2))
    const daily = 0.55 + 0.45 * (morning + evening)
    const noise = (rand() - 0.5) * 0.18
    const value = clamp(base * (daily + noise), 8, base * 1.25)
    points.push(Math.round(value))
    labels.push(String(h))
  }
  return { labels, data: points }
}

// Tren AQI tahunan 2015-2020: tren naik bertahap dengan sedikit variasi.
export function generateYearly(station) {
  const rand = seeded(hashString(station.id) + 19)
  const years = [2015, 2016, 2017, 2018, 2019, 2020]
  const start = station.baseAqi * 0.55
  const end = station.baseAqi * 1.05
  const data = years.map((_, i) => {
    const t = i / (years.length - 1)
    // kurva-S agar terlihat alami
    const smooth = t * t * (3 - 2 * t)
    const noise = (rand() - 0.5) * 0.08 * station.baseAqi
    return Math.round(clamp(start + (end - start) * smooth + noise, 20, 500))
  })
  return { labels: years.map(String), data }
}

// Prediksi nilai AQI untuk horizon tertentu (6/12/24 jam).
export function predictAqi(station, horizon) {
  const factor = { 6: 0.92, 12: 1.0, 24: 1.08 }[horizon] ?? 1
  return Math.round(station.baseAqi * factor)
}

// Forecast AQI ke depan: dari kondisi sekarang naik menuju nilai prediksi.
export function generateForecast(station, horizon) {
  const rand = seeded(hashString(station.id) + horizon)
  const target = predictAqi(station, horizon)
  const startVal = target * 0.62
  const steps = horizon // titik per jam
  const data = []
  const labels = []
  for (let i = 0; i <= steps; i++) {
    const t = i / steps
    const smooth = Math.pow(t, 1.15)
    const noise = i === 0 || i === steps ? 0 : (rand() - 0.5) * 0.05 * target
    data.push(Math.round(startVal + (target - startVal) * smooth + noise))
    labels.push(labelForStep(i, steps, horizon))
  }
  return { labels, data, target }
}

function labelForStep(i, steps, horizon) {
  if (i === 0) return 'Now'
  if (i === steps) return `+${horizon} Jam`
  // tampilkan label di sepertiga & dua-pertiga
  const third = Math.round(steps / 3)
  const twoThird = Math.round((2 * steps) / 3)
  if (i === third) return `+${Math.round(horizon / 3)} Jam`
  if (i === twoThird) return `+${Math.round((2 * horizon) / 3)} Jam`
  return ''
}

export { HORIZONS }
