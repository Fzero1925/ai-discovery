#!/usr/bin/env python3
"""
真实图片获取系统
使用Unsplash API为AI工具获取相关的真实图片
"""

import os
import sys
import requests
import json
import time
import hashlib
import codecs
from pathlib import Path
from PIL import Image
from urllib.parse import urlparse
from typing import Dict, List, Optional

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

class RealImageFetcher:
    """真实图片获取器"""
    
    def __init__(self):
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.images_dir = Path("static/images/tools")
        self.cache_dir = Path("static/images/cache")
        
        # 创建目录
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API配置
        self.api_base = "https://api.unsplash.com"
        self.headers = {
            'Authorization': f'Client-ID {self.access_key}',
            'Accept-Version': 'v1'
        }
        
        # 图片尺寸配置
        self.image_sizes = {
            'featured': (1200, 630),    # OG image size
            'thumbnail': (400, 300),    # Card thumbnail
            'icon': (150, 150)          # Small icon
        }
        
        # AI工具搜索查询优化 - 更具体的AI相关关键词
        self.search_queries = {
            'ChatGPT': 'artificial intelligence chatbot interface dashboard ai conversation',
            'Claude': 'ai assistant interface anthropic artificial intelligence dashboard',
            'Jasper AI': 'ai writing assistant dashboard content creation interface',
            'Copy.ai': 'ai copywriting interface dashboard marketing content creation',
            'Midjourney': 'ai art generation interface digital art creation dashboard',
            'DALL-E 3': 'ai image generation interface openai artificial intelligence art',
            'Stable Diffusion': 'ai art generation interface machine learning dashboard',
            'Adobe Firefly': 'ai creative interface adobe generative design dashboard',
            'GitHub Copilot': 'ai coding assistant interface programming dashboard development',
            'Codeium': 'ai code completion interface programming assistant dashboard',
            'Amazon CodeWhisperer': 'aws ai programming interface development assistant dashboard',
            'TabNine': 'ai code completion interface programming development assistant',
            'Grammarly': 'ai writing assistant interface proofreading dashboard editor',
            'Notion AI': 'ai productivity interface workspace collaboration dashboard',
            'Zapier': 'automation workflow interface productivity dashboard integration',
            'Tableau': 'data visualization interface analytics dashboard business intelligence',
            'DataRobot': 'machine learning interface ai analytics platform dashboard',
            'Power BI': 'business intelligence interface analytics dashboard microsoft data',
            # 通用AI工具相关搜索词
            'default': 'artificial intelligence interface dashboard ai technology software',
            'content_creation': 'ai writing assistant interface content creation dashboard',
            'image_generation': 'ai image generation interface art creation dashboard',
            'code_assistance': 'ai programming assistant interface coding development dashboard',
            'productivity': 'ai productivity interface automation dashboard workflow'
        }
        
        # 请求间隔（避免API限制）
        self.request_delay = 2  # 2秒间隔
        
        # 统计
        self.stats = {
            'processed': 0,
            'downloaded': 0,
            'cached': 0,
            'errors': 0
        }
    
    def check_api_key(self) -> bool:
        """检查API密钥是否有效"""
        if not self.access_key:
            print("❌ 错误：未找到UNSPLASH_ACCESS_KEY环境变量")
            print("请先运行: python scripts/test_unsplash_api.py")
            return False
        return True
    
    def get_tool_query(self, tool_name: str) -> str:
        """获取工具的搜索查询，支持智能类型推断"""
        # 直接匹配
        if tool_name in self.search_queries:
            return self.search_queries[tool_name]
        
        # 模糊匹配
        for key in self.search_queries.keys():
            if key.lower() in tool_name.lower() or tool_name.lower() in key.lower():
                return self.search_queries[key]
        
        # 基于工具名称推断类型
        tool_lower = tool_name.lower()
        if any(keyword in tool_lower for keyword in ['gpt', 'chat', 'claude', 'gemini', 'bard']):
            return self.search_queries['default']
        elif any(keyword in tool_lower for keyword in ['write', 'copy', 'jasper', 'content', 'grammar']):
            return self.search_queries['content_creation'] 
        elif any(keyword in tool_lower for keyword in ['midjourney', 'dalle', 'stable', 'image', 'art', 'firefly']):
            return self.search_queries['image_generation']
        elif any(keyword in tool_lower for keyword in ['copilot', 'code', 'program', 'github', 'codeium', 'tabnine']):
            return self.search_queries['code_assistance']
        elif any(keyword in tool_lower for keyword in ['zapier', 'notion', 'productivity', 'automat']):
            return self.search_queries['productivity']
        
        # 默认查询
        return f"{tool_name} artificial intelligence tool dashboard interface"
    
    def search_images(self, query: str, count: int = 5) -> List[Dict]:
        """搜索相关图片"""
        try:
            url = f"{self.api_base}/search/photos"
            params = {
                'query': query,
                'per_page': count,
                'orientation': 'landscape',
                'order_by': 'relevant'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            elif response.status_code == 403:
                print(f"⚠️ API限制：请等待后重试")
                return []
            else:
                print(f"⚠️ 搜索失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ 搜索错误: {e}")
            return []
    
    def download_image(self, image_url: str, tool_name: str, size_type: str) -> Optional[Path]:
        """下载并处理图片"""
        try:
            # 生成缓存文件名
            url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
            safe_name = tool_name.lower().replace(' ', '-').replace('.', '')
            cache_filename = f"{safe_name}-{size_type}-{url_hash}.jpg"
            cache_path = self.cache_dir / cache_filename
            
            # 检查缓存
            if cache_path.exists():
                print(f"  📦 使用缓存: {cache_filename}")
                self.stats['cached'] += 1
                return cache_path
            
            # 下载图片
            print(f"  📥 下载图片: {image_url}")
            response = requests.get(image_url, timeout=30, stream=True)
            
            if response.status_code == 200:
                # 保存原始图片到缓存
                with open(cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # 使用PIL处理图片
                with Image.open(cache_path) as img:
                    # 转换为RGB (移除透明通道)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        bg = Image.new('RGB', img.size, 'white')
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = bg
                    
                    # 调整尺寸
                    target_size = self.image_sizes[size_type]
                    img = img.resize(target_size, Image.LANCZOS)
                    
                    # 保存处理后的图片
                    final_filename = f"{safe_name}-{size_type}.jpg"
                    final_path = self.images_dir / final_filename
                    img.save(final_path, 'JPEG', quality=90, optimize=True)
                    
                    print(f"  ✅ 保存成功: {final_filename}")
                    self.stats['downloaded'] += 1
                    return final_path
            
            else:
                print(f"  ❌ 下载失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
            return None
    
    def process_tool_images(self, tool_name: str) -> bool:
        """处理单个工具的图片"""
        try:
            print(f"\\n🔍 处理工具: {tool_name}")
            
            # 获取搜索查询（使用智能推断）
            query = self.get_tool_query(tool_name)
            print(f"  🔎 搜索查询: {query}")
            
            # 搜索图片
            images = self.search_images(query, count=3)
            
            if not images:
                print(f"  ⚠️ 未找到相关图片")
                return False
            
            print(f"  📸 找到 {len(images)} 张候选图片")
            
            # 处理不同尺寸的图片
            success_count = 0
            
            for size_type in self.image_sizes.keys():
                # 选择最佳图片
                best_image = None
                for img in images:
                    # 优先选择高分辨率、横向的图片
                    if img['width'] >= self.image_sizes[size_type][0] and img['height'] >= self.image_sizes[size_type][1]:
                        best_image = img
                        break
                
                if not best_image and images:
                    best_image = images[0]  # 使用第一张作为备选
                
                if best_image:
                    image_url = best_image['urls']['regular']
                    result_path = self.download_image(image_url, tool_name, size_type)
                    
                    if result_path:
                        success_count += 1
                        
                        # 创建placeholder版本（保持向后兼容）
                        if size_type == 'featured':
                            safe_name = tool_name.lower().replace(' ', '-').replace('.', '')
                            placeholder_path = self.images_dir / f"{safe_name}-placeholder.jpg"
                            if result_path != placeholder_path:
                                # 复制为placeholder文件
                                with open(result_path, 'rb') as src, open(placeholder_path, 'wb') as dst:
                                    dst.write(src.read())
                    
                    # 添加延迟避免API限制
                    time.sleep(self.request_delay)
            
            if success_count > 0:
                print(f"  🎉 成功获取 {success_count}/{len(self.image_sizes)} 个尺寸的图片")
                return True
            else:
                print(f"  ❌ 所有图片处理失败")
                return False
                
        except Exception as e:
            print(f"  ❌ 处理工具失败: {e}")
            return False
    
    def process_all_tools(self):
        """批量处理所有工具的图片"""
        print("🎨 开始获取真实AI工具图片...")
        print("=" * 50)
        
        if not self.check_api_key():
            return
        
        tools = list(self.search_queries.keys())
        total_tools = len(tools)
        
        print(f"📊 将处理 {total_tools} 个AI工具")
        
        for i, tool_name in enumerate(tools, 1):
            print(f"\\n[{i}/{total_tools}] 处理: {tool_name}")
            
            success = self.process_tool_images(tool_name)
            
            if success:
                self.stats['processed'] += 1
            else:
                self.stats['errors'] += 1
            
            # 每5个工具显示一次进度
            if i % 5 == 0:
                print(f"\\n📈 进度报告: 已处理 {i}/{total_tools} 个工具")
                print(f"   ✅ 成功: {self.stats['processed']}")
                print(f"   📥 下载: {self.stats['downloaded']}")
                print(f"   📦 缓存: {self.stats['cached']}")
                print(f"   ❌ 错误: {self.stats['errors']}")
        
        # 最终统计
        print(f"\\n🎉 图片获取完成!")
        print("=" * 50)
        print(f"📊 最终统计:")
        print(f"   🎯 处理工具: {self.stats['processed']}/{total_tools}")
        print(f"   📸 下载图片: {self.stats['downloaded']}")
        print(f"   📦 使用缓存: {self.stats['cached']}")
        print(f"   ❌ 处理错误: {self.stats['errors']}")
        print(f"   📈 成功率: {self.stats['processed']/max(1,total_tools)*100:.1f}%")

def main():
    """主函数"""
    print("🌟 AI Discovery 真实图片获取系统")
    print("=" * 50)
    
    fetcher = RealImageFetcher()
    fetcher.process_all_tools()

if __name__ == "__main__":
    main()