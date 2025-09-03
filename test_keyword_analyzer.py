#!/usr/bin/env python3
"""
测试AI工具关键词分析器功能
Test script for AI Tool Keyword Analyzer
"""

import sys
import os
sys.path.append('modules')

from keyword_tools.ai_tool_keyword_analyzer import AIToolKeywordAnalyzer
import json

def test_keyword_analyzer():
    """测试关键词分析器基本功能"""
    print("=" * 50)
    print("AI Discovery - 关键词分析器测试")
    print("=" * 50)
    
    # 初始化分析器
    try:
        analyzer = AIToolKeywordAnalyzer()
        print("[SUCCESS] 关键词分析器初始化成功")
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        return False
    
    # 测试AI工具分类
    print("\n[TEST] 测试AI工具分类:")
    for category, tools in analyzer.ai_tool_categories.items():
        print(f"  {category}: {len(tools)}个工具")
        print(f"    - {', '.join(tools[:3])}...")
    
    # 测试缓存功能
    print("\n[TEST] 测试缓存系统:")
    try:
        cached_keywords = analyzer.load_analysis_cache()
        if cached_keywords:
            print(f"[SUCCESS] 找到缓存数据: {len(cached_keywords)}个关键词")
        else:
            print("[INFO] 无缓存数据，这是正常的")
    except Exception as e:
        print(f"[ERROR] 缓存测试失败: {e}")
    
    # 测试关键词生成功能
    print("\n[TEST] 测试内容关键词生成:")
    try:
        content_keywords = analyzer.generate_content_keywords("ChatGPT", "content_creation")
        if content_keywords:
            print(f"[SUCCESS] 生成了{len(content_keywords)}个内容关键词")
            print("示例关键词:")
            for i, keyword in enumerate(content_keywords[:5]):
                print(f"  {i+1}. {keyword}")
        else:
            print("[WARN] 未生成关键词")
    except Exception as e:
        print(f"[ERROR] 关键词生成测试失败: {e}")
    
    # 测试实际的Google Trends API (小范围测试)
    print("\n[TEST] 测试Google Trends API连接:")
    print("注意：这会进行实际的网络请求，可能需要一些时间...")
    try:
        # 使用内置的测试方法进行简单验证
        test_keyword = "AI"
        related_queries = analyzer._get_related_queries(test_keyword)
        
        if related_queries:
            print(f"[SUCCESS] Google Trends API连接正常")
            print(f"获取到{len(related_queries)}个相关查询")
            print(f"示例相关查询: {related_queries[:3]}")
        else:
            print("[WARN] 未获取到相关查询，可能是网络限制")
            
        print("[INFO] 跳过完整趋势分析以节省API请求")
        
    except Exception as e:
        print(f"[ERROR] Google Trends API测试失败: {e}")
        print("这可能是由于网络连接、请求限制或地区限制导致的")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] 关键词分析器测试完成")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_keyword_analyzer()