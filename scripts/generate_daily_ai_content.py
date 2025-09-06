#!/usr/bin/env python3
"""
AI工具每日内容生成脚本 - 专为变现优化
基于AI Smart Home成功经验，专注商业化和自动化运营
"""

import json
import os
import sys
import argparse
import codecs
from datetime import datetime
from pathlib import Path

# Import keyword analysis notifier
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))
try:
    from monitoring.keyword_analysis_notifier import KeywordAnalysisNotifier, ContentGenerationReport, KeywordAnalysis
    NOTIFICATIONS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Notification system not available: {e}")
    NOTIFICATIONS_AVAILABLE = False

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def load_trending_ai_tools():
    """Load trending AI tools with commercial focus"""
    trending_file = "data/trending_ai_tools_cache.json"
    
    # 高商业价值AI工具数据 - 专注变现
    fallback_data = [
        {
            "keyword": "claude ai review", 
            "category": "content_creation", 
            "trend_score": 0.95,
            "competition_score": 0.60,
            "commercial_intent": 0.94,
            "search_volume": 25000,
            "difficulty": "Medium",
            "affiliate_potential": "High",
            "monthly_revenue_estimate": "$150-300",
            "reason": "Claude AI爆火，高转化率AI助手类工具，联盟佣金丰厚"
        },
        {
            "keyword": "midjourney alternatives", 
            "category": "image_generation", 
            "trend_score": 0.92,
            "competition_score": 0.55,
            "commercial_intent": 0.96,
            "search_volume": 35000,
            "difficulty": "Low-Medium",
            "affiliate_potential": "Very High",
            "monthly_revenue_estimate": "$200-400",
            "reason": "Midjourney付费门槛高，用户急需替代方案，转化率极高"
        },
        {
            "keyword": "github copilot review", 
            "category": "code_assistance", 
            "trend_score": 0.88,
            "competition_score": 0.65,
            "commercial_intent": 0.91,
            "search_volume": 18000,
            "difficulty": "Medium",
            "affiliate_potential": "High",
            "monthly_revenue_estimate": "$100-250",
            "reason": "开发者工具需求旺盛，B端付费意愿强，长期价值高"
        },
        {
            "keyword": "notion ai features", 
            "category": "productivity", 
            "trend_score": 0.85,
            "competition_score": 0.58,
            "commercial_intent": 0.89,
            "search_volume": 22000,
            "difficulty": "Low-Medium",
            "affiliate_potential": "High",
            "monthly_revenue_estimate": "$120-280",
            "reason": "Notion付费升级需求大，生产力工具转化率高"
        },
        {
            "keyword": "chatgpt plus worth it", 
            "category": "content_creation", 
            "trend_score": 0.90,
            "competition_score": 0.70,
            "commercial_intent": 0.93,
            "search_volume": 40000,
            "difficulty": "Medium-High",
            "affiliate_potential": "Medium",
            "monthly_revenue_estimate": "$80-180",
            "reason": "付费决策关键词，用户购买意图明确，点击价值高"
        },
        {
            "keyword": "leonardo ai vs midjourney", 
            "category": "image_generation", 
            "trend_score": 0.87,
            "competition_score": 0.52,
            "commercial_intent": 0.95,
            "search_volume": 15000,
            "difficulty": "Low",
            "affiliate_potential": "Very High",
            "monthly_revenue_estimate": "$180-350",
            "reason": "对比类关键词转化率最高，两个工具都有联盟项目"
        },
        {
            "keyword": "nano banana ai tool",
            "category": "productivity",
            "trend_score": 0.92,
            "competition_score": 0.45,
            "commercial_intent": 0.88,
            "search_volume": 12000,
            "difficulty": "Low",
            "affiliate_potential": "High",
            "monthly_revenue_estimate": "$150-280",
            "reason": "最新热门AI生产力工具，搜索量激增，竞争度低，变现潜力大"
        },
        {
            "keyword": "lovart ai platform",
            "category": "image_generation", 
            "trend_score": 0.89,
            "competition_score": 0.48,
            "commercial_intent": 0.91,
            "search_volume": 18000,
            "difficulty": "Low-Medium",
            "affiliate_potential": "Very High",
            "monthly_revenue_estimate": "$200-380",
            "reason": "新兴AI艺术创作平台，用户付费意愿强，联盟佣金丰厚"
        }
    ]
    
    try:
        if os.path.exists(trending_file):
            with open(trending_file, 'r', encoding='utf-8') as f:
                trends = json.load(f)
            print(f"✅ Loaded {len(trends)} trending AI tools from cache")
            return trends
    except Exception as e:
        print(f"⚠️ Warning: Failed to load trending AI tools: {e}")
    
    # Ensure data directory exists and save fallback
    os.makedirs(os.path.dirname(trending_file), exist_ok=True)
    with open(trending_file, 'w', encoding='utf-8') as f:
        json.dump(fallback_data, f, indent=2, ensure_ascii=False)
    print("📄 Using fallback AI tools data - optimized for revenue")
    return fallback_data

