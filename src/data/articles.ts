export interface Article {
  slug: string;
  title: string;
  description: string;
  category: ArticleCategory;
  publishDate: string;
  author: string;
  tags: string[];
  readTime: number;
  featured: boolean;
  image?: string;
  content?: string;
}

export type ArticleCategory = 
  | 'image-ai' 
  | 'text-ai' 
  | 'productivity' 
  | 'media' 
  | 'developer' 
  | 'tutorials' 
  | 'insights' 
  | 'comparisons';

export const articleCategories = {
  'image-ai': {
    name: '图像AI',
    description: '图像AI工具评测与应用指南',
    icon: '🎨',
    color: 'from-purple-500 to-pink-500'
  },
  'text-ai': {
    name: '文本AI', 
    description: '文本AI工具分析与使用技巧',
    icon: '✍️',
    color: 'from-blue-500 to-indigo-500'
  },
  'productivity': {
    name: '效率工具',
    description: '提升工作效率的AI生产力工具',
    icon: '⚡',
    color: 'from-green-500 to-teal-500'
  },
  'media': {
    name: '多媒体',
    description: '音频、视频AI工具和应用',
    icon: '🎵',
    color: 'from-orange-500 to-red-500'
  },
  'developer': {
    name: '开发工具',
    description: '面向开发者的AI编程助手',
    icon: '💻',
    color: 'from-gray-500 to-slate-500'
  },
  'tutorials': {
    name: '教程指南',
    description: 'AI工具使用教程和实战指南',
    icon: '📚',
    color: 'from-yellow-500 to-amber-500'
  },
  'insights': {
    name: '行业洞察',
    description: 'AI行业趋势分析和深度洞察',
    icon: '💡',
    color: 'from-cyan-500 to-blue-500'
  },
  'comparisons': {
    name: '工具对比',
    description: 'AI工具深度对比分析',
    icon: '⚖️',
    color: 'from-rose-500 to-pink-500'
  }
} as const;

// 示例文章数据 - 转换自原有工具数据
export const articles: Article[] = [
  {
    slug: 'nano-banana-comprehensive-review',
    title: 'Nano Banana 深度评测：AI图像编辑的新选择',
    description: '全面分析Nano Banana的功能特色、使用体验和应用场景，为你提供专业的工具选择建议。',
    category: 'image-ai',
    publishDate: '2025-01-16',
    author: 'AI Compass Team',
    tags: ['图像编辑', 'AI工具', '评测', 'Nano Banana'],
    readTime: 8,
    featured: true,
    image: '/images/articles/nano-banana-review.svg'
  },
  {
    slug: 'chatgpt-advanced-guide',
    title: 'ChatGPT 高级应用指南：从入门到精通',
    description: '深入探索ChatGPT的高级功能和使用技巧，包括提示词工程、API应用和最佳实践。',
    category: 'text-ai', 
    publishDate: '2025-01-15',
    author: 'AI Compass Team',
    tags: ['ChatGPT', '文本AI', '教程', '提示词'],
    readTime: 12,
    featured: true,
    image: '/images/articles/chatgpt-guide.svg'
  },
  {
    slug: 'ai-writing-tools-comparison-2025',
    title: '2025年AI写作工具深度对比：ChatGPT vs Claude vs Jasper',
    description: '详细对比主流AI写作工具的功能特色、性能表现和适用场景，帮你选择最适合的写作助手。',
    category: 'comparisons',
    publishDate: '2025-01-14', 
    author: 'AI Compass Team',
    tags: ['写作工具', '对比分析', 'ChatGPT', 'Claude', 'Jasper'],
    readTime: 15,
    featured: true,
    image: '/images/articles/ai-writing-comparison.svg'
  },
  {
    slug: 'ai-image-generation-beginner-guide',
    title: 'AI图像生成入门指南：从零开始掌握AI绘画',
    description: '全面介绍AI图像生成的基础概念、常用工具和实用技巧，零基础也能快速上手AI绘画。',
    category: 'tutorials',
    publishDate: '2025-01-13',
    author: 'AI Compass Team', 
    tags: ['图像生成', 'AI绘画', '入门教程', 'Midjourney', 'DALL-E'],
    readTime: 10,
    featured: false,
    image: '/images/articles/ai-image-guide.svg'
  }
];

// 获取特色文章
export const getFeaturedArticles = () => articles.filter(article => article.featured);

// 按分类获取文章
export const getArticlesByCategory = (category: ArticleCategory) => 
  articles.filter(article => article.category === category);

// 获取最新文章
export const getLatestArticles = (limit?: number) => {
  const sortedArticles = [...articles].sort((a, b) => 
    new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime()
  );
  return limit ? sortedArticles.slice(0, limit) : sortedArticles;
};

// 根据slug获取文章
export const getArticleBySlug = (slug: string) => 
  articles.find(article => article.slug === slug);

// 获取相关文章
export const getRelatedArticles = (currentSlug: string, limit: number = 3) => {
  const currentArticle = getArticleBySlug(currentSlug);
  if (!currentArticle) return [];
  
  return articles
    .filter(article => 
      article.slug !== currentSlug && 
      (article.category === currentArticle.category || 
       article.tags.some(tag => currentArticle.tags.includes(tag)))
    )
    .sort((a, b) => new Date(b.publishDate).getTime() - new Date(a.publishDate).getTime())
    .slice(0, limit);
};