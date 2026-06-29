<script setup>
defineProps({
  size: { type: Number, default: 30 },
})
</script>

<template>
  <span class="brand">
    <svg
      class="brand-icon"
      :width="size"
      :height="size"
      viewBox="0 0 32 32"
      fill="none"
      aria-hidden="true"
    >
      <g stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
        <path d="M5 13h11a2.6 2.6 0 1 0 -2.6 -2.6" />
        <path d="M5 18h14a2.6 2.6 0 1 1 -2.6 2.6" />
        <path d="M5 23h8" />
      </g>
    </svg>
    <span class="brand-text">AIRA</span>
  </span>
</template>

<style scoped>
.brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
}
.brand-icon {
  display: block;
}
.brand-text {
  font-family: 'Quicksand', sans-serif;
  font-weight: 700;
  font-size: 1.35rem;
  letter-spacing: 0.02em;
}
</style>