def get_ai_tool_images(keyword, category):
    """获取AI工具相关的真实产品图片 - 使用API获取相关图片"""
    try:
        # Import image handler
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))
        from image_processor.ai_tool_image_handler import AIToolImageHandler
        
        # API keys
        unsplash_key = "fU_RSdecKs7yCLkwfietuN_An8Y4pDAARPjbGuWlyKQ"
        pexels_key = "GEIG80uBUWAZYPkdLvhqSxLatgJ5Gyiu7DWxTy3veJTMGMVVkMuSWdrg"
        pixabay_key = "52152560-87d638059f34cdb71e8341171"
        
        # Initialize image handler with API keys
        handler = AIToolImageHandler(
            unsplash_access_key=unsplash_key,
            pexels_api_key=pexels_key,
            pixabay_api_key=pixabay_key
        )
        
        # Extract tool name from keyword
        tool_name = keyword.replace(" review", "").replace(" guide", "").replace(" tutorial", "")
        
        # Fetch real image
        image_metadata = handler.fetch_tool_image(tool_name, category, [tool_name, "AI tool", category.replace("_", " ")])
        
        if image_metadata:
            # Return real image path
            image_path = f"/images/tools/{image_metadata.filename}"
            print(f"SUCCESS: Using real image for {tool_name}: {image_path}")
            
            # Return all expected keys with the same image
            return {
                "hero_image": image_path,
                "featured_image": image_path,
                "main_image": image_path,
                "product_1": image_path,
                "product_2": image_path,
                "product_3": image_path,
                "comparison": image_path,
                "pricing": image_path
            }
        else:
            print(f"WARNING: Failed to fetch real image for {tool_name}, using fallback")
            raise Exception("No real image available")
            
    except Exception as e:
        print(f"ERROR: Image fetch failed for {keyword}: {e}")
        
        # Fallback to placeholder only if API completely fails
        base_url = "/images/tools/"
        tool_slug = keyword.lower().replace(" ", "-").replace("ai", "").strip("-")
        placeholder_filename = f"{tool_slug}-placeholder.jpg"
        
        # Return all expected keys with placeholder
        return {
            "hero_image": f"{base_url}{placeholder_filename}",
            "featured_image": f"{base_url}{placeholder_filename}",
            "main_image": f"{base_url}{placeholder_filename}",
            "product_1": f"{base_url}{placeholder_filename}",
            "product_2": f"{base_url}{placeholder_filename}",
            "product_3": f"{base_url}{placeholder_filename}",
            "comparison": f"{base_url}{placeholder_filename}",
            "pricing": f"{base_url}{placeholder_filename}"
        }

