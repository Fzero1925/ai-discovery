#!/usr/bin/env python3
"""
简化版真实图片获取系统 - 避免编码问题
"""

import os
import requests
import time
import hashlib
from pathlib import Path
from PIL import Image

class RealImageFetcher:
    def __init__(self):
        self.access_key = "fU_RSdecKs7yCLkwfietuN_An8Y4pDAARPjbGuWlyKQ"
        self.images_dir = Path("static/images/tools")
        self.cache_dir = Path("static/images/cache")
        
        # Create directories
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API config
        self.headers = {
            'Authorization': f'Client-ID {self.access_key}',
            'Accept-Version': 'v1'
        }
        
        # Image sizes
        self.image_sizes = {
            'featured': (1200, 630),
            'thumbnail': (400, 300),
            'icon': (150, 150)
        }
        
        # AI tools search queries
        self.tools = {
            'ChatGPT': 'chatgpt ai assistant artificial intelligence openai',
            'Claude': 'claude ai anthropic artificial intelligence assistant',
            'Jasper AI': 'jasper ai writing content creation copywriting',
            'Copy.ai': 'copywriting ai content creation marketing tools',
            'Midjourney': 'midjourney ai art generation digital art creative',
            'DALL-E 3': 'dalle ai image generation artificial intelligence art',
            'Stable Diffusion': 'stable diffusion ai art generation machine learning',
            'Adobe Firefly': 'adobe firefly ai creative generative design',
            'GitHub Copilot': 'github copilot ai programming coding assistant',
            'Codeium': 'codeium ai coding assistant programming development',
            'Amazon CodeWhisperer': 'aws codewhisperer ai programming development',
            'TabNine': 'tabnine ai code completion programming assistant',
            'Grammarly': 'grammarly writing assistant ai proofreading editing',
            'Notion AI': 'notion ai productivity workspace collaboration',
            'Zapier': 'zapier automation workflow integration productivity',
            'Tableau': 'tableau data visualization analytics business intelligence',
            'DataRobot': 'datarobot machine learning ai analytics platform',
            'Power BI': 'power bi microsoft business intelligence analytics dashboard'
        }
        
        self.request_delay = 2
        self.stats = {'processed': 0, 'downloaded': 0, 'errors': 0}
    
    def search_images(self, query, count=3):
        try:
            url = "https://api.unsplash.com/search/photos"
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
            else:
                print(f"Search failed: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def download_image(self, image_url, tool_name, size_type):
        try:
            safe_name = tool_name.lower().replace(' ', '-').replace('.', '')
            
            # Download image
            response = requests.get(image_url, timeout=30, stream=True)
            
            if response.status_code == 200:
                # Save original to cache
                url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
                cache_filename = f"{safe_name}-{size_type}-{url_hash}.jpg"
                cache_path = self.cache_dir / cache_filename
                
                with open(cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Process with PIL
                with Image.open(cache_path) as img:
                    # Convert to RGB
                    if img.mode in ('RGBA', 'LA', 'P'):
                        bg = Image.new('RGB', img.size, 'white')
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        bg.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = bg
                    
                    # Resize
                    target_size = self.image_sizes[size_type]
                    img = img.resize(target_size, Image.LANCZOS)
                    
                    # Save processed image
                    final_filename = f"{safe_name}-{size_type}.jpg"
                    final_path = self.images_dir / final_filename
                    img.save(final_path, 'JPEG', quality=90, optimize=True)
                    
                    # Create placeholder version for featured
                    if size_type == 'featured':
                        placeholder_path = self.images_dir / f"{safe_name}-placeholder.jpg"
                        img.save(placeholder_path, 'JPEG', quality=90, optimize=True)
                    
                    return final_path
            
            return None
            
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    def process_tool(self, tool_name, query):
        print(f"\\nProcessing: {tool_name}")
        print(f"Search: {query}")
        
        # Search images
        images = self.search_images(query, 3)
        
        if not images:
            print("  No images found")
            return False
        
        print(f"  Found {len(images)} images")
        success_count = 0
        
        # Process different sizes
        for size_type in self.image_sizes.keys():
            # Use first suitable image
            best_image = None
            for img in images:
                if img['width'] >= self.image_sizes[size_type][0]:
                    best_image = img
                    break
            
            if not best_image and images:
                best_image = images[0]
            
            if best_image:
                image_url = best_image['urls']['regular']
                result = self.download_image(image_url, tool_name, size_type)
                
                if result:
                    success_count += 1
                    print(f"  SUCCESS: {size_type} image saved")
                
                # Delay to avoid rate limiting
                time.sleep(self.request_delay)
        
        return success_count > 0
    
    def process_all_tools(self):
        print("=== Real AI Tool Image Fetcher ===")
        print(f"Processing {len(self.tools)} AI tools...")
        
        for i, (tool_name, query) in enumerate(self.tools.items(), 1):
            print(f"\\n[{i}/{len(self.tools)}] {tool_name}")
            
            success = self.process_tool(tool_name, query)
            
            if success:
                self.stats['processed'] += 1
            else:
                self.stats['errors'] += 1
        
        # Final stats
        print(f"\\n=== COMPLETED ===")
        print(f"Processed: {self.stats['processed']}/{len(self.tools)}")
        print(f"Success rate: {self.stats['processed']/len(self.tools)*100:.1f}%")

def main():
    fetcher = RealImageFetcher()
    fetcher.process_all_tools()

if __name__ == "__main__":
    main()