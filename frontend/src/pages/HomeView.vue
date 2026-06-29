<script setup>
import { useRouter } from 'vue-router'
import HeroArt from '../components/HeroArt.vue'

const router = useRouter()

const stats = [
  { value: '200+', label: 'Monitoring Stasiun' },
  { value: '6', label: 'Parameter Polutan' },
  { value: '127', label: 'Kota di India' },
]

const features = [
  {
    key: 'forecast',
    title: 'AQI Forecasting',
    desc: 'Prediksi nilai AQI untuk 6, 12, dan 24 jam ke depan.',
  },
  {
    key: 'classify',
    title: 'Klasifikasi Kategori AQI',
    desc: 'Menentukan kategori kualitas udara berdasarkan nilai AQI ke dalam enam tingkat kondisi.',
  },
  {
    key: 'history',
    title: 'Data Historis AQI',
    desc: 'Menampilkan riwayat nilai AQI untuk membantu memahami perubahan kualitas udara.',
  },
  {
    key: 'alert',
    title: 'Sistem Peringatan',
    desc: 'Menyediakan informasi dan saran tindakan ketika kualitas udara berada pada kategori tidak sehat.',
  },
]
</script>

<template>
  <!-- HERO -->
  <section class="hero">
    <div class="container hero-inner">
      <div class="hero-text">
        <h1 class="hero-title">Monitoring dan Prediksi Kualitas Udara di India</h1>
        <p class="hero-sub">
          Prediksi kualitas udara beberapa jam ke depan, dengan klasifikasi AQI
          dan pemanfaatan data historis dari 200+ stasiun di India.
        </p>

        <div class="hero-actions">
          <button class="btn btn-ghost" @click="router.push('/predict')">
            Mulai Prediksi
          </button>
          <button class="btn btn-ghost" @click="router.push('/histori')">
            Lihat Histori
          </button>
        </div>

        <div class="stats">
          <div v-for="s in stats" :key="s.label" class="stat-card">
            <div class="stat-value">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </div>

      <div class="hero-illustration">
        <HeroArt />
      </div>
    </div>
  </section>

  <!-- FITUR -->
  <section class="section features-section">
    <div class="container">
      <h2 class="section-title">Fitur Utama Sistem</h2>
      <div class="features">
        <article v-for="f in features" :key="f.key" class="feature-card">
          <div class="feature-icon">
            <!-- AQI Forecasting -->
            <svg v-if="f.key === 'forecast'" viewBox="0 0 24 24" fill="none">
              <path
                d="M4 17l5-5 3 3 7-7"
                stroke="#fff"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
              <path
                d="M16 8h4v4"
                stroke="#fff"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <!-- Klasifikasi -->
            <svg v-else-if="f.key === 'classify'" viewBox="0 0 24 24" fill="none">
              <path
                d="M7 3l4 7H3l4-7z"
                stroke="#fff"
                stroke-width="2"
                stroke-linejoin="round"
              />
              <rect
                x="13"
                y="4"
                width="7"
                height="7"
                rx="1.5"
                stroke="#fff"
                stroke-width="2"
              />
              <circle cx="8" cy="17.5" r="3.5" stroke="#fff" stroke-width="2" />
              <circle cx="16.5" cy="17.5" r="3.5" stroke="#fff" stroke-width="2" />
            </svg>
            <!-- Data Historis -->
            <svg v-else-if="f.key === 'history'" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="9" stroke="#fff" stroke-width="2" />
              <path
                d="M12 7v5l3.5 2"
                stroke="#fff"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <!-- Sistem Peringatan -->
            <svg v-else viewBox="0 0 24 24" fill="none">
              <path
                d="M12 3.5L21 19H3l9-15.5z"
                stroke="#fff"
                stroke-width="2"
                stroke-linejoin="round"
              />
              <path
                d="M12 10v4"
                stroke="#fff"
                stroke-width="2"
                stroke-linecap="round"
              />
              <circle cx="12" cy="16.6" r="1.1" fill="#fff" />
            </svg>
          </div>
          <h3 class="feature-title">{{ f.title }}</h3>
          <p class="feature-desc">{{ f.desc }}</p>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  background: linear-gradient(120deg, var(--hero-1) 0%, var(--hero-2) 100%);
  color: #fff;
  padding: 60px 0 70px;
}
.hero-inner {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 40px;
  align-items: center;
}
.hero-title {
  font-size: 2.7rem;
  line-height: 1.12;
  margin: 0 0 18px;
  max-width: 14ch;
}
.hero-sub {
  color: var(--on-dark-muted);
  font-size: 1.05rem;
  line-height: 1.6;
  margin: 0 0 30px;
  max-width: 52ch;
}
.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.stat-card {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: var(--radius);
  padding: 20px 22px;
}
.stat-value {
  font-family: 'Quicksand', sans-serif;
  font-weight: 700;
  font-size: 2rem;
  line-height: 1;
}
.stat-label {
  margin-top: 8px;
  color: var(--on-dark-muted);
  font-size: 0.95rem;
}
.hero-illustration {
  display: flex;
  justify-content: center;
}

.features-section {
  background: var(--page);
}
.features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 22px;
}
.feature-card {
  background: var(--feature);
  border-radius: var(--radius);
  padding: 26px 28px;
}
.feature-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: var(--navy);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}
.feature-icon svg {
  width: 26px;
  height: 26px;
}
.feature-title {
  font-size: 1.4rem;
  color: var(--ink);
  margin: 0 0 10px;
}
.feature-desc {
  color: var(--ink-2);
  line-height: 1.55;
  margin: 0;
}

@media (max-width: 860px) {
  .hero-inner {
    grid-template-columns: 1fr;
  }
  .hero-illustration {
    order: -1;
  }
  .hero-title {
    font-size: 2.1rem;
  }
  .features {
    grid-template-columns: 1fr;
  }
  .stats {
    grid-template-columns: 1fr;
  }
}
</style>
