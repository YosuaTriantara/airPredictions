import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../pages/HomeView.vue'
import PredictView from '../pages/PredictView.vue'
import HistoriView from '../pages/HistoriView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/predict', name: 'predict', component: PredictView },
  { path: '/histori', name: 'histori', component: HistoriView },
]

// createWebHashHistory dipilih agar routing tetap jalan di GitHub Pages
// tanpa konfigurasi server tambahan.
const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
