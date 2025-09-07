#!/usr/bin/env python3
"""
AI Discovery - Enhanced Content Generation with Hot Topics Support
支持热门话题快速响应内容生成
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Add modules to path
sys.path.append('modules')

try:
    from content_generator.ai_tool_content_generator import AIToolContentGenerator
except ImportError as e:
    print(f"Error importing content generator: {e}")
    sys.exit(1)

def generate_trending_topic_content(generator, keyword_data, is_controversy=False):
    """
    为热门话题生成专门的内容
    """
    tool_name = keyword_data['keyword']
    category = keyword_data.get('category', 'AI Tools')
    
    # 如果是争议话题，使用特殊的关键词组合
    if is_controversy:
        target_keywords = [
            f"{tool_name} issues 2025",
            f"{tool_name} problems analysis", 
            f"what happened to {tool_name}",
            f"{tool_name} performance decline",
            f"{tool_name} alternatives comparison",
            f"is {tool_name} getting worse"
        ]
    else:
        target_keywords = [
            f"{tool_name} review",
            f"best {tool_name} guide", 
            f"{tool_name} complete analysis",
            f"how to use {tool_name}",
            f"{tool_name} vs alternatives"
        ]
    
    print(f"🎯 Generating content for: {tool_name} {'(CONTROVERSY)' if is_controversy else '(STANDARD)'}")
    return generator.generate_ai_tool_review(tool_name, target_keywords)

def main():
    print("📝 Generating AI tool content with hot topics support...")
    
    try:
        # 加载关键词数据
        if os.path.exists('daily_keywords.json'):
            with open('daily_keywords.json', 'r', encoding='utf-8') as f:
                keywords = json.load(f)
        else:
            print("⚠️  No keywords file found, using default generation")
            keywords = []
        
        generator = AIToolContentGenerator()
        generated_files = []
        
        # 优先处理热门争议话题
        controversy_keywords = [kw for kw in keywords if kw.get('is_trending_topic', False)]
        regular_keywords = [kw for kw in keywords if not kw.get('is_trending_topic', False)]
        
        print(f"📊 Found {len(controversy_keywords)} trending controversies, {len(regular_keywords)} regular topics")
        
        # 处理争议话题（优先级高）
        for keyword_data in controversy_keywords[:2]:  # 最多处理2个争议话题
            tool_name = keyword_data['keyword']
            try:
                content = generate_trending_topic_content(generator, keyword_data, is_controversy=True)
                
                # 创建文件名（争议话题标记）
                filename = f"content/articles/{tool_name.lower().replace(' ', '-')}-controversy-analysis-{datetime.now().strftime('%Y-%m')}.md"
                
                # 确保目录存在
                os.makedirs('content/articles', exist_ok=True)
                
                # 检查文件是否已存在
                if not os.path.exists(filename):
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    generated_files.append(filename)
                    print(f"✅ Generated controversy analysis: {filename}")
                else:
                    print(f"⚠️  File already exists: {filename}")
                    
            except Exception as e:
                print(f"❌ Error generating controversy content for {tool_name}: {e}")
        
        # 处理常规工具评测
        for tool_name in list(generator.ai_tool_database.keys())[:3]:  # 限制生成数量
            keyword_data = next((kw for kw in regular_keywords if tool_name.lower() in kw['keyword'].lower()), None)
            
            try:
                if keyword_data:
                    content = generate_trending_topic_content(generator, keyword_data, is_controversy=False)
                else:
                    # 使用默认关键词
                    target_keywords = [f"{tool_name} review", "AI tools 2025", f"best {tool_name} alternative"]
                    content = generator.generate_ai_tool_review(tool_name, target_keywords)
                
                # 创建文件名
                filename = f"content/reviews/{tool_name.lower().replace(' ', '-')}-review-{datetime.now().strftime('%Y-%m')}.md"
                
                # 确保目录存在
                os.makedirs('content/reviews', exist_ok=True)
                
                # 检查文件是否已存在
                if not os.path.exists(filename):
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    generated_files.append(filename)
                    print(f"✅ Generated review: {filename}")
                else:
                    print(f"⚠️  File already exists: {filename}")
                    
            except Exception as e:
                print(f"❌ Error generating content for {tool_name}: {e}")
        
        print(f"📈 Generated {len(generated_files)} new articles")
        
        # 保存生成的文件列表
        with open('generated_files.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(generated_files))
        
        # 为通知准备数据
        if keywords and len(generated_files) > 0:
            # 选择最高优先级的关键词（争议话题优先）
            primary_keyword = controversy_keywords[0] if controversy_keywords else keywords[0]
            
            notification_data = {
                'keyword_data': primary_keyword,
                'content_data': {
                    'tool_name': primary_keyword['keyword'],
                    'title': f"{primary_keyword['keyword']} Complete Analysis Guide 2025",
                    'word_count': 2800,
                    'articles_generated': len(generated_files),
                    'categories_covered': list(set([kw.get('category', 'AI Tools') for kw in keywords[:3]])),
                    'total_keywords_analyzed': len(keywords),
                    'controversy_articles': len(controversy_keywords),
                    'trending_topics_detected': len([kw for kw in keywords if kw.get('controversy_score', 0) > 0])
                }
            }
            
            with open('notification_data.json', 'w', encoding='utf-8') as f:
                json.dump(notification_data, f, ensure_ascii=False, indent=2)
            
            print(f"📊 Notification data prepared - Primary keyword: {primary_keyword['keyword']}")
            if controversy_keywords:
                print(f"🔥 Hot topic detected: {primary_keyword['keyword']} (Controversy score: {primary_keyword.get('controversy_score', 0)})")
    
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()