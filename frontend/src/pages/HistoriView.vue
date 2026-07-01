<script setup>
import { ref, computed } from 'vue'
import AreaChart from '../components/AreaChart.vue'
import { STATIONS_GROUPED, getStationById, DEFAULT_STATION_ID } from '../data/stations.js'
import { generate24h, generateYearly } from '../utils/chartData.js'

const selectedId = ref(DEFAULT_STATION_ID)
const station = computed(() => getStationById(selectedId.value))

const daily = computed(() => generate24h(station.value))
const yearly = computed(() => generateYearly(station.value))

const dailySeries = computed(() => [
  { name: station.value.city, color: 'var(--chart)', data: daily.value.data },
])
const yearlySeries = computed(() => [
  { name: station.value.city, color: 'var(--chart)', data: yearly.value.data },
])
</script>

<template>
  <section class="container histori">
    <h1 class="page-heading">Histori AQI</h1>
    <div class="page-heading-rule"></div>

    <label class="field-label" for="station">Stasiun/Kota</label>
    <div class="select-wrap histori-select">
      <select id="station" v-model="selectedId">
        <optgroup v-for="g in STATIONS_GROUPED" :key="g.state" :label="g.state">
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

    <div class="chart-card">
      <h3>Tren AQI 24 Jam Terakhir</h3>
      <AreaChart :series="dailySeries" :labels="daily.labels" :height="300" />
    </div>

    <div class="chart-card">
      <h3>Tren AQI Tahunan – 2015–2020</h3>
      <AreaChart :series="yearlySeries" :labels="yearly.labels" :height="300" />
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
</style>