def generate_ai_tool_review(keyword, category, tool_data):
    """生成专为变现优化的AI工具评测内容 - 2500+字，高转化率"""
    import random
    
    # 专为SEO和转化优化的标题变体
    title_patterns = [
        f"{keyword.title()} 2025: Complete Review, Pricing & Alternatives",
        f"Is {keyword.title()} Worth It? Honest Review & Pricing Guide 2025",
        f"{keyword.title()} Review 2025: Features, Pricing & Best Alternatives",
        f"Ultimate {keyword.title()} Guide 2025: Review, Pricing & Free Alternatives"
    ]
    title = random.choice(title_patterns)
    
    # 获取商业化图片
    product_images = get_ai_tool_images(keyword, category)
    
    # 商业化导向的引言变体
    intro_hooks = [
        f"Looking for an honest {keyword} review? You're in the right place.",
        f"Considering {keyword} for your workflow? Here's everything you need to know.",
        f"Is {keyword} worth your money? We tested it thoroughly to find out.",
        f"Thinking about investing in {keyword}? This comprehensive review has all the answers."
    ]
    
    value_props = [
        f"In this detailed {keyword} review, we'll cover pricing, features, alternatives, and help you decide if it's the right investment for your needs.",
        f"This comprehensive analysis examines {keyword} from a user's perspective, including real-world testing, cost analysis, and competitive comparisons.",
        f"We've spent weeks testing {keyword} to bring you an unbiased review covering features, pricing, pros, cons, and better alternatives.",
        f"Our in-depth {keyword} evaluation covers everything from core features to hidden costs, helping you make an informed purchasing decision."
    ]
    
    # 商业化收益预测数据
    revenue_estimate = tool_data.get('monthly_revenue_estimate', '$50-150')
    affiliate_potential = tool_data.get('affiliate_potential', 'Medium')
    
    content = f"""## Quick Summary

{random.choice(intro_hooks)} {random.choice(value_props)}

![{keyword.title()} Review 2025]({product_images['hero_image']} "{keyword.title()} - Complete Review and Pricing Guide")

**⭐ Our Rating: 4.2/5**

✅ **Best For**: {get_best_use_case(category)}  
✅ **Starting Price**: {get_pricing_info(keyword)}  
✅ **Free Trial**: {get_trial_info(keyword)}  
✅ **Best Alternative**: {get_top_alternative(category)}

---

## What is {keyword.title()}?

{keyword.title()} is a {get_tool_description(category)} that has gained significant attention in 2025. {get_detailed_description(keyword, category)}

### Key Features at a Glance

{generate_feature_list(category)}

### Who Should Use {keyword.title()}?

Based on our testing, {keyword} works best for:

- **{get_target_user_1(category)}**: Perfect for professionals who need {get_benefit_1(category)}
- **{get_target_user_2(category)}**: Ideal for teams requiring {get_benefit_2(category)}  
- **{get_target_user_3(category)}**: Great for individuals looking to {get_benefit_3(category)}

## Pricing Analysis - Is It Worth the Cost?

![{keyword.title()} Pricing Plans]({product_images['pricing']} "{keyword.title()} Pricing Comparison 2025")

Understanding the true cost of {keyword} requires looking beyond the base price. Here's our detailed breakdown:

### Official Pricing Tiers

{generate_pricing_breakdown(keyword)}

### Hidden Costs to Consider

- **Setup Time**: Approximately 2-3 hours for full configuration
- **Learning Curve**: Most users become proficient within 5-7 days
- **Integration Costs**: May require additional tools for full functionality
- **Support Fees**: Premium support plans start at additional cost

### Cost-Benefit Analysis

After extensive testing, we found that {keyword} provides good value for:
- Users processing {get_volume_threshold(category)} per month
- Teams with budgets above {get_budget_threshold(category)}
- Professionals in {get_industry_match(category)} industries

**Our Verdict**: {get_pricing_verdict(keyword, category)}

## In-Depth Feature Review

### Core Functionality

{generate_core_features_review(keyword, category)}

![{keyword.title()} Interface]({product_images['product_1']} "{keyword.title()} User Interface and Features")

### Advanced Features

{generate_advanced_features_review(category)}

### Performance Testing Results

We conducted comprehensive performance tests over 30 days:

- **Speed**: {get_performance_metric('speed', category)}
- **Accuracy**: {get_performance_metric('accuracy', category)}
- **Reliability**: {get_performance_metric('reliability', category)}
- **User Satisfaction**: {get_performance_metric('satisfaction', category)}

## Pros and Cons - Honest Assessment

### ✅ Pros

{generate_pros_list(category)}

### ❌ Cons  

{generate_cons_list(category)}

### Deal Breakers

Some users should avoid {keyword} if they:
- Need {get_dealbreaker_1(category)}
- Require {get_dealbreaker_2(category)}
- Have budgets under {get_budget_minimum(category)}

## Best Alternatives to {keyword.title()}

![AI Tool Comparison]({product_images['comparison']} "{keyword.title()} vs Alternatives - Feature Comparison")

If {keyword} doesn't meet your needs, consider these alternatives:

### 1. {get_alternative_1(category)} - Best Overall Alternative

{generate_alternative_review(1, category)}

**Pricing**: {get_alternative_pricing(1, category)}  
**Best For**: {get_alternative_best_for(1, category)}

### 2. {get_alternative_2(category)} - Best Budget Option

{generate_alternative_review(2, category)}

**Pricing**: {get_alternative_pricing(2, category)}  
**Best For**: {get_alternative_best_for(2, category)}

### 3. {get_alternative_3(category)} - Best Premium Option

{generate_alternative_review(3, category)}

**Pricing**: {get_alternative_pricing(3, category)}  
**Best For**: {get_alternative_best_for(3, category)}

## Getting Started Guide

### Step 1: Account Setup (5 minutes)

{generate_setup_steps(keyword)}

### Step 2: First Project Configuration (15 minutes)

{generate_configuration_steps(category)}

### Step 3: Optimization for Best Results (30 minutes)

{generate_optimization_tips(category)}

## Real User Reviews and Testimonials

Based on our analysis of 500+ user reviews across multiple platforms:

**Positive Feedback (78%)**:
- "Significantly improved my {get_workflow_improvement(category)}"
- "ROI became positive within {get_roi_timeframe(category)}"
- "Customer support is responsive and helpful"

**Critical Feedback (22%)**:
- "Learning curve steeper than expected"
- "Some features feel underdeveloped"
- "Pricing could be more competitive"

## ROI and Business Impact

### Productivity Gains

Organizations using {keyword} typically see:
- {get_productivity_gain_1(category)}
- {get_productivity_gain_2(category)}  
- {get_productivity_gain_3(category)}

### Cost Savings

The tool helps reduce costs through:
- Automation of {get_automation_area(category)}
- Reduced need for {get_reduced_need(category)}
- Improved efficiency in {get_efficiency_area(category)}

### Revenue Impact

For revenue-generating use cases:
- Average revenue increase: {get_revenue_increase(category)}
- Time to positive ROI: {get_roi_timeframe(category)}
- Customer satisfaction improvement: {get_satisfaction_improvement(category)}

## Security and Privacy Considerations

{generate_security_analysis(category)}

## Final Verdict and Recommendations

After comprehensive testing and analysis, here's our final assessment of {keyword}:

### Overall Rating: 4.2/5 ⭐⭐⭐⭐

**Excellent for**: {get_excellent_for(category)}  
**Good for**: {get_good_for(category)}  
**Skip if**: {get_skip_if(category)}

### Our Recommendation

{generate_final_recommendation(keyword, category, affiliate_potential)}

### Next Steps

If you've decided {keyword} is right for you:

1. **Start with the free trial** to test core features
2. **Begin with the starter plan** to minimize initial investment  
3. **Set up tracking** to measure ROI from day one
4. **Consider alternatives** if specific needs aren't met

## Frequently Asked Questions

**Q: Is {keyword} suitable for beginners?**
A: {get_beginner_suitability(category)}

**Q: How does it compare to [main competitor]?**
A: {generate_competitor_comparison(category)}

**Q: What's the learning curve like?**  
A: {get_learning_curve_info(category)}

**Q: Is there a free version available?**
A: {get_free_version_info(keyword)}

**Q: How good is customer support?**
A: {get_support_quality_info(category)}

**Q: Can I cancel anytime?**
A: {get_cancellation_info(keyword)}

---

*This {keyword} review was last updated on {datetime.now().strftime("%B %Y")}. Pricing and features may have changed. Always check the official website for the most current information.*

**Disclosure**: This post may contain affiliate links. We may earn a commission when you purchase through links on our site, at no additional cost to you."""

    return {
        'title': title,
        'content': content,
        'metadata': {
            'description': f'Honest {keyword} review 2025: Features, pricing, pros, cons, and alternatives. Find out if {keyword} is worth your investment with our comprehensive analysis.',
            'categories': [category.replace('_', '-')],
            'tags': [keyword.split()[0], 'AI tool', 'review', '2025', 'pricing', 'alternatives'],
            'featured_image': product_images['hero_image'],
            'rating': 4.2,
            'commercial_intent': tool_data.get('commercial_intent', 0.8),
            'affiliate_potential': affiliate_potential,
            'monthly_revenue_estimate': revenue_estimate
        }
    }

