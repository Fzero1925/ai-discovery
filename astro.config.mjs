// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://ai-compass.github.io',
  // Uncomment the line below if deploying to a GitHub Pages subdirectory
  // base: '/ai-compass',
  integrations: [tailwind()],
  build: {
    assets: '_astro'
  }
});
