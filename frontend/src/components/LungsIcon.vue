<script setup>
// Indikator kesehatan berbentuk paru-paru. Lobus diisi penuh dengan warna
// kategori AQI (hijau = sehat hingga merah/marun = berbahaya), dengan pohon
// bronkus putih di atasnya sebagai detail agar menonjol sebagai sinyal visual.
defineProps({
  color: { type: String, default: '#22a45d' },
  size: { type: Number, default: 92 },
})
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 64 64"
    fill="none"
    role="img"
    aria-label="Indikator kesehatan paru-paru"
  >
    <!-- Lobus paru kiri (terisi penuh) -->
    <path
      d="M25.8 21.5
         C 22 23.5 18 27.5 16.4 33.8
         C 15.2 39 15.2 45.2 18 49
         C 20.4 52.2 24.6 51 25.6 45.8
         C 26.6 40.4 27 30 27 24
         Z"
      :fill="color"
    />

    <!-- Lobus paru kanan (terisi penuh) -->
    <path
      d="M38.2 21.5
         C 42 23.5 46 27.5 47.6 33.8
         C 48.8 39 48.8 45.2 46 49
         C 43.6 52.2 39.4 51 38.4 45.8
         C 37.4 40.4 37 30 37 24
         Z"
      :fill="color"
    />

    <!-- Pohon bronkus + trakea (putih) -->
    <g
      stroke="#ffffff"
      stroke-width="2.4"
      stroke-linecap="round"
      stroke-linejoin="round"
      fill="none"
    >
      <!-- trakea -->
      <path d="M32 9 V24" />
      <!-- bronkus utama kiri & kanan -->
      <path d="M32 21 C 29.5 25 26.5 29 25 34.5" />
      <path d="M32 21 C 34.5 25 37.5 29 39 34.5" />
      <!-- cabang kecil kiri -->
      <path d="M27 30 l -3.4 1.6" />
      <path d="M25.4 35.5 l -3.2 1.2" />
      <!-- cabang kecil kanan -->
      <path d="M37 30 l 3.4 1.6" />
      <path d="M38.6 35.5 l 3.2 1.2" />
    </g>

    <!-- simpul atas trakea -->
    <circle cx="32" cy="8.6" r="2.5" :fill="color" />
  </svg>
</template>
