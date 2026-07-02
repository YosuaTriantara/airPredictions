import { ref, computed } from 'vue'
import { api } from '../services/api.js'

// State dibuat di luar fungsi supaya dibagikan (singleton) antar komponen
// yang memanggil useStations() — daftar stasiun cukup diambil sekali.
const stations = ref([])
const loading = ref(false)
const error = ref(null)
const loaded = ref(false)

async function fetchStations() {
  if (loaded.value || loading.value) return
  loading.value = true
  error.value = null
  try {
    const data = await api.getStations()
    stations.value = (data || []).map((s) => ({
      id: s.id,
      name: s.station_name,
      city: s.city,
      country: s.country,
      latitude: s.latitude,
      longitude: s.longitude,
      status: s.is_active ? 'Active' : 'Unknown',
    }))
    loaded.value = true
  } catch (err) {
    error.value = err.message || 'Gagal memuat daftar stasiun.'
  } finally {
    loading.value = false
  }
}

// Dikelompokkan per kota untuk <optgroup> pada dropdown (backend tidak
// menyediakan field provinsi/state seperti pada data mock sebelumnya).
const stationsGrouped = computed(() => {
  const groups = new Map()
  for (const s of stations.value) {
    const key = s.city || s.country || 'Lainnya'
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key).push(s)
  }
  return [...groups.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([city, list]) => ({ state: city, stations: list }))
})

function getStationById(id) {
  return stations.value.find((s) => String(s.id) === String(id)) || null
}

export function useStations() {
  fetchStations()
  return {
    stations,
    stationsGrouped,
    loading,
    error,
    getStationById,
    refresh: () => {
      loaded.value = false
      fetchStations()
    },
  }
}
