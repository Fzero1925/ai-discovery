export async function GET() {
  const baseUrl = 'https://fzero1925.github.io/ai-compass';
  
  const staticPages = [
    '',
    '/tools',
    '/tools/image-tools',
    '/tools/text-tools', 
    '/tools/productivity',
    '/tools/video-tools'
  ];
  
  const toolPages = [
    '/tools/image-tools/nano-banana',
    '/tools/text-tools/chatgpt'
    // Add more tool pages here as they are created
  ];
  
  const allPages = [...staticPages, ...toolPages];
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages.map(page => {
    const url = `${baseUrl}${page}`;
    const lastmod = new Date().toISOString();
    const priority = getPriority(page);
    const changefreq = getChangefreq(page);
    
    return `  <url>
    <loc>${url}</loc>
    <lastmod>${lastmod}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>
  </url>`;
  }).join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
    },
  });
}

function getPriority(page: string): string {
  if (page === '') return '1.0'; // Homepage
  if (page === '/tools') return '0.9'; // Tools overview
  if (page.includes('/tools/') && !page.includes('/nano-banana') && !page.includes('/chatgpt')) return '0.8'; // Category pages
  if (page.includes('/nano-banana') || page.includes('/chatgpt')) return '0.7'; // Tool detail pages
  return '0.6'; // Other pages
}

function getChangefreq(page: string): string {
  if (page === '' || page === '/tools') return 'weekly'; // Homepage and main pages
  if (page.includes('/tools/') && !page.includes('/nano-banana') && !page.includes('/chatgpt')) return 'weekly'; // Category pages
  if (page.includes('/nano-banana') || page.includes('/chatgpt')) return 'monthly'; // Tool detail pages
  return 'monthly'; // Other pages
}