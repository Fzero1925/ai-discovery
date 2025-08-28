export interface ToolData {
  id: string;
  title: string;
  category: string;
  rating: number;
  rating_count: number;
  description: string;
  logo?: string;
  hot?: boolean;
  last_updated: string;
  tags: string[];
  pricing: 'free' | 'freemium' | 'paid';
  url: string;
}

export const categories = [
  {
    id: 'image-tools',
    name: '图像工具',
    description: 'AI 图像编辑、生成和处理工具',
    icon: '🎨',
    count: 12
  },
  {
    id: 'text-tools', 
    name: '文本工具',
    description: 'AI 写作、翻译和文本处理工具',
    icon: '✍️',
    count: 8
  },
  {
    id: 'productivity',
    name: '效率工具',
    description: 'AI 辅助办公和生产力工具',
    icon: '⚡',
    count: 15
  },
  {
    id: 'video-tools',
    name: '视频工具',
    description: 'AI 视频编辑、生成和处理工具',
    icon: '🎬',
    count: 6
  }
];

export const featuredTools: ToolData[] = [
  {
    id: 'nano-banana',
    title: 'Nano Banana',
    category: 'image-tools',
    rating: 4.5,
    rating_count: 128,
    description: '专业的 AI 图像编辑工具，支持智能抠图、背景替换等功能',
    hot: true,
    last_updated: '2025-01-15',
    tags: ['图像编辑', '背景移除', 'AI增强'],
    pricing: 'freemium',
    url: 'https://nanobanana.ai'
  },
  {
    id: 'chatgpt',
    title: 'ChatGPT',
    category: 'text-tools',
    rating: 4.8,
    rating_count: 2156,
    description: '最受欢迎的 AI 对话助手，支持写作、编程、分析等多种任务',
    hot: true,
    last_updated: '2025-01-20',
    tags: ['对话AI', '写作辅助', '编程助手'],
    pricing: 'freemium',
    url: 'https://chat.openai.com'
  },
  {
    id: 'midjourney',
    title: 'Midjourney',
    category: 'image-tools', 
    rating: 4.7,
    rating_count: 892,
    description: '顶级的 AI 图像生成工具，以艺术性和创意著称',
    hot: true,
    last_updated: '2025-01-18',
    tags: ['图像生成', 'AI艺术', '创意设计'],
    pricing: 'paid',
    url: 'https://midjourney.com'
  }
];