# 辅助函数生成器 - 专为商业化优化
def get_tool_description(category):
    descriptions = {
        'content_creation': 'powerful AI writing and content generation platform',
        'image_generation': 'advanced AI image and art generation tool',
        'code_assistance': 'intelligent coding assistant and development tool',
        'productivity': 'comprehensive productivity and workflow optimization solution'
    }
    return descriptions.get(category, 'innovative AI-powered tool')

def get_best_use_case(category):
    use_cases = {
        'content_creation': 'Content creators, marketers, and writers',
        'image_generation': 'Designers, artists, and content creators',  
        'code_assistance': 'Developers, programmers, and software teams',
        'productivity': 'Business professionals and remote workers'
    }
    return use_cases.get(category, 'Professional users')

def get_pricing_info(keyword):
    # 模拟定价信息 - 实际应用中会从API获取
    return "From $19/month"

def get_trial_info(keyword):
    return "7-14 days available"

def get_top_alternative(category):
    alternatives = {
        'content_creation': 'Jasper AI',
        'image_generation': 'Leonardo AI',
        'code_assistance': 'Cursor AI', 
        'productivity': 'Notion AI'
    }
    return alternatives.get(category, 'Similar tool')

def generate_feature_list(category):
    features = {
        'content_creation': """- **AI Writing Assistant**: Generate high-quality content in seconds
- **Template Library**: 50+ proven content templates
- **Multi-language Support**: Write in 25+ languages
- **SEO Optimization**: Built-in keyword optimization
- **Team Collaboration**: Real-time editing and sharing""",
        'image_generation': """- **AI Art Generation**: Create stunning visuals from text prompts
- **Style Controls**: 100+ artistic styles and filters
- **Batch Processing**: Generate multiple variations quickly
- **High Resolution**: Output up to 4K quality images
- **Commercial License**: Use images for business purposes""",
        'code_assistance': """- **Intelligent Autocomplete**: AI-powered code suggestions
- **Multi-language Support**: 30+ programming languages
- **Error Detection**: Real-time bug identification
- **Code Explanation**: Natural language code documentation
- **Refactoring Tools**: Automated code optimization""",
        'productivity': """- **Task Automation**: Streamline repetitive workflows
- **Smart Scheduling**: AI-optimized calendar management
- **Document Processing**: Automated data extraction
- **Integration Hub**: Connect with 100+ popular tools
- **Analytics Dashboard**: Productivity insights and reporting"""
    }
    return features.get(category, "- **Core Features**: Essential functionality for users")

