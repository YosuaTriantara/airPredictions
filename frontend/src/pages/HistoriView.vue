<script setup>
import { ref, watch } from 'vue'
import AreaChart from '../components/AreaChart.vue'
import { useStations } from '../composables/useStations.js'
import { api } from '../services/api.js'

const { stationsGrouped, stations, loading: loadingStations, error: stationsError } =
  useStations()

const selectedId = ref(null)
const loading = ref(false)
const errorMsg = ref(null)
const daily = ref({ labels: [], data: [] })

watch(
  stations,
  (list) => {
    if (list.length && !selectedId.value) {
      selectedId.value = list[0].id
    }
  },
  { immediate: true }
)

watch(selectedId, (id) => {
  if (id) loadHistory(id)
})

function formatHourLabel(iso) {
  try {
    return new Date(iso).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })
  } catch {
    return ''
  }
}

async function loadHistory(stationId) {
  loading.value = true
  errorMsg.value = null
  try {
    const rows = (await api.getMeasurementHistory(stationId, 24)) || []
    daily.value = {
      labels: rows.map((r) => formatHourLabel(r.measurement_time)),
      data: rows.map((r) => Math.round(r.aqi ?? r.pm25 ?? 0)),
    }
  } catch (err) {
    errorMsg.value = err.message || 'Gagal memuat data histori dari server.'
    daily.value = { labels: [], data: [] }
  } finally {
    loading.value = false
  }
}

const stationName = () =>
  stationsGrouped.value.flatMap((g) => g.stations).find((s) => String(s.id) === String(selectedId.value))
    ?.city || ''
</script>

<template>
  <section class="container histori">
    <h1 class="page-heading">Histori AQI</h1>
    <div class="page-heading-rule"></div>

    <label class="field-label" for="station">Stasiun/Kota</label>
    <div class="select-wrap histori-select">
      <select id="station" v-model="selectedId" :disabled="loadingStations">
        <optgroup v-for="g in stationsGrouped" :key="g.state" :label="g.state">
          <option v-for="s in g.stations" :key="s.id" :value="s.id">
            {{ s.name }}
          </option>
        </optgroup>
      </select>
      <svg class="chevron" width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path
          d="M6 9l6 6 6-6"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </div>
    <p v-if="stationsError" class="fetch-error">{{ stationsError }}</p>
    <p v-if="errorMsg" class="fetch-error">{{ errorMsg }}</p>

    <div class="chart-card">
      <h3>Tren AQI 24 Jam Terakhir</h3>
      <p v-if="loading">Memuat data...</p>
      <p v-else-if="!daily.data.length">Belum ada data pengukuran untuk stasiun ini.</p>
      <AreaChart
        v-else
        :series="[{ name: stationName(), color: 'var(--chart)', data: daily.data }]"
        :labels="daily.labels"
        :height="300"
      />
    </div>

    <div class="chart-card">
      <h3>Tren AQI Tahunan</h3>
      <p class="fetch-error">
        Data tren tahunan belum tersedia — backend saat ini hanya menyediakan endpoint histori
        pengukuran jam-jaman (`/measurement/history/{station_id}`), belum ada endpoint agregat
        tahunan.
      </p>
    </div>
  </section>
</template>

<style scoped>
.histori {
  padding: 40px 24px 56px;
}
.histori-select {
  max-width: 100%;
  margin-bottom: 28px;
}
.fetch-error {
  color: var(--danger, #e23b3b);
  font-size: 0.9rem;
  margin: 8px 0 18px;
}
</style>
