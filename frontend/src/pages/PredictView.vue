<script setup>
import { ref, computed } from 'vue'
import AreaChart from '../components/AreaChart.vue'
import LungsIcon from '../components/LungsIcon.vue'
import {
  STATIONS_GROUPED,
  getStationById,
  HORIZONS,
  POLLUTANT_UNITS,
  DEFAULT_STATION_ID,
} from '../data/stations.js'
import { generateForecast } from '../utils/chartData.js'
import {
  getAqiCategory,
  getCategoryThreshold,
  isWarningLevel,
  AQI_CATEGORIES,
} from '../utils/aqi.js'

const selectedId = ref(DEFAULT_STATION_ID)
const horizon = ref(12)
const result = ref(null) // { station, horizon, aqi, category, forecast }

function runPrediction() {
  const station = getStationById(selectedId.value)
  const forecast = generateForecast(station, horizon.value)
  const aqi = forecast.target
  result.value = {
    station,
    horizon: horizon.value,
    aqi,
    category: getAqiCategory(aqi),
    forecast,
  }
}

// Tampilkan hasil awal yang sesuai contoh (Delhi – Anand Vihar, 12 jam).
runPrediction()

const chartSeries = computed(() => {
  if (!result.value) return []
  return [
    {
      name: result.value.station.city,
      color: 'var(--chart)',
      data: result.value.forecast.data,
    },
  ]
})

const thresholdConfig = computed(() => {
  if (!result.value) return null
  const t = getCategoryThreshold(result.value.aqi)
  if (t <= 0) return null
  return {
    value: t,
    color: 'var(--danger)',
    label: `Batas Kategori ${result.value.category.name}`,
  }
})

const showAlert = computed(() => result.value && isWarningLevel(result.value.aqi))

const pollutants = computed(() => {
  if (!result.value) return []
  return Object.entries(result.value.station.pollutants).map(([name, value]) => ({
    name,
    value,
    unit: POLLUTANT_UNITS[name] || '',
  }))
})
</script>

<template>
  <!-- Header + form -->
  <section class="predict-head">
    <div class="container">
      <h1 class="page-heading on-dark">Prediksi AQI</h1>
      <div class="rule"></div>

      <label class="field-label on-dark" for="station">Stasiun/Kota</label>
      <div class="select-wrap">
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

      <p class="field-label on-dark range-label">Rentang Prediksi</p>
      <div class="range-grid">
        <button
          v-for="h in HORIZONS"
          :key="h"
          class="range-btn"
          :class="{ active: horizon === h }"
          @click="horizon = h"
        >
          {{ h }} Jam
        </button>
      </div>

      <button class="btn predict-btn" @click="runPrediction">Prediksi</button>
    </div>
  </section>

  <!-- Hasil -->
  <section class="predict-body container" v-if="result">
    <!-- Kartu hasil -->
    <div class="result-card">
      <div class="result-left">
        <span class="result-aqi" :style="{ color: result.category.color }">
          {{ result.aqi }}
        </span>
        <div class="result-meta">
          <span
            class="result-badge"
            :style="{
              color: result.category.color,
              background: result.category.color + '22',
            }"
          >
            {{ result.category.name }}
          </span>
          <p class="result-loc">{{ result.station.name }}</p>
          <p class="result-horizon">Prediksi AQI dalam {{ result.horizon }} Jam</p>
        </div>
      </div>
      <LungsIcon :color="result.category.color" :size="96" />
    </div>

    <!-- Grafik forecast -->
    <div class="chart-card">
      <h3>AQI Forecast – {{ result.horizon }} Jam Kedepan</h3>
      <AreaChart
        :series="chartSeries"
        :labels="result.forecast.labels"
        :threshold="thresholdConfig"
        :height="280"
      />
    </div>

    <!-- Banner peringatan -->
    <div v-if="showAlert" class="alert">
      <div class="alert-icon">
        <svg viewBox="0 0 24 24" fill="none" width="22" height="22">
          <path
            d="M12 3.5L21 19H3l9-15.5z"
            stroke="currentColor"
            stroke-width="2"
            stroke-linejoin="round"
          />
          <path d="M12 10v4" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          <circle cx="12" cy="16.6" r="1.1" fill="currentColor" />
        </svg>
      </div>
      <div>
        <p class="alert-title">Peringatan — Kualitas Udara Memburuk</p>
        <p class="alert-text">{{ result.category.advice }}</p>
      </div>
    </div>

    <!-- Polutan saat ini -->
    <h2 class="pollutant-heading">Kadar Polutan Saat Ini</h2>
    <div class="pollutant-grid">
      <div v-for="p in pollutants" :key="p.name" class="pollutant-card">
        <span class="pollutant-name">{{ p.name }}</span>
        <span class="pollutant-value">{{ p.value }}</span>
        <span class="pollutant-unit">{{ p.unit }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.predict-head {
  background: var(--navy);
  color: #fff;
  padding: 36px 0 44px;
}
.on-dark {
  color: #fff;
}
.rule {
  height: 3px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 2px;
  margin: 12px 0 26px;
}
.range-label {
  margin-top: 22px;
}
.range-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.range-btn {
  background: var(--primary);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  padding: 14px;
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.15s ease, box-shadow 0.15s ease;
}
.range-btn:hover {
  background: var(--primary-d);
}
.range-btn.active {
  background: var(--primary-l);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.25) inset;
}
.predict-btn {
  width: 100%;
  margin-top: 16px;
  background: #cfe2f7;
  color: var(--navy);
  font-size: 1.05rem;
}
.predict-btn:hover {
  background: #bcd6f1;
}

.predict-body {
  padding: 34px 24px 60px;
}

/* Kartu hasil */
.result-card {
  background: #fff;
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 26px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}
.result-left {
  display: flex;
  align-items: center;
  gap: 26px;
}
.result-aqi {
  font-family: 'Quicksand', sans-serif;
  font-weight: 700;
  font-size: 5rem;
  line-height: 1;
}
.result-badge {
  display: inline-block;
  font-weight: 600;
  font-size: 0.92rem;
  padding: 4px 14px;
  border-radius: 999px;
  margin-bottom: 8px;
}
.result-loc {
  font-family: 'Quicksand', sans-serif;
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--ink);
  margin: 0 0 4px;
}
.result-horizon {
  color: var(--muted);
  margin: 0;
}

.pollutant-heading {
  font-size: 1.3rem;
  color: var(--ink);
  margin: 6px 0 16px;
}
.pollutant-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
.pollutant-card {
  background: #fff;
  border: 1.5px solid var(--line);
  border-radius: var(--radius);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.pollutant-name {
  color: var(--muted);
  font-weight: 500;
}
.pollutant-value {
  font-family: 'Quicksand', sans-serif;
  font-weight: 700;
  font-size: 2rem;
  color: var(--ink);
  line-height: 1.05;
}
.pollutant-unit {
  color: var(--muted);
  font-size: 0.9rem;
}

/* Alert */
.alert {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  background: var(--danger-soft);
  border: 1.5px solid var(--danger);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 30px;
  color: var(--danger);
}
.alert-icon {
  flex-shrink: 0;
  margin-top: 2px;
}
.alert-title {
  font-weight: 700;
  margin: 0 0 4px;
}
.alert-text {
  margin: 0;
  color: #8a2b2b;
}

@media (max-width: 860px) {
  .range-grid {
    grid-template-columns: 1fr;
  }
  .result-card {
    flex-direction: column;
    align-items: flex-start;
  }
  .result-aqi {
    font-size: 4rem;
  }
  .pollutant-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