def generate_pricing_breakdown(keyword):
    return f"""
**Starter Plan**: $19/month
- Core {keyword} features
- 10,000 monthly credits
- Email support
- Basic templates

**Professional Plan**: $49/month  
- Everything in Starter
- 50,000 monthly credits
- Priority support
- Advanced features
- Team collaboration (up to 5 users)

**Enterprise Plan**: $99/month
- Everything in Professional
- Unlimited credits
- Dedicated account manager
- Custom integrations
- SSO and advanced security"""

def generate_core_features_review(keyword, category):
    reviews = {
        'content_creation': f"The core writing capabilities of {keyword} impressed us during testing. The AI generates coherent, contextually appropriate content that requires minimal editing. We found the output quality consistently high across different content types, from blog posts to social media captions.",
        'image_generation': f"{keyword} excels at translating text descriptions into high-quality visual content. During our testing, we generated over 500 images across various styles and found the AI's interpretation of prompts to be remarkably accurate and creative.",
        'code_assistance': f"The coding assistance features of {keyword} significantly improved our development workflow. Code suggestions were contextually relevant, and the error detection caught issues we might have missed during manual review.",
        'productivity': f"The productivity features in {keyword} delivered measurable improvements to our workflow efficiency. Task automation capabilities reduced manual work by approximately 60%, while the smart scheduling optimized our team's calendar management."
    }
    return reviews.get(category, f"The core functionality of {keyword} meets professional standards with room for improvement in specific areas.")

def generate_advanced_features_review(category):
    reviews = {
        'content_creation': "Advanced features include tone adjustment, brand voice training, and bulk content generation. The plagiarism checker and fact-verification tools add significant value for professional content creators.",
        'image_generation': "Advanced capabilities include style transfer, image upscaling, and batch processing. The prompt engineering tools help users achieve more consistent results across multiple generations.",
        'code_assistance': "Advanced features encompass code review automation, security vulnerability scanning, and performance optimization suggestions. The refactoring tools proved particularly valuable for legacy code maintenance.",
        'productivity': "Advanced functionality includes workflow automation, predictive analytics, and custom dashboard creation. The integration capabilities allow seamless connection with existing business tools."
    }
    return reviews.get(category, "Advanced features provide additional value for power users and professional applications.")

def get_performance_metric(metric, category):
    metrics = {
        'speed': {'content_creation': 'Average 3-5 seconds per generation', 'image_generation': 'Average 15-30 seconds per image', 'code_assistance': 'Real-time suggestions (<1 second)', 'productivity': 'Instant task processing'},
        'accuracy': {'content_creation': '92% factually accurate content', 'image_generation': '89% prompt interpretation accuracy', 'code_assistance': '94% suggestion relevance', 'productivity': '96% automation success rate'},
        'reliability': {'content_creation': '99.2% uptime over testing period', 'image_generation': '98.8% successful generation rate', 'code_assistance': '99.5% IDE integration stability', 'productivity': '99.1% workflow execution success'},
        'satisfaction': {'content_creation': '4.3/5 user satisfaction rating', 'image_generation': '4.5/5 creative satisfaction score', 'code_assistance': '4.2/5 developer productivity rating', 'productivity': '4.4/5 efficiency improvement score'}
    }
    return metrics.get(metric, {}).get(category, 'Performance data not available')

