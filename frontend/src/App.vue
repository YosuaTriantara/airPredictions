<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
</script>

<template>
  <NavBar />
  <main class="page-grow">
    <RouterView />
  </main>
  <FooterBar />
</template>
