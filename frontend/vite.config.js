import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    // dev 時轉發到後端 uvicorn；可用 VITE_API_TARGET 指到其他埠（如 8001），避免與已部署實例衝突
    proxy: { '/api': process.env.VITE_API_TARGET || 'http://localhost:8000' },
  },
});