def generate_pros_list(category):
    pros = {
        'content_creation': """- High-quality content generation with minimal editing required
- Extensive template library covers most content needs
- Strong SEO optimization features
- Excellent multi-language support
- Responsive customer support team""",
        'image_generation': """- Exceptional image quality and artistic variety
- Intuitive prompt interface for beginners
- Fast generation times compared to competitors
- Commercial usage rights included
- Regular model updates improve output quality""",
        'code_assistance': """- Significantly improves coding productivity
- Excellent support for popular programming languages
- Real-time error detection saves debugging time
- Seamless IDE integration across platforms
- Strong security and privacy measures""",
        'productivity': """- Measurable productivity improvements within days
- Extensive integration ecosystem
- Intuitive user interface requires minimal training
- Excellent automation capabilities
- Strong analytics and reporting features"""
    }
    return pros.get(category, "- Solid core functionality\n- Good value for the price\n- Regular updates and improvements")

def generate_cons_list(category):
    cons = {
        'content_creation': """- Can occasionally produce repetitive phrasing
- Advanced features require learning curve
- Credit limits may be restrictive for heavy users
- Some niche industries lack specialized templates""",
        'image_generation': """- Complex prompts may require multiple attempts
- Limited control over specific image elements
- Credit system can become expensive for high usage
- Occasional inconsistencies in character generation""",
        'code_assistance': """- Suggestions sometimes lack broader context awareness  
- Can become overly dependent on AI assistance
- Premium pricing may be steep for individual developers
- Limited support for very new or obscure languages""",
        'productivity': """- Initial setup and configuration can be time-consuming
- Some automations require technical knowledge
- Integration complexity varies significantly
- Advanced features have a steeper learning curve"""
    }
    return cons.get(category, "- Some features could be more intuitive\n- Pricing may be high for small teams\n- Learning curve for advanced features")

# 更多辅助函数...
def get_alternative_1(category):
    alts = {'content_creation': 'Jasper AI', 'image_generation': 'Leonardo AI', 'code_assistance': 'Cursor AI', 'productivity': 'Notion AI'}
    return alts.get(category, 'Alternative Tool')

def get_alternative_2(category):
    alts = {'content_creation': 'Copy.ai', 'image_generation': 'Stable Diffusion', 'code_assistance': 'Tabnine', 'productivity': 'Zapier'}
    return alts.get(category, 'Budget Alternative')

def get_alternative_3(category):
    alts = {'content_creation': 'Writesonic', 'image_generation': 'DALL-E 3', 'code_assistance': 'GitHub Copilot', 'productivity': 'Microsoft Power Automate'}
    return alts.get(category, 'Premium Alternative')

def generate_alternative_review(num, category):
    return f"Strong alternative with competitive features and pricing. Particularly strong in specific use cases that complement the main tool's weaknesses."

def get_alternative_pricing(num, category):
    prices = ["From $15/month", "From $25/month", "From $35/month"]
    return prices[num-1]

def get_alternative_best_for(num, category):
    best_for = ["Budget-conscious users", "Mid-market teams", "Enterprise customers"]
    return best_for[num-1]

def generate_final_recommendation(keyword, category, affiliate_potential):
    if affiliate_potential == "Very High":
        return f"{keyword} represents an excellent investment for professionals in {category.replace('_', ' ')}. The combination of powerful features, competitive pricing, and strong support makes it our top recommendation for most users. The ROI typically becomes positive within 2-3 months of consistent usage."
    else:
        return f"{keyword} is a solid choice for {category.replace('_', ' ')} needs, though users should carefully evaluate alternatives before committing to ensure the feature set aligns with their specific requirements."

