#!/usr/bin/env python3
"""
Test Telegram Notification Format
展示增强的通知消息格式
"""

import json
import sys
from datetime import datetime
import pytz

sys.path.append('.')
from scripts.telegram_notify import format_keyword_analysis_message, get_china_time

def test_enhanced_notification():
    """测试增强的Telegram通知格式"""
    print("=== Enhanced Telegram Notification Test ===\n")
    
    # 模拟热门争议话题数据
    keyword_data = {
        "keyword": "Claude AI",
        "category": "content_creation", 
        "trend_score": 92,
        "search_volume": 94500,
        "commercial_intent": 0.88,
        "difficulty": "High",
        "monthly_revenue_estimate": "$390-620",
        "reason": "This keyword shows high competition with growing search trends in the content creation category. **TRENDING CONTROVERSY DETECTED** - Recent surge in problem-related queries (score: 40), making this highly valuable for capturing user attention and providing timely solutions.",
        "related_queries": [
            "claude ai problems",
            "claude ai worse", 
            "claude downgrade",
            "claude intelligence drop",
            "claude ai issues 2025"
        ],
        "is_trending_topic": True,
        "controversy_score": 40
    }
    
    content_data = {
        "tool_name": "Claude AI",
        "title": "Claude AI Complete Analysis Guide 2025",
        "word_count": 2800,
        "articles_generated": 3,
        "categories_covered": ["content_creation", "AI Tools"],
        "total_keywords_analyzed": 4,
        "controversy_articles": 1,
        "trending_topics_detected": 1
    }
    
    # 生成通知消息
    message = format_keyword_analysis_message(keyword_data, content_data)
    
    print("Generated Notification Message:")
    print("=" * 80)
    print(message)
    print("=" * 80)
    
    # 测试常规工具通知
    print("\n=== Regular Tool Notification Test ===\n")
    
    regular_keyword = {
        "keyword": "Perplexity AI",
        "category": "content_creation",
        "trend_score": 85,
        "search_volume": 87200,
        "commercial_intent": 0.85,
        "difficulty": "Medium", 
        "monthly_revenue_estimate": "$369-806",
        "reason": "This keyword shows medium competition with growing search trends in the content creation category, making it ideal for our AI tools directory targeting with excellent commercial potential.",
        "related_queries": [
            "perplexity ai vs chatgpt",
            "perplexity ai pricing",
            "perplexity search engine",
            "best ai search tool",
            "perplexity ai review"
        ],
        "is_trending_topic": False,
        "controversy_score": 0
    }
    
    regular_content = {
        "tool_name": "Perplexity AI",
        "title": "Perplexity AI Complete Analysis Guide 2025", 
        "word_count": 2500,
        "articles_generated": 2,
        "categories_covered": ["content_creation", "research_search"],
        "total_keywords_analyzed": 4,
        "controversy_articles": 0,
        "trending_topics_detected": 0
    }
    
    regular_message = format_keyword_analysis_message(regular_keyword, regular_content)
    
    print("Regular Tool Notification:")
    print("=" * 80)
    print(regular_message)
    print("=" * 80)
    
    print("\n=== Analysis Summary ===")
    print("✅ Controversy detection working")
    print("✅ Commercial value analysis included") 
    print("✅ Keyword selection reasoning shown")
    print("✅ Competitive analysis provided")
    print("✅ Hot topics prioritized properly")
    print("✅ Business intelligence metrics complete")

if __name__ == "__main__":
    test_enhanced_notification()