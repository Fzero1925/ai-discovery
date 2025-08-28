// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://fzero1925.github.io',
  base: '/ai-compass',
  integrations: [tailwind()],
  build: {
    assets: '_astro'
  }
});
