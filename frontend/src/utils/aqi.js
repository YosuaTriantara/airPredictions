// Kategori AQI mengikuti skala CPCB India (sesuai dataset yang digunakan model).
export const AQI_CATEGORIES = [
  { name: 'Good', min: 0, max: 50, color: '#22a45d', advice: 'Kualitas udara baik. Aman untuk semua aktivitas di luar ruangan.' },
  { name: 'Satisfactory', min: 51, max: 100, color: '#84b515', advice: 'Kualitas udara memuaskan. Sebagian kecil orang sensitif perlu sedikit waspada.' },
  { name: 'Moderate', min: 101, max: 200, color: '#efb008', advice: 'Kelompok sensitif (anak, lansia, penderita asma) sebaiknya membatasi aktivitas berat di luar.' },
  { name: 'Poor', min: 201, max: 300, color: '#f5793b', advice: 'AQI diprediksi masuk kategori Poor. Kurangi aktivitas di luar ruangan.' },
  { name: 'Very Poor', min: 301, max: 400, color: '#e23b3b', advice: 'Kualitas udara sangat buruk. Hindari aktivitas luar ruangan dan gunakan masker.' },
  { name: 'Severe', min: 401, max: 9999, color: '#8b1a2b', advice: 'Kualitas udara berbahaya. Tetap di dalam ruangan dan gunakan penyaring udara.' },
]

export function getAqiCategory(value) {
  const v = Math.max(0, Math.round(value))
  return (
    AQI_CATEGORIES.find((c) => v >= c.min && v <= c.max) ||
    AQI_CATEGORIES[AQI_CATEGORIES.length - 1]
  )
}

export function getCategoryIndex(value) {
  return AQI_CATEGORIES.indexOf(getAqiCategory(value))
}

// Nilai ambang batas bawah kategori (mis. Poor -> 200) untuk garis batas pada grafik.
export function getCategoryThreshold(value) {
  const cat = getAqiCategory(value)
  return Math.max(0, cat.min - 1)
}

// Kategori dianggap "peringatan" mulai dari Poor (indeks 3) ke atas.
export function isWarningLevel(value) {
  return getCategoryIndex(value) >= 3
}
