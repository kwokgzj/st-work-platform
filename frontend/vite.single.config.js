import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { viteSingleFile } from 'vite-plugin-singlefile';

// 單檔構建：所有 JS/CSS 內聯進一個 HTML，file:// 雙擊即可使用（api.js 自動切 localStorage 模式）
export default defineConfig({
  plugins: [vue(), viteSingleFile()],
  build: { outDir: 'dist-single', emptyOutDir: true },
});
