<script setup>
import { computed } from 'vue'

const props = defineProps({
  // series: [{ name, color, data: number[] }]
  series: { type: Array, required: true },
  labels: { type: Array, default: () => [] },
  height: { type: Number, default: 300 },
  yTicks: { type: Number, default: 5 },
  maxY: { type: Number, default: null },
  // threshold: { value, color, label }
  threshold: { type: Object, default: null },
  showLegend: { type: Boolean, default: true },
})

// Sistem koordinat internal (viewBox). SVG diskalakan ke lebar kontainer.
const W = 1000
const H = computed(() => props.height)
const padLeft = 52
const padRight = 22
const padTop = 18
const padBottom = 38

const plotLeft = padLeft
const plotRight = computed(() => W - padRight)
const plotTop = padTop
const plotBottom = computed(() => H.value - padBottom)
const plotW = computed(() => plotRight.value - plotLeft)
const plotH = computed(() => plotBottom.value - plotTop)

const uid = Math.random().toString(36).slice(2, 8)

const niceMax = computed(() => {
  if (props.maxY) return props.maxY
  let max = 0
  for (const s of props.series) {
    for (const v of s.data) max = Math.max(max, v)
  }
  if (props.threshold) max = Math.max(max, props.threshold.value)
  if (max <= 0) return 10
  // bulatkan ke atas ke kelipatan "rapi"
  const step = Math.pow(10, Math.floor(Math.log10(max)))
  const rounded = Math.ceil(max / (step / 2)) * (step / 2)
  return rounded
})

function xAt(i, n) {
  if (n <= 1) return plotLeft + plotW.value / 2
  return plotLeft + (i / (n - 1)) * plotW.value
}
function yAt(v) {
  return plotBottom.value - (v / niceMax.value) * plotH.value
}

function pointsFor(data) {
  return data.map((v, i) => ({ x: xAt(i, data.length), y: yAt(v) }))
}

// Kurva halus (Catmull-Rom -> Bezier)
function smoothLine(pts) {
  if (pts.length < 2) return pts.length ? `M ${pts[0].x} ${pts[0].y}` : ''
  let d = `M ${pts[0].x.toFixed(2)} ${pts[0].y.toFixed(2)}`
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i]
    const p1 = pts[i]
    const p2 = pts[i + 1]
    const p3 = pts[i + 2] || p2
    const cp1x = p1.x + (p2.x - p0.x) / 6
    const cp1y = p1.y + (p2.y - p0.y) / 6
    const cp2x = p2.x - (p3.x - p1.x) / 6
    const cp2y = p2.y - (p3.y - p1.y) / 6
    d += ` C ${cp1x.toFixed(2)} ${cp1y.toFixed(2)}, ${cp2x.toFixed(2)} ${cp2y.toFixed(
      2
    )}, ${p2.x.toFixed(2)} ${p2.y.toFixed(2)}`
  }
  return d
}

const renderSeries = computed(() =>
  props.series.map((s, idx) => {
    const pts = pointsFor(s.data)
    const line = smoothLine(pts)
    const first = pts[0]
    const last = pts[pts.length - 1]
    const area =
      line +
      ` L ${last.x.toFixed(2)} ${plotBottom.value} L ${first.x.toFixed(2)} ${plotBottom.value} Z`
    return {
      name: s.name,
      color: s.color || 'var(--chart)',
      line,
      area,
      gradId: `grad-${uid}-${idx}`,
    }
  })
)

const yGrid = computed(() => {
  const arr = []
  for (let i = 0; i <= props.yTicks; i++) {
    const v = (niceMax.value / props.yTicks) * i
    arr.push({ value: Math.round(v), y: yAt(v) })
  }
  return arr
})

const xLabels = computed(() => {
  const n = props.labels.length
  return props.labels.map((label, i) => ({
    label,
    x: xAt(i, n),
  }))
})

const thresholdY = computed(() =>
  props.threshold ? yAt(props.threshold.value) : 0
)
</script>

<template>
  <div class="chart">
    <svg :viewBox="`0 0 ${W} ${H}`" class="chart-svg" preserveAspectRatio="xMidYMid meet">
      <defs>
        <linearGradient
          v-for="s in renderSeries"
          :key="s.gradId"
          :id="s.gradId"
          x1="0"
          y1="0"
          x2="0"
          y2="1"
        >
          <stop offset="0%" :stop-color="s.color" stop-opacity="0.32" />
          <stop offset="100%" :stop-color="s.color" stop-opacity="0.02" />
        </linearGradient>
      </defs>

      <!-- Grid + label sumbu Y -->
      <g class="grid">
        <line
          v-for="g in yGrid"
          :key="'g' + g.value"
          :x1="plotLeft"
          :x2="plotRight"
          :y1="g.y"
          :y2="g.y"
        />
        <text
          v-for="g in yGrid"
          :key="'t' + g.value"
          :x="plotLeft - 12"
          :y="g.y + 4"
          class="axis-y"
        >
          {{ g.value }}
        </text>
      </g>

      <!-- Garis ambang batas kategori -->
      <g v-if="threshold">
        <line
          :x1="plotLeft"
          :x2="plotRight"
          :y1="thresholdY"
          :y2="thresholdY"
          class="threshold-line"
          :stroke="threshold.color"
        />
      </g>

      <!-- Area + garis tiap series -->
      <g v-for="s in renderSeries" :key="s.name">
        <path :d="s.area" :fill="`url(#${s.gradId})`" />
        <path :d="s.line" fill="none" :stroke="s.color" stroke-width="2.6" />
      </g>

      <!-- Label sumbu X -->
      <text
        v-for="(xl, i) in xLabels"
        :key="'x' + i"
        :x="xl.x"
        :y="plotBottom + 26"
        class="axis-x"
      >
        {{ xl.label }}
      </text>
    </svg>

    <!-- Legend -->
    <div v-if="showLegend" class="legend">
      <span v-for="s in renderSeries" :key="'l' + s.name" class="legend-item">
        <span class="legend-swatch" :style="{ background: s.color }"></span>
        {{ s.name }}
      </span>
      <span v-if="threshold" class="legend-item">
        <span class="legend-swatch" :style="{ background: threshold.color }"></span>
        {{ threshold.label }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.chart-svg {
  width: 100%;
  height: auto;
  display: block;
  overflow: visible;
}
.grid line {
  stroke: rgba(15, 39, 71, 0.12);
  stroke-width: 1;
}
.axis-y {
  fill: var(--muted);
  font-size: 18px;
  text-anchor: end;
  font-family: 'Poppins', sans-serif;
}
.axis-x {
  fill: var(--muted);
  font-size: 18px;
  text-anchor: middle;
  font-family: 'Poppins', sans-serif;
}
.threshold-line {
  stroke-width: 2.4;
  stroke-dasharray: 7 6;
}
.legend {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 22px;
  margin-top: 10px;
  font-size: 0.86rem;
  color: var(--muted);
}
.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.legend-swatch {
  width: 18px;
  height: 4px;
  border-radius: 2px;
  display: inline-block;
}
</style>