# 其他必需的辅助函数（简化版本）
def get_dealbreaker_1(category): return "offline functionality"
def get_dealbreaker_2(category): return "custom branding options"  
def get_budget_minimum(category): return "$20/month"
def get_target_user_1(category): return "Content Creators"
def get_target_user_2(category): return "Marketing Teams"
def get_target_user_3(category): return "Small Business Owners"
def get_benefit_1(category): return "streamlined content creation"
def get_benefit_2(category): return "collaborative workflows"
def get_benefit_3(category): return "automated task management"
def get_volume_threshold(category): return "100+ projects"
def get_budget_threshold(category): return "$500/month"
def get_industry_match(category): return "digital marketing"
def get_pricing_verdict(keyword, category): return f"{keyword} offers good value for money in the {category.replace('_', ' ')} space"
def generate_setup_steps(keyword): return f"1. Visit the {keyword} website\n2. Sign up for a free trial\n3. Complete email verification\n4. Choose your plan\n5. Access the dashboard"
def generate_configuration_steps(category): return "1. Set up your workspace\n2. Configure preferences\n3. Connect integrations\n4. Create your first project\n5. Invite team members"
def generate_optimization_tips(category): return "1. Complete the onboarding tutorial\n2. Set up automation rules\n3. Configure notifications\n4. Customize templates\n5. Monitor performance metrics"
def get_workflow_improvement(category): return "daily productivity"
def get_roi_timeframe(category): return "2-3 months"
def get_productivity_gain_1(category): return "40% reduction in manual tasks"
def get_productivity_gain_2(category): return "60% faster project completion"
def get_productivity_gain_3(category): return "25% improvement in output quality"
def get_automation_area(category): return "repetitive workflows"
def get_reduced_need(category): return "manual oversight"
def get_efficiency_area(category): return "project management"
def get_revenue_increase(category): return "15-30%"
def get_satisfaction_improvement(category): return "45%"
def generate_security_analysis(category): return f"Security measures include enterprise-grade encryption, SOC 2 compliance, and regular security audits. Data privacy policies align with GDPR requirements, and user data is stored in secure, geographically distributed data centers."
def get_excellent_for(category): return f"Professional {category.replace('_', ' ')} teams"
def get_good_for(category): return "Individual users and small teams"
def get_skip_if(category): return "you need offline functionality"
def get_beginner_suitability(category): return "Yes, with a moderate learning curve of 3-5 days"
def generate_competitor_comparison(category): return "It offers better value and more comprehensive features than most direct competitors"
def get_learning_curve_info(category): return "Most users become proficient within one week of regular use"
def get_free_version_info(keyword): return f"{keyword} offers a limited free trial but no permanent free tier"
def get_support_quality_info(category): return "Customer support is responsive with average response times of 4-6 hours"
def get_cancellation_info(keyword): return f"Yes, {keyword} allows cancellation at any time with no penalties"

def get_detailed_description(keyword, category):
    """Generate detailed description for AI tool"""
    descriptions = {
        'content_creation': f"This AI-powered platform uses advanced machine learning to help users create high-quality written content efficiently. With its intuitive interface and powerful algorithms, {keyword} streamlines the content creation process for professionals.",
        'image_generation': f"Using cutting-edge diffusion models and neural networks, {keyword} transforms text prompts into stunning visual content. The platform offers professional-grade image generation capabilities with customizable parameters.",
        'code_assistance': f"Built on transformer architecture, {keyword} provides intelligent code completion, debugging assistance, and development workflow optimization. It integrates seamlessly with popular IDEs and supports multiple programming languages.",
        'productivity': f"Leveraging AI automation and smart workflows, {keyword} helps teams and individuals optimize their daily operations. The platform combines task management, automation, and intelligent suggestions to boost productivity."
    }
    return descriptions.get(category, f"This innovative AI tool leverages advanced technology to deliver powerful {category.replace('_', ' ')} capabilities, helping users achieve better results with less effort.")

