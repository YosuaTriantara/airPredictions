<script setup>
// Ilustrasi awan + angin (selaras dengan logo AIRA) untuk hero halaman Home.
</script>

<template>
  <svg
    class="hero-art"
    viewBox="0 0 260 210"
    fill="none"
    aria-hidden="true"
  >
    <!-- Awan -->
    <path
      d="M86 150
         C 60 150 46 132 58 114
         C 50 92 78 78 96 92
         C 104 66 146 66 156 92
         C 184 84 210 104 200 130
         C 220 134 220 158 196 158
         L 96 158
         C 84 158 80 154 86 150 Z"
      fill="#cfe2f7"
      stroke="#0a2342"
      stroke-width="5"
      stroke-linejoin="round"
    />

    <!-- Pusaran angin di dalam awan -->
    <path
      d="M120 128 a9 9 0 1 1 -7 -14"
      stroke="#0a2342"
      stroke-width="4.5"
      stroke-linecap="round"
    />
    <path
      d="M158 132 a9 9 0 1 1 -7 -14"
      stroke="#0a2342"
      stroke-width="4.5"
      stroke-linecap="round"
    />

    <!-- Garis angin keluar dari awan -->
    <path
      d="M40 170 h54 a8 8 0 1 0 -7 -8"
      stroke="#0a2342"
      stroke-width="4.5"
      stroke-linecap="round"
    />
    <path
      d="M58 186 h40 a7 7 0 1 1 -6 7"
      stroke="#0a2342"
      stroke-width="4.5"
      stroke-linecap="round"
    />
  </svg>
</template>

<style scoped>
.hero-art {
  width: 100%;
  height: auto;
  max-width: 360px;
  display: block;
}
</style>
