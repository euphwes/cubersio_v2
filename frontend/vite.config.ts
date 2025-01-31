import { sveltekit } from '@sveltejs/kit/vite';

export default {
  plugins: [sveltekit()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // FastAPI backend
        changeOrigin: true,
        rewrite: (path: string) => path.replace(/^\/api/, '') // Optional: adjust path
      }
    }
  }
};
