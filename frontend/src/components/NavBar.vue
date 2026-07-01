<script setup>
import { ref } from 'vue'
import BrandMark from './BrandMark.vue'

const open = ref(false)
const links = [
  { to: '/', label: 'Home' },
  { to: '/predict', label: 'Predict' },
  { to: '/histori', label: 'Histori' },
]
</script>

<template>
  <header class="nav">
    <div class="container nav-inner">
      <RouterLink to="/" class="nav-brand" @click="open = false">
        <BrandMark :size="30" />
      </RouterLink>

      <button
        class="nav-toggle"
        :aria-expanded="open"
        aria-label="Buka menu"
        @click="open = !open"
      >
        <span></span><span></span><span></span>
      </button>

      <nav class="nav-links" :class="{ 'is-open': open }">
        <RouterLink
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          class="nav-link"
          @click="open = false"
        >
          {{ l.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.nav {
  background: var(--navy);
  color: var(--on-dark);
  position: sticky;
  top: 0;
  z-index: 50;
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}
.nav-brand {
  color: #fff;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 34px;
}
.nav-link {
  color: var(--on-dark-muted);
  font-weight: 500;
  font-size: 1.02rem;
  transition: color 0.15s ease;
}
.nav-link:hover {
  color: #fff;
}
.nav-link.router-link-active {
  color: #fff;
  font-weight: 600;
}
.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
}
.nav-toggle span {
  width: 24px;
  height: 2.5px;
  background: #fff;
  border-radius: 2px;
}

@media (max-width: 720px) {
  .nav-toggle {
    display: flex;
  }
  .nav-links {
    position: absolute;
    top: 70px;
    left: 0;
    right: 0;
    background: var(--navy);
    flex-direction: column;
    gap: 0;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.25s ease;
  }
  .nav-links.is-open {
    max-height: 240px;
  }
  .nav-link {
    width: 100%;
    padding: 16px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }
}
</style>
