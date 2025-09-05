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
        
        # AI工具搜索查询优化
        self.search_queries = {
            'ChatGPT': 'chatgpt ai assistant artificial intelligence',
            'Claude': 'claude ai anthropic artificial intelligence assistant',
            'Jasper AI': 'jasper ai writing content creation copywriting',
            'Copy.ai': 'copywriting ai content creation marketing tools',
            'Midjourney': 'midjourney ai art generation digital art',
            'DALL-E 3': 'dalle ai image generation artificial intelligence art',
            'Stable Diffusion': 'stable diffusion ai art generation machine learning',
            'Adobe Firefly': 'adobe firefly ai creative generative design',
            'GitHub Copilot': 'github copilot ai programming coding assistant',
            'Codeium': 'codeium ai coding assistant programming development',
            'Amazon CodeWhisperer': 'aws codewhisperer ai programming development',
            'TabNine': 'tabnine ai code completion programming assistant',
            'Grammarly': 'grammarly writing assistant ai proofreading',
            'Notion AI': 'notion ai productivity workspace collaboration',
            'Zapier': 'zapier automation workflow integration productivity',
            'Tableau': 'tableau data visualization analytics business intelligence',
            'DataRobot': 'datarobot machine learning ai analytics platform',
            'Power BI': 'power bi microsoft business intelligence analytics'
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
            
            # 获取搜索查询
            query = self.search_queries.get(tool_name, f"{tool_name} artificial intelligence")
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