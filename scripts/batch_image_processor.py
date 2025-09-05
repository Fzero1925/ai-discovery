#!/usr/bin/env python3
"""
AI Discovery批量图片处理器

为所有AI工具创建高质量的placeholder图片和真实图片处理
"""

import os
import sys
import codecs
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import colorsys

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# 添加模块路径
sys.path.append(str(Path(__file__).parent.parent))
from modules.image_processor.ai_tool_image_handler import AIToolImageHandler


class BatchImageProcessor:
    """批量图片处理器"""
    
    def __init__(self):
        self.images_dir = Path("static/images/tools")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # AI工具类别颜色映射
        self.category_colors = {
            'content_creation': '#4F46E5',    # Indigo
            'image_generation': '#EC4899',    # Pink  
            'code_assistance': '#10B981',     # Emerald
            'productivity': '#F59E0B',        # Amber
            'data_analysis': '#8B5CF6'        # Purple
        }
        
        # 常见AI工具及其类别
        self.tools_catalog = {
            'ChatGPT': 'content_creation',
            'Claude': 'content_creation', 
            'Jasper AI': 'content_creation',
            'Copy.ai': 'content_creation',
            'Midjourney': 'image_generation',
            'DALL-E 3': 'image_generation',
            'Stable Diffusion': 'image_generation',
            'Adobe Firefly': 'image_generation',
            'GitHub Copilot': 'code_assistance',
            'Codeium': 'code_assistance',
            'Amazon CodeWhisperer': 'code_assistance',
            'TabNine': 'code_assistance',
            'Grammarly': 'productivity',
            'Notion AI': 'productivity',
            'Zapier': 'productivity',
            'Tableau': 'data_analysis',
            'DataRobot': 'data_analysis',
            'Power BI': 'data_analysis'
        }
        
        # 图片尺寸设置
        self.image_sizes = {
            'featured': (1200, 630),      # OG image size
            'thumbnail': (400, 300),      # Card thumbnail
            'icon': (150, 150)            # Small icon
        }
    
    def hex_to_rgb(self, hex_color: str) -> tuple:
        """转换十六进制颜色到RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def get_complementary_color(self, hex_color: str) -> str:
        """获取补色"""
        rgb = self.hex_to_rgb(hex_color)
        # 转换到HSV
        h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        # 获取补色（色相+180度）
        comp_h = (h + 0.5) % 1.0
        comp_rgb = colorsys.hsv_to_rgb(comp_h, s * 0.7, v * 0.9)
        # 转换回RGB并格式化
        comp_rgb = tuple(int(c * 255) for c in comp_rgb)
        return f"#{comp_rgb[0]:02x}{comp_rgb[1]:02x}{comp_rgb[2]:02x}"
    
    def create_gradient_background(self, size: tuple, color1: str, color2: str) -> Image.Image:
        """创建渐变背景"""
        width, height = size
        img = Image.new('RGB', size, color1)
        draw = ImageDraw.Draw(img)
        
        # 创建径向渐变
        center_x, center_y = width // 2, height // 2
        max_radius = max(width, height) // 2
        
        rgb1 = self.hex_to_rgb(color1)
        rgb2 = self.hex_to_rgb(color2)
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                ratio = min(distance / max_radius, 1.0)
                
                # 线性插值
                r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
                g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
                b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
                
                img.putpixel((x, y), (r, g, b))
        
        return img
    
    def create_tool_placeholder(self, tool_name: str, category: str, size: tuple = (1200, 630)) -> Image.Image:
        """为AI工具创建高质量placeholder图片"""
        
        # 获取类别颜色
        primary_color = self.category_colors.get(category, '#6B7280')
        secondary_color = self.get_complementary_color(primary_color)
        
        # 创建渐变背景
        img = self.create_gradient_background(size, primary_color, secondary_color)
        draw = ImageDraw.Draw(img)
        
        width, height = size
        
        # 添加几何装饰
        # 大圆圈
        circle_radius = min(width, height) // 4
        circle_center = (width // 4, height // 4)
        circle_bbox = [
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ]
        draw.ellipse(circle_bbox, fill=None, outline='white', width=3)
        
        # 小方块装饰
        square_size = 60
        square_pos = (width - 150, height - 150)
        square_bbox = [
            square_pos[0],
            square_pos[1],
            square_pos[0] + square_size,
            square_pos[1] + square_size
        ]
        draw.rectangle(square_bbox, fill='white', outline=None)
        
        # 波浪线装饰
        wave_y = height // 3
        wave_points = []
        for x in range(0, width, 20):
            y_offset = 30 * (0.5 + 0.5 * (x / width))
            wave_points.extend([x, wave_y + y_offset])
        if len(wave_points) > 2:
            draw.line(wave_points, fill='white', width=2)
        
        # 加载字体（尝试系统字体，否则使用默认）
        try:
            # Windows系统字体
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
        except:
            try:
                # 备选字体
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
        
        # 添加工具名称
        text_y = height // 2 - 50
        draw.text(
            (width // 2, text_y),
            tool_name,
            font=title_font,
            fill='white',
            anchor='mm'
        )
        
        # 添加类别标签
        category_text = category.replace('_', ' ').title()
        draw.text(
            (width // 2, text_y + 60),
            category_text,
            font=subtitle_font,
            fill='white',
            anchor='mm'
        )
        
        # 添加AI标识
        ai_text = "AI TOOL"
        # 使用半透明白色 (200, 200, 200)
        draw.text(
            (width // 2, text_y + 100),
            ai_text,
            font=subtitle_font,
            fill=(200, 200, 200),
            anchor='mm'
        )
        
        return img
    
    def process_all_tools(self):
        """为所有工具创建图片"""
        print("🎨 开始批量创建AI工具图片...")
        
        created_count = 0
        
        for tool_name, category in self.tools_catalog.items():
            try:
                # 创建各种尺寸的图片
                for size_name, size in self.image_sizes.items():
                    # 生成文件名
                    safe_name = tool_name.lower().replace(' ', '-').replace('.', '')
                    filename = f"{safe_name}-{size_name}.jpg"
                    filepath = self.images_dir / filename
                    
                    # 如果文件已存在且较新，则跳过
                    if filepath.exists():
                        print(f"  ⚪ 跳过已存在: {filename}")
                        continue
                    
                    # 创建图片
                    img = self.create_tool_placeholder(tool_name, category, size)
                    
                    # 保存图片
                    img.save(filepath, format='JPEG', quality=90, optimize=True)
                    created_count += 1
                    
                    print(f"  ✅ 创建成功: {filename} ({size[0]}x{size[1]})")
                
                # 创建主要的placeholder文件（用于featured_image）
                main_filename = f"{tool_name.lower().replace(' ', '-').replace('.', '')}-placeholder.jpg"
                main_filepath = self.images_dir / main_filename
                
                if not main_filepath.exists():
                    main_img = self.create_tool_placeholder(tool_name, category, self.image_sizes['featured'])
                    main_img.save(main_filepath, format='JPEG', quality=90, optimize=True)
                    created_count += 1
                    print(f"  🎯 创建主图: {main_filename}")
                
            except Exception as e:
                print(f"  ❌ 创建失败: {tool_name}, Error: {e}")
        
        print(f"\n🎉 图片创建完成! 总计创建 {created_count} 张图片")
        return created_count
    
    def optimize_all_images(self):
        """使用性能优化器优化所有图片"""
        print("\n⚡ 开始图片性能优化...")
        
        try:
            # 导入性能优化器
            sys.path.append(str(Path(__file__).parent))
            from performance_optimizer import PerformanceOptimizer
            
            optimizer = PerformanceOptimizer()
            results = optimizer.optimize_images()
            
            print(f"✅ 图片优化完成:")
            print(f"  📊 处理数量: {results.get('processed_count', 0)}")
            print(f"  📈 压缩比: {results.get('compression_ratio', 0):.1f}%")
            print(f"  💾 节省空间: {(results.get('total_size_before', 0) - results.get('total_size_after', 0)) / 1024:.1f}KB")
            
            return results
            
        except Exception as e:
            print(f"⚠️ 图片优化遇到问题: {e}")
            return None
    
    def update_article_image_paths(self):
        """更新文章中的图片路径"""
        print("\n🔗 更新文章图片路径...")
        
        content_dir = Path("content/reviews")
        if not content_dir.exists():
            print("❌ 内容目录不存在")
            return
        
        updated_count = 0
        
        for md_file in content_dir.glob("*.md"):
            if md_file.name == "_index.md":
                continue
            
            try:
                # 读取文件内容
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否需要更新featured_image路径
                if 'featured_image:' in content:
                    # 提取工具名称来匹配图片
                    for tool_name in self.tools_catalog.keys():
                        tool_key = tool_name.lower().replace(' ', '-').replace('.', '')
                        if tool_key in md_file.stem.lower():
                            old_pattern = f'featured_image: /images/tools/{tool_key}.jpg'
                            new_pattern = f'featured_image: /images/tools/{tool_key}-placeholder.jpg'
                            
                            if old_pattern in content:
                                content = content.replace(old_pattern, new_pattern)
                                updated_count += 1
                                print(f"  🔄 更新: {md_file.name}")
                                break
                
                # 写回文件
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
            except Exception as e:
                print(f"  ❌ 更新失败: {md_file.name}, Error: {e}")
        
        print(f"✅ 图片路径更新完成，共更新 {updated_count} 个文件")
        return updated_count


def main():
    """主函数"""
    print("🎨 AI Discovery 批量图片处理器")
    print("=" * 50)
    
    processor = BatchImageProcessor()
    
    # 第一步：创建所有工具的placeholder图片
    created_count = processor.process_all_tools()
    
    # 第二步：优化图片性能
    if created_count > 0:
        processor.optimize_all_images()
    
    # 第三步：更新文章中的图片路径
    processor.update_article_image_paths()
    
    print("\n🎉 批量图片处理完成!")


if __name__ == "__main__":
    main()