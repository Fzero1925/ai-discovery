#!/usr/bin/env python3
"""
Multi-Source Keywords Generator
整合多个免费数据源生成AI工具关键词和争议话题检测
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加模块路径
sys.path.append('.')
sys.path.append('modules')

def main():
    try:
        print("🚀 Starting multi-source keyword analysis...")
        
        # 导入多源检测器
        from trending_detector.multi_source_detector import MultiSourceTrendDetector, TrendingTopic
        
        # 初始化检测器
        detector = MultiSourceTrendDetector()
        
        # 检测热门话题
        trending_topics = detector.get_all_trending_topics(limit=25)
        
        if not trending_topics:
            print("⚠️ No trending topics detected, falling back to basic system")
            return False
        
        # 转换为关键词格式
        keywords_data = convert_topics_to_keywords(trending_topics)
        
        # 保存关键词数据
        save_keywords_data(keywords_data)
        
        # 保存通知数据
        save_notification_data(trending_topics, keywords_data)
        
        print(f"✅ Multi-source analysis completed - {len(keywords_data)} keywords generated")
        return True
        
    except Exception as e:
        print(f"❌ Multi-source analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def convert_topics_to_keywords(topics):
    """将trending topics转换为关键词格式"""
    keywords_data = []
    
    for topic in topics:
        # 计算月收入估算
        monthly_revenue = calculate_monthly_revenue(topic)
        
        # 确定困难度
        difficulty = determine_difficulty(topic.score, topic.controversy_score)
        
        # 生成选择原因
        reason = generate_selection_reason(topic)
        
        keyword_entry = {
            "keyword": topic.keyword,
            "category": categorize_keyword(topic.keyword),
            "trend_score": topic.score,
            "related_queries": topic.related_terms,
            "search_volume": estimate_search_volume(topic.score),
            "commercial_intent": calculate_commercial_intent(topic),
            "difficulty": difficulty,
            "monthly_revenue_estimate": monthly_revenue,
            "reason": reason,
            "is_trending_topic": topic.controversy_score > 20 or topic.score > 80,
            "controversy_score": topic.controversy_score,
            "data_sources": [topic.source],
            "sentiment": topic.sentiment,
            "last_updated": datetime.now().isoformat()
        }
        
        keywords_data.append(keyword_entry)
    
    return keywords_data

def calculate_monthly_revenue(topic):
    """计算月收入估算"""
    base_revenue = topic.score * 5  # 基础收入
    controversy_bonus = topic.controversy_score * 3  # 争议话题奖励
    total_potential = base_revenue + controversy_bonus
    
    # 收入区间
    min_revenue = max(50, int(total_potential * 0.8))
    max_revenue = int(total_potential * 1.5)
    
    return f"${min_revenue}-{max_revenue}"

def determine_difficulty(score, controversy_score):
    """确定关键词难度"""
    combined_score = score + (controversy_score * 0.5)
    
    if combined_score >= 90:
        return "High"
    elif combined_score >= 60:
        return "Medium"
    else:
        return "Low"

def generate_selection_reason(topic):
    """生成关键词选择原因"""
    reasons = []
    
    # 基础原因
    category = categorize_keyword(topic.keyword)
    if topic.score >= 80:
        reasons.append(f"This keyword shows high competition with growing search trends in the {category} category")
    elif topic.score >= 50:
        reasons.append(f"This keyword shows medium competition with strong search trends in the {category} category")
    else:
        reasons.append(f"This keyword shows low competition with growing search trends in the {category} category")
    
    # 添加数据源信息
    if 'reddit' in topic.source:
        reasons.append("with strong community engagement on Reddit")
    elif 'news' in topic.source:
        reasons.append("with recent news coverage")
    elif 'hackernews' in topic.source:
        reasons.append("with developer community interest")
    
    # 争议检测
    if topic.controversy_score > 30:
        controversy_terms = ", ".join(topic.related_terms[:3])
        reasons.append(f"**TRENDING CONTROVERSY DETECTED** - Recent surge in problem-related queries (score: {topic.controversy_score})")
        reasons.append("making this highly valuable for capturing user attention and providing timely solutions")
    
    # 商业价值
    if topic.sentiment == 'negative':
        reasons.append("with excellent opportunity for solution-oriented content")
    
    reason = ", ".join(reasons) + ", making it ideal for our AI tools directory targeting"
    
    # 添加商业潜力评估
    commercial_intent = calculate_commercial_intent(topic)
    if commercial_intent > 0.8:
        reason += " with excellent commercial potential"
    elif commercial_intent > 0.6:
        reason += " with strong commercial potential"
    else:
        reason += " with moderate commercial potential"
    
    return reason + "."

def categorize_keyword(keyword):
    """将关键词分类"""
    keyword_lower = keyword.lower()
    
    content_tools = ['chatgpt', 'claude', 'jasper', 'copy.ai', 'writesonic', 'perplexity', 'character.ai']
    image_tools = ['midjourney', 'dall-e', 'stable diffusion', 'firefly']
    code_tools = ['copilot', 'codewhisperer', 'tabnine', 'codeium']
    productivity_tools = ['notion', 'todoist', 'zapier', 'calendly']
    
    if any(tool in keyword_lower for tool in content_tools):
        return "content_creation"
    elif any(tool in keyword_lower for tool in image_tools):
        return "image_generation"
    elif any(tool in keyword_lower for tool in code_tools):
        return "code_assistance"
    elif any(tool in keyword_lower for tool in productivity_tools):
        return "productivity"
    else:
        return "content_creation"  # 默认分类

def estimate_search_volume(score):
    """估算搜索量"""
    # 基于分数生成搜索量
    base_volume = score * 1000
    variation = int(base_volume * 0.3)  # 30%变化
    
    min_volume = base_volume - variation
    max_volume = base_volume + variation
    
    return max(100, min_volume)

def calculate_commercial_intent(topic):
    """计算商业意图分数"""
    commercial_keywords = ['pricing', 'cost', 'buy', 'purchase', 'subscription', 'plan', 'review', 'vs', 'alternative', 'best']
    
    text_combined = f"{topic.keyword} {' '.join(topic.related_terms)}".lower()
    
    # 基础商业意图分数
    base_score = 0.5
    
    # 检查商业关键词
    commercial_count = sum(1 for kw in commercial_keywords if kw in text_combined)
    commercial_bonus = min(0.4, commercial_count * 0.1)
    
    # 争议话题通常有更高商业价值
    controversy_bonus = min(0.2, topic.controversy_score * 0.002)
    
    total_score = base_score + commercial_bonus + controversy_bonus
    return min(1.0, total_score)

def save_keywords_data(keywords_data):
    """保存关键词数据"""
    with open('daily_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(keywords_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved {len(keywords_data)} keywords to daily_keywords.json")

def save_notification_data(topics, keywords_data):
    """保存通知数据"""
    if not topics or not keywords_data:
        return
    
    # 选择最具争议性或最热门的话题
    primary_topic = max(topics, key=lambda x: x.controversy_score + x.score)
    primary_keyword = next((kw for kw in keywords_data if kw['keyword'] == primary_topic.keyword), keywords_data[0])
    
    notification_data = {
        "keyword_data": {
            "keyword": primary_keyword["keyword"],
            "trend_score": primary_keyword["trend_score"],
            "controversy_score": primary_keyword["controversy_score"],
            "monthly_revenue_estimate": primary_keyword["monthly_revenue_estimate"],
            "difficulty": primary_keyword["difficulty"],
            "commercial_intent": primary_keyword["commercial_intent"],
            "reason": primary_keyword["reason"],
            "data_sources": primary_keyword.get("data_sources", ["multi-source"]),
            "related_queries": primary_keyword["related_queries"],
            "sentiment": primary_keyword.get("sentiment", "neutral"),
            "is_trending_topic": primary_keyword["is_trending_topic"]
        },
        "content_data": {
            "total_topics": len(topics),
            "total_keywords": len(keywords_data),
            "controversy_detected": any(t.controversy_score > 20 for t in topics),
            "sources_used": list(set(topic.source for topic in topics)),
            "avg_controversy_score": sum(t.controversy_score for t in topics) / len(topics),
            "high_value_keywords": len([kw for kw in keywords_data if kw["trend_score"] > 80]),
            "generation_timestamp": datetime.now().isoformat()
        },
        "trending_analysis": {
            "top_controversies": [
                {
                    "keyword": t.keyword,
                    "controversy_score": t.controversy_score,
                    "source": t.source,
                    "content_snippet": t.content_snippet[:100]
                }
                for t in sorted(topics, key=lambda x: x.controversy_score, reverse=True)[:3]
                if t.controversy_score > 10
            ],
            "multi_source_validation": len(set(topic.source for topic in topics)) > 1,
            "real_time_data": True
        }
    }
    
    with open('notification_data.json', 'w', encoding='utf-8') as f:
        json.dump(notification_data, f, indent=2, ensure_ascii=False)
    
    print("📢 Notification data prepared for enhanced Telegram alerts")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)