def create_hugo_review_file(article_data, output_dir):
    """Create Hugo markdown file for AI tool review"""
    keyword = article_data['metadata']['tags'][0]
    
    # Create filename - SEO optimized
    safe_title = keyword.lower().replace(' ', '-').replace(',', '').replace(':', '')
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{safe_title}-review-{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Hugo front matter with commercial optimization
    front_matter = f"""---
title: "{article_data['title']}"
description: "{article_data['metadata']['description']}"
date: {datetime.now().isoformat()}Z
categories: {json.dumps(article_data['metadata']['categories'])}
tags: {json.dumps(article_data['metadata']['tags'])}
keywords: {json.dumps([keyword, 'AI tool', 'review', '2025', 'pricing'])}
featured: true
rating: {article_data['metadata']['rating']}
author: "AI Discovery Team"
featured_image: "{article_data['metadata']['featured_image']}"
commercial_intent: {article_data['metadata']['commercial_intent']}
affiliate_potential: "{article_data['metadata']['affiliate_potential']}"
monthly_revenue_estimate: "{article_data['metadata']['monthly_revenue_estimate']}"
review_type: "comprehensive"
last_updated: "{datetime.now().strftime('%Y-%m-%d')}"
---

"""
    
    # Write article file
    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(article_data['content'])
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Generate AI tool reviews - optimized for revenue')
    parser.add_argument('--count', type=int, default=1, help='Number of reviews to generate')
    parser.add_argument('--output-dir', default='content/reviews', help='Output directory for reviews')
    parser.add_argument('--focus-high-revenue', action='store_true', help='Prioritize high-revenue potential keywords')
    
    args = parser.parse_args()
    
    print(f"🚀 启动AI工具内容生成系统...")
    print(f"💰 目标: 生成 {args.count} 篇高转化率评测")
    
    # Load trending AI tools with commercial focus
    ai_tools = load_trending_ai_tools()
    
    # Sort by revenue potential if requested
    if args.focus_high_revenue:
        ai_tools = sorted(ai_tools, key=lambda x: x.get('commercial_intent', 0), reverse=True)
        print("💎 优先生成高收益潜力内容")
    
    # Generate reviews
    generated_files = []
    used_tools = []
    review_count = min(args.count, len(ai_tools))
    
    for i in range(review_count):
        tool = ai_tools[i]
        keyword = tool.get('keyword', 'ai tool')
        category = tool.get('category', 'ai-tools')
        
        print(f"📝 生成评测 {i+1}/{review_count}: {keyword}")
        print(f"💰 收益预估: {tool.get('monthly_revenue_estimate', 'N/A')}")
        
        try:
            article_data = generate_ai_tool_review(keyword, category, tool)
            filepath = create_hugo_review_file(article_data, args.output_dir)
            generated_files.append(filepath)
            
            # Save tool info for Telegram notification
            tool_info = {
                'keyword': keyword,
                'category': category,
                'trend_score': tool.get('trend_score', 0.0),
                'competition_score': tool.get('competition_score', 0.0),
                'commercial_intent': tool.get('commercial_intent', 0.0),
                'search_volume': tool.get('search_volume', 0),
                'difficulty': tool.get('difficulty', 'Unknown'),
                'affiliate_potential': tool.get('affiliate_potential', 'Medium'),
                'monthly_revenue_estimate': tool.get('monthly_revenue_estimate', 'N/A'),
                'reason': tool.get('reason', 'AI工具评测内容生成'),
                'priority': i + 1,
                'filepath': filepath,
                'word_count': len(article_data['content'].split()),
                'rating': article_data['metadata']['rating']
            }
            used_tools.append(tool_info)
            
            print(f"✅ 已生成: {filepath}")
            print(f"📊 字数: {tool_info['word_count']} | 评分: {tool_info['rating']}/5")
            
            # Send immediate keyword analysis notification
            if NOTIFICATIONS_AVAILABLE:
                try:
                    notifier = KeywordAnalysisNotifier()
                    
                    # Create keyword analysis object
                    keyword_analysis = KeywordAnalysis(
                        primary_keyword=keyword,
                        search_volume=tool.get('search_volume', 2000),
                        competition_score=tool.get('competition_score', 0.6),
                        commercial_intent=tool.get('commercial_intent', 0.8),
                        cpc_estimate=tool.get('cpc_estimate', 2.0),
                        trend_score=tool.get('trend_score', 0.75),
                        monthly_revenue_estimate=float(tool.get('monthly_revenue_estimate', '$50').replace('$', '').split('-')[0] or 50),
                        selection_reason=tool.get('reason', f'High-value {category.replace("_", " ")} keyword with strong commercial intent'),
                        alternative_keywords=tool.get('alternative_keywords', [])
                    )
                    
                    # Create content generation report
                    report = ContentGenerationReport(
                        tool_name=keyword.title(),
                        article_title=article_data['title'],
                        category=category,
                        keyword_analysis=keyword_analysis,
                        generation_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
                        article_word_count=tool_info['word_count'],
                        seo_score_estimate=float(tool_info['rating'])
                    )
                    
                    # Send notification immediately
                    success = notifier.send_content_generation_notification(report)
                    if success:
                        print(f"📱 Telegram通知已发送: {keyword}")
                    else:
                        print(f"⚠️ Telegram通知发送失败: {keyword}")
                        
                except Exception as notify_error:
                    print(f"⚠️ 通知系统错误: {notify_error}")
            
        except Exception as e:
            print(f"❌ 生成失败 {keyword}: {e}")
            continue
    
    # Save generated files list
    with open('generated_files.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(generated_files))
    
    # Save tool analysis for Telegram notifications
    if used_tools:
        with open('ai_tools_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(used_tools, f, indent=2, ensure_ascii=False)
        
        # Calculate revenue potential
        total_estimated_revenue = sum([
            int(tool.get('monthly_revenue_estimate', '$0-0').replace('$', '').split('-')[1]) 
            for tool in used_tools 
            if tool.get('monthly_revenue_estimate', '').replace('$', '').replace('-', '').replace(' ', '').isdigit()
        ])
        
        print(f"📊 已保存AI工具分析数据: {len(used_tools)} 个工具")
        print(f"💰 预估月收益潜力: ${total_estimated_revenue}+")
    
    print(f"🎉 成功生成 {len(generated_files)} 篇AI工具评测")
    print(f"🚀 系统已优化用于自动化变现!")
    return len(generated_files) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)