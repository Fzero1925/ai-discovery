export interface ToolDetail {
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
  
  // 6模块详细信息
  introduction: {
    overview: string;
    purpose: string;
    target_users: string[];
  };
  
  highlights: {
    features: string[];
    advantages: string[];
    unique_selling_points: string[];
  };
  
  use_cases: {
    scenarios: Array<{
      title: string;
      description: string;
      example?: string;
    }>;
    industries: string[];
    user_types: string[];
  };
  
  community_reviews: {
    pros: string[];
    cons: string[];
    user_feedback: Array<{
      rating: number;
      comment: string;
      author?: string;
    }>;
    expert_review?: {
      score: number;
      summary: string;
      detailed_analysis: string;
    };
  };
  
  access_info: {
    pricing_plans: Array<{
      name: string;
      price: string;
      features: string[];
      recommended?: boolean;
    }>;
    free_trial?: {
      duration: string;
      limitations: string[];
    };
    system_requirements?: {
      platform: string[];
      browser?: string[];
      other?: string[];
    };
  };
  
  faq: Array<{
    question: string;
    answer: string;
    category?: string;
  }>;
}

export const toolDetails: Record<string, ToolDetail> = {
  'nano-banana': {
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
    url: 'https://nanobanana.ai',
    
    introduction: {
      overview: 'Nano Banana 是一款基于先进AI技术的图像编辑工具，专注于简化复杂的图像处理任务。通过深度学习算法，它能够智能识别图像中的对象并进行精确的编辑操作。',
      purpose: '为设计师、营销人员和内容创作者提供快速、专业的图像编辑解决方案，让复杂的图像处理变得简单易用。',
      target_users: ['平面设计师', '电商运营', '社交媒体营销', '内容创作者', '摄影师']
    },
    
    highlights: {
      features: [
        '一键智能抠图，支持复杂背景',
        '背景替换和生成',
        '图像质量增强和修复',
        '批量处理功能',
        'API集成支持'
      ],
      advantages: [
        '处理速度快，单张图片3-5秒完成',
        '精度高，边缘处理自然',
        '支持多种图像格式',
        '云端处理，无需安装软件',
        '用户界面简洁直观'
      ],
      unique_selling_points: [
        '独有的边缘优化算法',
        '支持毛发等细节抠图',
        '智能背景建议功能',
        '与Adobe、Figma等工具集成'
      ]
    },
    
    use_cases: {
      scenarios: [
        {
          title: '电商产品图处理',
          description: '快速移除产品背景，制作统一的白底图片',
          example: '服装、3C产品、家居用品等商品图片处理'
        },
        {
          title: '社交媒体内容制作',
          description: '制作精美的社交媒体图片和广告素材',
          example: 'Instagram帖子、Facebook广告、微信朋友圈图片'
        },
        {
          title: '证件照制作',
          description: '一键更换证件照背景色',
          example: '蓝底、红底、白底证件照快速生成'
        }
      ],
      industries: ['电子商务', '广告营销', '摄影工作室', '设计公司', '教育培训'],
      user_types: ['专业设计师', '营销人员', '小企业主', '个人用户']
    },
    
    community_reviews: {
      pros: [
        '抠图精度很高，毛发边缘处理出色',
        '界面简单易用，新手也能快速上手',
        '处理速度快，大大提高工作效率',
        '支持批量处理，适合大量图片处理需求',
        '客服响应及时，问题解决效率高'
      ],
      cons: [
        '免费版本有处理次数限制',
        '复杂背景的处理偶尔需要手动调整',
        '高分辨率图片处理需要付费版本',
        'API调用价格相对较高'
      ],
      user_feedback: [
        {
          rating: 5,
          comment: '作为电商运营，这个工具帮我节省了大量时间，抠图效果比我用PS做的还好！',
          author: '张设计师'
        },
        {
          rating: 4,
          comment: '总体很不错，但希望能增加更多背景模板选择。',
          author: '李营销'
        },
        {
          rating: 5,
          comment: '价格合理，功能强大，团队协作功能也很实用。',
          author: '王创意'
        }
      ],
      expert_review: {
        score: 4.3,
        summary: 'Nano Banana 在AI抠图领域表现优秀，特别是在边缘处理和速度方面有明显优势。',
        detailed_analysis: '经过专业测试，Nano Banana 的抠图精度达到92%，在同类工具中处于领先地位。其独有的边缘优化算法能够很好地处理毛发、透明物体等复杂情况。用户界面设计简洁，学习成本低。不足之处在于高级功能需要付费，且对于极其复杂的背景仍需要人工干预。'
      }
    },
    
    access_info: {
      pricing_plans: [
        {
          name: '免费版',
          price: '￥0/月',
          features: [
            '每月10次处理',
            '基础抠图功能',
            '标准画质输出',
            '社区支持'
          ]
        },
        {
          name: '专业版',
          price: '￥29/月',
          features: [
            '每月200次处理',
            '高级抠图算法',
            '高清画质输出',
            '批量处理',
            '优先客服支持'
          ],
          recommended: true
        },
        {
          name: '企业版',
          price: '￥199/月',
          features: [
            '无限次处理',
            'API接入',
            '团队协作功能',
            '专属客服',
            '定制化服务'
          ]
        }
      ],
      free_trial: {
        duration: '7天',
        limitations: ['每日最多5次处理', '输出图片带水印']
      },
      system_requirements: {
        platform: ['Web浏览器', 'iOS App', 'Android App'],
        browser: ['Chrome 80+', 'Safari 13+', 'Firefox 75+', 'Edge 80+'],
        other: ['稳定的网络连接', '建议上传图片不超过20MB']
      }
    },
    
    faq: [
      {
        question: '支持哪些图片格式？',
        answer: '支持 JPG、PNG、WEBP、TIFF 等主流格式，推荐使用 PNG 格式以获得最佳效果。',
        category: '基础使用'
      },
      {
        question: '处理后的图片质量如何？',
        answer: '免费版输出标准质量(1080p)，付费版支持原图质量输出，最高支持4K分辨率。',
        category: '图片质量'
      },
      {
        question: '如何获得更好的抠图效果？',
        answer: '建议上传清晰度高、主体与背景对比明显的图片。复杂背景可能需要手动微调。',
        category: '使用技巧'
      },
      {
        question: '是否提供API服务？',
        answer: '企业版用户可以使用我们的API服务，支持批量处理和系统集成。',
        category: '高级功能'
      },
      {
        question: '数据安全如何保障？',
        answer: '我们采用SSL加密传输，处理完成后24小时内自动删除用户上传的图片。',
        category: '安全隐私'
      }
    ]
  }
};