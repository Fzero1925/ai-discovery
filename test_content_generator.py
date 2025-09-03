#!/usr/bin/env python3
"""
测试AI工具内容生成器功能
Test script for AI Tool Content Generator
"""

import sys
import os
sys.path.append('modules')

from content_generator.ai_tool_content_generator import AIToolContentGenerator
import json

def test_content_generator():
    """测试内容生成器基本功能"""
    print("=" * 50)
    print("AI Discovery - 内容生成器测试")
    print("=" * 50)
    
    # 初始化生成器
    try:
        generator = AIToolContentGenerator()
        print("[SUCCESS] 内容生成器初始化成功")
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        return False
    
    # 测试AI工具数据库
    print("\n[TEST] 测试AI工具数据库:")
    categories = {}
    for tool_name, tool_data in generator.ai_tool_database.items():
        category = tool_data.category
        if category not in categories:
            categories[category] = []
        categories[category].append(tool_name)
    
    for category, tools in categories.items():
        print(f"  {category}: {len(tools)}个工具")
        print(f"    示例工具: {', '.join(tools)}")
    
    # 测试内容变化模式
    print("\n[TEST] 测试内容变化模式:")
    try:
        variations = generator.variations
        print(f"[SUCCESS] 内容变化模式加载成功")
        print(f"  句子开头: {len(variations.sentence_starters)}个")
        print(f"  过渡短语: {len(variations.transition_phrases)}个") 
        print(f"  结论模式: {len(variations.conclusion_patterns)}个")
        print(f"  专业标记: {len(variations.expertise_markers)}个")
        print(f"  个人语调: {len(variations.personal_touches)}个")
    except Exception as e:
        print(f"[ERROR] 内容变化模式测试失败: {e}")
    
    # 测试内容生成 (使用数据库中现有工具)
    print("\n[TEST] 测试内容生成:")
    try:
        test_tool_name = "ChatGPT"  # 使用数据库中存在的工具
        print(f"生成{test_tool_name}评测文章...")
        
        content = generator.generate_ai_tool_review(
            tool_name=test_tool_name,
            target_keywords=["ChatGPT review", "AI assistant comparison", "best AI tools 2025"]
        )
        
        if content:
            print("[SUCCESS] 内容生成成功")
            print(f"文章长度: {len(content)}字符")
            print(f"文章预览:")
            print("-" * 30)
            print(content[:500] + "..." if len(content) > 500 else content)
            print("-" * 30)
        else:
            print("[ERROR] 内容生成失败")
            
    except Exception as e:
        print(f"[ERROR] 内容生成测试失败: {e}")
    
    # 测试反AI检测功能
    print("\n[TEST] 测试反AI检测功能:")
    try:
        test_text = "This AI tool is extremely powerful and versatile. It provides excellent results consistently."
        humanized_text = generator._apply_human_variations({"test": test_text})
        
        print("[SUCCESS] 反AI检测处理完成")
        print("原文:", test_text)
        print("处理后:", humanized_text.get("test", "未处理"))
        
    except Exception as e:
        print(f"[ERROR] 反AI检测测试失败: {e}")
    
    # 测试SEO优化功能
    print("\n[TEST] 测试SEO模式:")
    try:
        seo_patterns = generator.seo_patterns
        print(f"[SUCCESS] SEO模式加载成功: {len(seo_patterns)}个模式")
        for i, pattern in enumerate(seo_patterns[:3]):
            print(f"  {i+1}. {pattern}")
        print("  ...")
    except Exception as e:
        print(f"[ERROR] SEO模式测试失败: {e}")
        
    # 测试工具类别分析
    print("\n[TEST] 测试工具数据完整性:")
    try:
        test_tool = generator.ai_tool_database.get("ChatGPT")
        if test_tool:
            print("[SUCCESS] 工具数据结构验证通过")
            print(f"  工具名: {test_tool.tool_name}")
            print(f"  类别: {test_tool.category}")
            print(f"  评分: {test_tool.rating}")
            print(f"  定价: {test_tool.pricing}")
            print(f"  主要功能: {len(test_tool.key_features)}个")
            print(f"  优点: {len(test_tool.pros)}个")
            print(f"  缺点: {len(test_tool.cons)}个")
            print(f"  使用场景: {len(test_tool.use_cases)}个")
        else:
            print("[ERROR] 测试工具数据不存在")
    except Exception as e:
        print(f"[ERROR] 工具数据测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] 内容生成器测试完成")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_content_generator()