import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// base: './' agar aset memakai path relatif (cocok untuk GitHub Pages)
export default defineConfig({
  plugins: [vue()],
  base: './',
})
