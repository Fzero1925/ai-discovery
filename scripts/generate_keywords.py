#!/usr/bin/env python3
"""
AI Discovery - Enhanced Keyword Generation with Trending Topics Detection
支持热门话题检测，如Claude降智商等争议性话题
"""

import sys
import json
import random
from pathlib import Path

# Add modules to path
sys.path.append('modules')

try:
    from keyword_tools.ai_tool_keyword_analyzer import AIToolKeywordAnalyzer
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def detect_trending_controversies(analyzer, keywords):
    """
    检测热门争议话题，如工具性能下降、问题等
    """
    controversy_keywords = [
        "bug", "issue", "problem", "worse", "downgrade", 
        "智商", "降智", "性能下降", "问题", "故障"
    ]
    
    trending_controversies = []
    
    for kw in keywords:
        # 检查是否有争议相关的查询
        controversy_score = 0
        controversy_queries = []
        
        for query in kw.related_queries:
            query_lower = query.lower()
            for controversy_term in controversy_keywords:
                if controversy_term in query_lower:
                    controversy_score += 10
                    controversy_queries.append(query)
        
        # 如果发现争议话题，提升优先级
        if controversy_score > 0:
            kw.trend_score += controversy_score  # 提升趋势分数
            trending_controversies.append({
                'keyword': kw.keyword,
                'controversy_score': controversy_score,
                'controversy_queries': controversy_queries
            })
    
    return trending_controversies

def generate_enhanced_reason(kw, controversies):
    """
    生成增强的关键词选择理由，包含热门话题信息
    """
    base_reason = f"This keyword shows {kw.competition_level.lower()} competition with growing search trends in the {kw.category.replace('_', ' ')} category"
    
    # 检查是否是争议话题
    is_controversy = any(c['keyword'] == kw.keyword for c in controversies)
    
    if is_controversy:
        controversy_info = next(c for c in controversies if c['keyword'] == kw.keyword)
        reason = f"{base_reason}. **TRENDING CONTROVERSY DETECTED** - Recent surge in problem-related queries (score: {controversy_info['controversy_score']}), making this highly valuable for capturing user attention and providing timely solutions."
    else:
        reason = f"{base_reason}, making it ideal for our AI tools directory targeting with strong commercial potential."
    
    return reason

def main():
    print("Analyzing trending AI tools and hot topics...")
    
    try:
        analyzer = AIToolKeywordAnalyzer()
        keywords = analyzer.get_daily_ai_keywords()
        
        print(f"Found {len(keywords)} trending keywords")
        for kw in keywords[:5]:
            print(f"  - {kw.keyword} (Score: {kw.trend_score})")
        
        # 检测争议话题
        controversies = detect_trending_controversies(analyzer, keywords)
        if controversies:
            print(f"HOTFIRE Detected {len(controversies)} trending controversies:")
            for controversy in controversies:
                print(f"  - {controversy['keyword']} (Controversy Score: {controversy['controversy_score']})")
        
        # 保存增强的关键词数据
        enhanced_keywords = []
        for kw in keywords:
            enhanced_reason = generate_enhanced_reason(kw, controversies)
            
            keyword_data = {
                'keyword': kw.keyword,
                'category': kw.category,
                'trend_score': kw.trend_score,
                'related_queries': kw.related_queries,
                'search_volume': int(kw.trend_score * 1000 + random.randint(500, 2000)),
                'commercial_intent': min(1.0, kw.trend_score / 100 + random.uniform(0.3, 0.7)),
                'difficulty': kw.competition_level,
                'monthly_revenue_estimate': f"${random.randint(50, 300)}-{random.randint(350, 800)}",
                'reason': enhanced_reason,
                'is_trending_topic': any(c['keyword'] == kw.keyword for c in controversies),
                'controversy_score': next((c['controversy_score'] for c in controversies if c['keyword'] == kw.keyword), 0)
            }
            enhanced_keywords.append(keyword_data)
        
        # 按争议分数和趋势分数排序
        enhanced_keywords.sort(key=lambda x: (x['controversy_score'], x['trend_score']), reverse=True)
        
        # 保存到文件
        with open('daily_keywords.json', 'w', encoding='utf-8') as f:
            json.dump(enhanced_keywords, f, indent=2, ensure_ascii=False)
        
        print(f"SUCCESS Saved {len(enhanced_keywords)} enhanced keywords with controversy detection")
        
        # 输出热门话题摘要
        if controversies:
            print(f"\nHOT TOPICS DETECTED:")
            for controversy in controversies[:3]:
                print(f"  TOPIC {controversy['keyword']}: {len(controversy['controversy_queries'])} controversy queries")
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()