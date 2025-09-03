#!/usr/bin/env python3
"""
批量生成AI工具评测示例内容
Generate sample AI tool review content in batch
"""

import sys
import os
from datetime import datetime
sys.path.append('modules')

from content_generator.ai_tool_content_generator import AIToolContentGenerator

def generate_sample_articles():
    """生成示例AI工具评测文章"""
    print("=" * 60)
    print("AI Discovery - 批量内容生成")
    print("=" * 60)
    
    # 初始化内容生成器
    try:
        generator = AIToolContentGenerator()
        print("[SUCCESS] 内容生成器初始化成功")
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        return False
    
    # 获取所有可用工具
    all_tools = list(generator.ai_tool_database.keys())
    print(f"[INFO] 发现 {len(all_tools)} 个AI工具")
    
    # 选择要生成的工具（每个类别选择1-2个）
    selected_tools = [
        "Claude",           # Content Creation
        "DALL-E 3",         # Image Generation
        "Amazon CodeWhisperer",  # Code Assistance
        "Grammarly",        # Productivity  
        "Power BI",         # Data Analysis
        "Stable Diffusion", # Additional popular tool
        "Codeium"          # Additional popular tool
    ]
    
    print(f"[INFO] 计划生成 {len(selected_tools)} 篇文章")
    
    # 确保输出目录存在
    os.makedirs('content/reviews', exist_ok=True)
    
    generated_files = []
    failed_tools = []
    
    for i, tool_name in enumerate(selected_tools, 1):
        try:
            print(f"\n[{i}/{len(selected_tools)}] 正在生成: {tool_name}")
            
            # 为每个工具定制关键词
            target_keywords = [
                f"{tool_name} review",
                f"{tool_name} guide",
                f"best {tool_name} alternatives",
                "AI tools 2025",
                f"how to use {tool_name}"
            ]
            
            # 生成内容
            content = generator.generate_ai_tool_review(tool_name, target_keywords)
            
            if content:
                # 创建文件名（安全化处理）
                safe_name = tool_name.lower().replace(' ', '-').replace('/', '-').replace(':', '')
                filename = f"content/reviews/{safe_name}-comprehensive-review.md"
                
                # 保存文件
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                generated_files.append(filename)
                print(f"  [SUCCESS] 已保存: {filename}")
                print(f"  [INFO] 文章长度: {len(content)} 字符")
                
            else:
                print(f"  [ERROR] 内容生成失败: {tool_name}")
                failed_tools.append(tool_name)
                
        except Exception as e:
            print(f"  [ERROR] 生成 {tool_name} 时发生错误: {e}")
            failed_tools.append(tool_name)
    
    # 生成统计报告
    print("\n" + "=" * 60)
    print("生成完成统计")
    print("=" * 60)
    print(f"成功生成: {len(generated_files)} 篇文章")
    print(f"失败工具: {len(failed_tools)} 个")
    
    if generated_files:
        print("\n成功生成的文件:")
        for i, filename in enumerate(generated_files, 1):
            print(f"  {i}. {filename}")
    
    if failed_tools:
        print("\n失败的工具:")
        for i, tool in enumerate(failed_tools, 1):
            print(f"  {i}. {tool}")
    
    # 创建文件列表供Git使用
    if generated_files:
        with open('generated_files_list.txt', 'w') as f:
            for filename in generated_files:
                f.write(filename + '\n')
        print(f"\n[INFO] 文件列表已保存至 generated_files_list.txt")
    
    print(f"\n[SUCCESS] 批量内容生成完成!")
    return len(generated_files) > 0

if __name__ == "__main__":
    generate_sample_articles()