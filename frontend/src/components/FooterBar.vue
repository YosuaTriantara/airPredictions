<script setup>
import BrandMark from './BrandMark.vue'
</script>

<template>
  <footer class="footer">
    <div class="container footer-inner">
      <BrandMark :size="30" />
      <p class="footer-tag">Monitoring dan Prediksi Kualitas Udara di India</p>
      <div class="footer-rule"></div>
      <p class="footer-copy">© 2026 AIRA. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--navy);
  color: var(--on-dark);
  margin-top: auto;
}
.footer-inner {
  text-align: center;
  padding: 34px 24px 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.footer-tag {
  margin: 12px 0 0;
  font-weight: 600;
  color: var(--on-dark);
}
.footer-rule {
  width: min(680px, 100%);
  height: 1px;
  background: rgba(255, 255, 255, 0.16);
  margin: 22px 0;
}
.footer-copy {
  margin: 0;
  font-size: 0.92rem;
  color: var(--on-dark-muted);
}
</style>
