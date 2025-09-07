#!/usr/bin/env python3
"""
AI Discovery System Test with Mock Data
用于测试系统功能的模拟数据版本
"""

import json
import random
from pathlib import Path

def create_mock_keywords():
    """创建模拟关键词数据用于测试"""
    mock_keywords = [
        {
            'keyword': 'Perplexity AI',
            'category': 'content_creation',
            'trend_score': 85,
            'related_queries': ['perplexity ai vs chatgpt', 'perplexity ai pricing', 'perplexity search engine'],
            'search_volume': 85000 + random.randint(500, 2000),
            'commercial_intent': 0.85,
            'difficulty': 'Medium',
            'monthly_revenue_estimate': f"${random.randint(200, 400)}-{random.randint(500, 900)}",
            'reason': 'This keyword shows medium competition with strong search trends in the content creation category, making it ideal for our AI tools directory targeting with excellent commercial potential.',
            'is_trending_topic': False,
            'controversy_score': 0
        },
        {
            'keyword': 'Character.AI',
            'category': 'content_creation', 
            'trend_score': 78,
            'related_queries': ['character ai alternatives', 'character ai problems', 'character ai down'],
            'search_volume': 78000 + random.randint(500, 2000),
            'commercial_intent': 0.72,
            'difficulty': 'Low',
            'monthly_revenue_estimate': f"${random.randint(150, 350)}-{random.randint(400, 800)}",
            'reason': 'This keyword shows low competition with growing search trends in the content creation category, making it ideal for our AI tools directory targeting with strong commercial potential.',
            'is_trending_topic': False,
            'controversy_score': 0
        },
        {
            'keyword': 'Claude AI',
            'category': 'content_creation',
            'trend_score': 92,
            'related_queries': ['claude ai problems', 'claude ai worse', 'claude downgrade', 'claude intelligence drop'],
            'search_volume': 92000 + random.randint(500, 2000),
            'commercial_intent': 0.88,
            'difficulty': 'High',
            'monthly_revenue_estimate': f"${random.randint(300, 500)}-{random.randint(600, 1000)}",
            'reason': 'This keyword shows high competition with growing search trends in the content creation category. **TRENDING CONTROVERSY DETECTED** - Recent surge in problem-related queries (score: 40), making this highly valuable for capturing user attention and providing timely solutions.',
            'is_trending_topic': True,
            'controversy_score': 40
        },
        {
            'keyword': 'ChatGPT',
            'category': 'content_creation',
            'trend_score': 95,
            'related_queries': ['chatgpt review', 'chatgpt vs claude', 'chatgpt alternatives'],
            'search_volume': 95000 + random.randint(500, 2000),
            'commercial_intent': 0.92,
            'difficulty': 'High',
            'monthly_revenue_estimate': f"${random.randint(400, 600)}-{random.randint(700, 1200)}",
            'reason': 'This keyword shows high competition with growing search trends in the content creation category, making it ideal for our AI tools directory targeting with excellent commercial potential.',
            'is_trending_topic': False,
            'controversy_score': 0
        }
    ]
    
    # 按争议分数和趋势分数排序
    mock_keywords.sort(key=lambda x: (x['controversy_score'], x['trend_score']), reverse=True)
    
    return mock_keywords

def test_keyword_generation():
    """测试关键词生成"""
    print("Testing keyword generation with mock data...")
    
    keywords = create_mock_keywords()
    
    # 保存到文件
    with open('daily_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(keywords, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(keywords)} test keywords:")
    for i, kw in enumerate(keywords, 1):
        print(f"{i}. {kw['keyword']} - Score: {kw['trend_score']}")
        if kw['is_trending_topic']:
            print(f"   *** HOT TOPIC *** Controversy Score: {kw['controversy_score']}")
        print(f"   Revenue: {kw['monthly_revenue_estimate']}")
        print()
    
    return keywords

def test_content_generation():
    """测试内容生成"""
    print("Testing content generation...")
    
    # 模拟内容生成
    generated_files = [
        'content/articles/claude-ai-controversy-analysis-2025-09.md',
        'content/reviews/perplexity-ai-review-2025-09.md',
        'content/reviews/character-ai-review-2025-09.md'
    ]
    
    # 保存文件列表
    with open('generated_files.txt', 'w') as f:
        f.write('\n'.join(generated_files))
    
    print(f"Simulated generation of {len(generated_files)} files:")
    for file in generated_files:
        print(f"  - {file}")
    
    return generated_files

def test_notification_data():
    """测试通知数据生成"""
    print("Testing notification data preparation...")
    
    # 加载关键词数据
    with open('daily_keywords.json', 'r', encoding='utf-8') as f:
        keywords = json.load(f)
    
    # 选择最高优先级的关键词（争议话题优先）
    primary_keyword = keywords[0]  # Claude AI (有争议)
    
    notification_data = {
        'keyword_data': primary_keyword,
        'content_data': {
            'tool_name': primary_keyword['keyword'],
            'title': f"{primary_keyword['keyword']} Complete Analysis Guide 2025",
            'word_count': 2800,
            'articles_generated': 3,
            'categories_covered': ['content_creation', 'AI Tools'],
            'total_keywords_analyzed': len(keywords),
            'controversy_articles': len([kw for kw in keywords if kw['is_trending_topic']]),
            'trending_topics_detected': len([kw for kw in keywords if kw['controversy_score'] > 0])
        }
    }
    
    # 保存通知数据
    with open('notification_data.json', 'w', encoding='utf-8') as f:
        json.dump(notification_data, f, ensure_ascii=False, indent=2)
    
    print("Notification data prepared:")
    print(f"  Primary keyword: {primary_keyword['keyword']}")
    print(f"  Controversy score: {primary_keyword['controversy_score']}")
    print(f"  Commercial value: {primary_keyword['monthly_revenue_estimate']}")
    print(f"  Articles generated: {notification_data['content_data']['articles_generated']}")
    print(f"  Hot topics detected: {notification_data['content_data']['trending_topics_detected']}")
    
    return notification_data

def main():
    print("=== AI Discovery System Test ===")
    print("Testing enhanced system with hot topics detection\n")
    
    try:
        # 测试关键词生成
        keywords = test_keyword_generation()
        print()
        
        # 测试内容生成
        files = test_content_generation()
        print()
        
        # 测试通知数据
        notification = test_notification_data()
        print()
        
        print("=== Test Summary ===")
        print(f"Keywords generated: {len(keywords)}")
        print(f"Hot topics detected: {len([kw for kw in keywords if kw['is_trending_topic']])}")
        print(f"Files simulated: {len(files)}")
        print("System test completed successfully!")
        
        # 清理测试文件
        # Path('daily_keywords.json').unlink(missing_ok=True)
        # Path('generated_files.txt').unlink(missing_ok=True)
        # Path('notification_data.json').unlink(missing_ok=True)
        
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    main()