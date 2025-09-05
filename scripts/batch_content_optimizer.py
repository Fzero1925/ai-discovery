#!/usr/bin/env python3
"""
AI Discovery批量内容优化器

使用升级后的内容质量生成系统重写现有文章，确保：
- 高质量、人性化的内容
- 反AI检测技术
- SEO优化
- 真实图片集成
"""

import os
import sys
import re
import codecs
from pathlib import Path
from datetime import datetime
import frontmatter

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加模块路径
sys.path.append(str(Path(__file__).parent.parent))
from modules.content_generator.ai_tool_content_generator import AIToolContentGenerator


class BatchContentOptimizer:
    """批量内容优化器"""
    
    def __init__(self, content_dir: str = "content/reviews"):
        self.content_dir = Path(content_dir)
        self.generator = AIToolContentGenerator()
        
        # 统计数据
        self.stats = {
            'processed': 0,
            'optimized': 0,
            'skipped': 0,
            'errors': 0
        }
    
    def extract_tool_info_from_article(self, article_path: Path) -> dict:
        """从现有文章中提取工具信息"""
        try:
            with open(article_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # 从frontmatter提取信息
            title = post.metadata.get('title', '')
            categories = post.metadata.get('categories', [])
            tags = post.metadata.get('tags', [])
            
            # 尝试从标题和标签中提取工具名称
            tool_name = None
            
            # 常见的工具名称匹配
            common_tools = [
                'ChatGPT', 'Claude', 'Midjourney', 'DALL-E 3', 'Stable Diffusion',
                'GitHub Copilot', 'Codeium', 'Amazon CodeWhisperer', 'Grammarly',
                'Jasper AI', 'Copy.ai', 'Notion AI', 'Zapier', 'Tableau', 
                'DataRobot', 'TabNine', 'Adobe Firefly'
            ]
            
            # 从标签中查找工具名称
            for tag in tags:
                if tag in common_tools:
                    tool_name = tag
                    break
            
            # 从标题中提取工具名称
            if not tool_name:
                for tool in common_tools:
                    if tool.lower() in title.lower():
                        tool_name = tool
                        break
            
            # 如果还没找到，尝试从标题中提取第一个词
            if not tool_name:
                title_words = title.split()
                if title_words:
                    # 移除常见词汇后的第一个词可能是工具名
                    common_words = ['complete', 'comprehensive', 'review', 'guide', 'vs', 'competitors']
                    for word in title_words:
                        clean_word = re.sub(r'[^a-zA-Z0-9]', '', word)
                        if clean_word and clean_word.lower() not in common_words and len(clean_word) > 2:
                            tool_name = clean_word.title()
                            break
            
            category = categories[0] if categories else 'content_creation'
            
            return {
                'tool_name': tool_name or 'AI Tool',
                'category': category,
                'original_title': title,
                'tags': tags,
                'file_path': article_path
            }
            
        except Exception as e:
            print(f"❌ Error extracting info from {article_path}: {e}")
            return None
    
    def optimize_article(self, tool_info: dict) -> bool:
        """优化单篇文章"""
        try:
            tool_name = tool_info['tool_name']
            category = tool_info['category'] 
            file_path = tool_info['file_path']
            
            print(f"🔄 优化文章: {tool_name} ({category})")
            
            # 生成关键词
            target_keywords = [
                f"{tool_name} review",
                f"AI {category.replace('_', ' ')} tools",
                f"best {tool_name} alternative",
                "artificial intelligence software",
                f"{tool_name} vs competitors"
            ]
            
            # 使用升级后的内容生成器创建新内容
            optimized_content = self.generator.generate_ai_tool_review(tool_name, target_keywords)
            
            # 读取原文件的frontmatter以保持某些元数据
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # 保持原有的日期和某些元数据
            original_date = post.metadata.get('date')
            
            # 解析新内容的frontmatter
            new_post = frontmatter.loads(optimized_content)
            
            # 合并元数据：保留某些原有数据，使用新的优化数据
            new_post.metadata['date'] = original_date or new_post.metadata.get('date')
            
            # 写入优化后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(new_post))
            
            print(f"  ✅ 已优化: {file_path.name}")
            return True
            
        except Exception as e:
            print(f"  ❌ 优化失败: {tool_info.get('tool_name', 'Unknown')}, Error: {e}")
            return False
    
    def optimize_all_articles(self):
        """批量优化所有文章"""
        print("🚀 开始批量优化AI Discovery文章...")
        print(f"📂 扫描目录: {self.content_dir}")
        
        if not self.content_dir.exists():
            print(f"❌ 内容目录不存在: {self.content_dir}")
            return
        
        # 获取所有markdown文件
        md_files = [f for f in self.content_dir.glob('*.md') if f.name != '_index.md']
        total_files = len(md_files)
        
        print(f"📊 发现 {total_files} 篇文章需要优化")
        
        for i, md_file in enumerate(md_files, 1):
            print(f"\n[{i}/{total_files}] 处理文章: {md_file.name}")
            
            # 提取工具信息
            tool_info = self.extract_tool_info_from_article(md_file)
            
            if not tool_info:
                print(f"  ⚠️ 跳过: 无法提取工具信息")
                self.stats['skipped'] += 1
                continue
            
            # 优化文章
            success = self.optimize_article(tool_info)
            
            if success:
                self.stats['optimized'] += 1
            else:
                self.stats['errors'] += 1
            
            self.stats['processed'] += 1
            
            # 每处理5篇文章显示进度
            if i % 5 == 0:
                print(f"\n📈 进度报告: 已处理 {i}/{total_files} 篇文章")
                print(f"   ✅ 成功优化: {self.stats['optimized']}")
                print(f"   ❌ 出现错误: {self.stats['errors']}")
                print(f"   ⚠️ 跳过文章: {self.stats['skipped']}")
        
        # 最终统计
        print(f"\n🎉 批量优化完成!")
        print("=" * 50)
        print(f"📊 最终统计:")
        print(f"   📝 总处理数: {self.stats['processed']}")
        print(f"   ✅ 优化成功: {self.stats['optimized']}")
        print(f"   ❌ 优化失败: {self.stats['errors']}")
        print(f"   ⚠️ 跳过文章: {self.stats['skipped']}")
        print(f"   📈 成功率: {self.stats['optimized']/max(1,self.stats['processed'])*100:.1f}%")


def main():
    """主函数"""
    print("🤖 AI Discovery 批量内容优化器")
    print("=" * 50)
    
    optimizer = BatchContentOptimizer()
    optimizer.optimize_all_articles()


if __name__ == "__main__":
    main()