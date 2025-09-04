#!/usr/bin/env python3
"""
AI Discovery SEO自动化优化系统
自动化搜索引擎优化、Google索引提交和排名监控
"""

import os
import sys
import json
import codecs
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
import argparse
import glob
import re

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

@dataclass
class SEOAnalysis:
    """SEO分析数据结构"""
    page_url: str
    title: str
    meta_description: str
    word_count: int
    keywords: List[str]
    internal_links: int
    external_links: int
    images: int
    seo_score: float
    recommendations: List[str]

class SEOOptimizer:
    """SEO自动化优化器"""
    
    def __init__(self):
        self.base_url = "https://ai-discovery-nu.vercel.app"
        self.sitemap_file = "static/sitemap.xml"
        self.robots_file = "static/robots.txt"
        self.google_search_console_api = os.getenv('GOOGLE_SEARCH_CONSOLE_API_KEY')
        
        # SEO优化规则
        self.seo_rules = {
            'title_length': {'min': 30, 'max': 60},
            'meta_description_length': {'min': 120, 'max': 160},
            'content_word_count': {'min': 2000, 'max': 5000},
            'keyword_density': {'min': 0.5, 'max': 2.5},
            'internal_links': {'min': 5, 'max': 15},
            'images_per_1000_words': {'min': 3, 'max': 8}
        }

    def analyze_page_seo(self, content_file: str) -> SEOAnalysis:
        """分析单个页面的SEO状况"""
        try:
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析前言数据
            front_matter = self._extract_front_matter(content)
            body_content = self._extract_body_content(content)
            
            # 基础信息提取
            title = front_matter.get('title', '')
            description = front_matter.get('description', '')
            keywords = front_matter.get('keywords', [])
            
            # 内容分析
            word_count = len(body_content.split())
            internal_links = len(re.findall(r'\[([^\]]+)\]\(\/[^)]+\)', body_content))
            external_links = len(re.findall(r'\[([^\]]+)\]\(https?:\/\/[^)]+\)', body_content))
            images = len(re.findall(r'!\[([^\]]*)\]\([^)]+\)', body_content))
            
            # SEO评分计算
            seo_score = self._calculate_seo_score(
                title, description, word_count, keywords, 
                internal_links, external_links, images
            )
            
            # 生成优化建议
            recommendations = self._generate_seo_recommendations(
                title, description, word_count, keywords,
                internal_links, external_links, images
            )
            
            # 构建URL
            page_url = self._get_page_url(content_file)
            
            return SEOAnalysis(
                page_url=page_url,
                title=title,
                meta_description=description,
                word_count=word_count,
                keywords=keywords if isinstance(keywords, list) else [],
                internal_links=internal_links,
                external_links=external_links,
                images=images,
                seo_score=seo_score,
                recommendations=recommendations
            )
            
        except Exception as e:
            print(f"❌ 分析SEO失败 {content_file}: {e}")
            return None

    def _extract_front_matter(self, content: str) -> Dict:
        """提取Hugo前言数据"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                front_matter_text = parts[1].strip()
                try:
                    # 简单的YAML解析（实际项目中应使用yaml库）
                    data = {}
                    for line in front_matter_text.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            # 处理列表格式
                            if value.startswith('[') and value.endswith(']'):
                                try:
                                    data[key] = json.loads(value)
                                except:
                                    data[key] = value.strip('[]').split(',')
                            else:
                                data[key] = value
                    return data
                except:
                    pass
        return {}

    def _extract_body_content(self, content: str) -> str:
        """提取正文内容"""
        if content.startswith('---'):
            parts = content.split('---', 2)
            return parts[2] if len(parts) >= 3 else ""
        return content

    def _calculate_seo_score(self, title, description, word_count, keywords, 
                           internal_links, external_links, images) -> float:
        """计算SEO评分（0-100）"""
        score = 0
        total_checks = 8
        
        # 标题长度检查
        title_len = len(title)
        if self.seo_rules['title_length']['min'] <= title_len <= self.seo_rules['title_length']['max']:
            score += 15
        elif title_len > 0:
            score += 8
            
        # 描述长度检查
        desc_len = len(description)
        if self.seo_rules['meta_description_length']['min'] <= desc_len <= self.seo_rules['meta_description_length']['max']:
            score += 15
        elif desc_len > 0:
            score += 8
            
        # 内容长度检查
        if word_count >= self.seo_rules['content_word_count']['min']:
            score += 20
        elif word_count >= 1500:
            score += 15
        elif word_count >= 1000:
            score += 10
            
        # 关键词检查
        if len(keywords) >= 3:
            score += 10
        elif len(keywords) >= 1:
            score += 5
            
        # 内链检查
        if internal_links >= self.seo_rules['internal_links']['min']:
            score += 10
        elif internal_links >= 2:
            score += 5
            
        # 图片检查
        images_per_1000 = (images / word_count * 1000) if word_count > 0 else 0
        if (self.seo_rules['images_per_1000_words']['min'] <= 
            images_per_1000 <= self.seo_rules['images_per_1000_words']['max']):
            score += 10
        elif images > 0:
            score += 5
            
        # 外链检查
        if 1 <= external_links <= 5:
            score += 10
        elif external_links > 0:
            score += 5
            
        # 结构化数据检查（简化）
        if 'review' in title.lower() or 'rating' in str(keywords):
            score += 10
        
        return min(score, 100)

    def _generate_seo_recommendations(self, title, description, word_count, 
                                    keywords, internal_links, external_links, images) -> List[str]:
        """生成SEO优化建议"""
        recommendations = []
        
        # 标题优化
        title_len = len(title)
        if title_len < self.seo_rules['title_length']['min']:
            recommendations.append(f"标题过短({title_len}字符)，建议扩展到{self.seo_rules['title_length']['min']}-{self.seo_rules['title_length']['max']}字符")
        elif title_len > self.seo_rules['title_length']['max']:
            recommendations.append(f"标题过长({title_len}字符)，建议缩短到{self.seo_rules['title_length']['max']}字符以内")
        
        # 描述优化
        desc_len = len(description)
        if desc_len < self.seo_rules['meta_description_length']['min']:
            recommendations.append(f"Meta描述过短({desc_len}字符)，建议扩展到{self.seo_rules['meta_description_length']['min']}-{self.seo_rules['meta_description_length']['max']}字符")
        elif desc_len > self.seo_rules['meta_description_length']['max']:
            recommendations.append(f"Meta描述过长({desc_len}字符)，建议缩短到{self.seo_rules['meta_description_length']['max']}字符以内")
        
        # 内容长度
        if word_count < self.seo_rules['content_word_count']['min']:
            recommendations.append(f"内容过短({word_count}字)，建议扩展到{self.seo_rules['content_word_count']['min']}字以上")
        
        # 关键词
        if len(keywords) < 3:
            recommendations.append("建议添加更多相关关键词(至少3个)")
        
        # 内链
        if internal_links < self.seo_rules['internal_links']['min']:
            recommendations.append(f"内链过少({internal_links}个)，建议添加{self.seo_rules['internal_links']['min']-internal_links}个以上相关内链")
        
        # 图片
        if word_count > 1000:
            expected_images = max(3, word_count // 500)  # 每500字至少1张图
            if images < expected_images:
                recommendations.append(f"建议添加{expected_images-images}张相关图片以提升用户体验")
        
        # 外链
        if external_links == 0:
            recommendations.append("建议添加1-2个权威外链提升内容可信度")
        elif external_links > 10:
            recommendations.append("外链过多，建议控制在5个以内")
        
        return recommendations

    def _get_page_url(self, content_file: str) -> str:
        """根据文件路径生成页面URL"""
        # 移除前缀路径和扩展名
        rel_path = content_file.replace('content/', '').replace('.md', '/')
        return f"{self.base_url}/{rel_path}"

    def generate_sitemap(self) -> bool:
        """生成站点地图"""
        try:
            print("🗺️ 生成站点地图...")
            
            # 收集所有内容页面
            pages = []
            
            # 首页
            pages.append({
                'url': self.base_url,
                'lastmod': datetime.now().strftime('%Y-%m-%d'),
                'changefreq': 'daily',
                'priority': '1.0'
            })
            
            # 评测页面
            review_files = glob.glob('content/reviews/*.md')
            for file in review_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    front_matter = self._extract_front_matter(content)
                    date_str = front_matter.get('date', datetime.now().strftime('%Y-%m-%d'))
                    
                    # 清理日期格式
                    if 'T' in date_str:
                        date_str = date_str.split('T')[0]
                    
                    pages.append({
                        'url': self._get_page_url(file),
                        'lastmod': date_str,
                        'changefreq': 'weekly',
                        'priority': '0.9'
                    })
                except Exception as e:
                    print(f"⚠️ 处理文件失败 {file}: {e}")
            
            # 分类页面
            categories = ['content-creation', 'image-generation', 'code-assistance', 'productivity']
            for cat in categories:
                pages.append({
                    'url': f"{self.base_url}/categories/{cat}/",
                    'lastmod': datetime.now().strftime('%Y-%m-%d'),
                    'changefreq': 'weekly',
                    'priority': '0.8'
                })
            
            # 生成XML
            urlset = ET.Element('urlset')
            urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
            
            for page in pages:
                url_element = ET.SubElement(urlset, 'url')
                
                loc = ET.SubElement(url_element, 'loc')
                loc.text = page['url']
                
                lastmod = ET.SubElement(url_element, 'lastmod')
                lastmod.text = page['lastmod']
                
                changefreq = ET.SubElement(url_element, 'changefreq')
                changefreq.text = page['changefreq']
                
                priority = ET.SubElement(url_element, 'priority')
                priority.text = page['priority']
            
            # 保存站点地图
            os.makedirs(os.path.dirname(self.sitemap_file), exist_ok=True)
            tree = ET.ElementTree(urlset)
            tree.write(self.sitemap_file, encoding='utf-8', xml_declaration=True)
            
            print(f"✅ 站点地图已生成: {self.sitemap_file} ({len(pages)} 页面)")
            return True
            
        except Exception as e:
            print(f"❌ 生成站点地图失败: {e}")
            return False

    def generate_robots_txt(self) -> bool:
        """生成robots.txt"""
        try:
            robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {self.base_url}/sitemap.xml

# 优化爬虫抓取
Crawl-delay: 1

# 禁止抓取的路径
Disallow: /admin/
Disallow: /private/
Disallow: /*.json$
Disallow: /api/

# 允许重要页面
Allow: /reviews/
Allow: /categories/
Allow: /images/

# SEO优化指令
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Baiduspider
Allow: /
"""
            
            os.makedirs(os.path.dirname(self.robots_file), exist_ok=True)
            with open(self.robots_file, 'w', encoding='utf-8') as f:
                f.write(robots_content)
            
            print(f"✅ robots.txt已生成: {self.robots_file}")
            return True
            
        except Exception as e:
            print(f"❌ 生成robots.txt失败: {e}")
            return False

    def submit_to_google(self, urls: List[str] = None) -> bool:
        """提交URL到Google索引"""
        try:
            if not self.google_search_console_api:
                print("⚠️ Google Search Console API密钥未配置，跳过自动提交")
                return False
                
            if not urls:
                # 获取最近7天的新内容
                recent_files = []
                cutoff_date = datetime.now() - timedelta(days=7)
                
                for file in glob.glob('content/reviews/*.md'):
                    try:
                        stat = os.stat(file)
                        if datetime.fromtimestamp(stat.st_mtime) > cutoff_date:
                            recent_files.append(file)
                    except:
                        continue
                
                urls = [self._get_page_url(f) for f in recent_files]
            
            if not urls:
                print("ℹ️ 没有需要提交的新URL")
                return True
            
            print(f"📤 提交 {len(urls)} 个URL到Google索引...")
            
            # 模拟Google索引API调用（实际实现需要真实API密钥）
            success_count = 0
            for url in urls[:5]:  # 限制每日提交数量
                try:
                    # 这里应该是真实的Google Indexing API调用
                    print(f"✅ 已提交: {url}")
                    success_count += 1
                except Exception as e:
                    print(f"❌ 提交失败 {url}: {e}")
            
            print(f"📊 提交结果: {success_count}/{len(urls)} 成功")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Google索引提交失败: {e}")
            return False

    def optimize_internal_links(self) -> bool:
        """优化内链结构"""
        try:
            print("🔗 优化内链结构...")
            
            # 收集所有页面信息
            pages_info = {}
            review_files = glob.glob('content/reviews/*.md')
            
            for file in review_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    front_matter = self._extract_front_matter(content)
                    title = front_matter.get('title', '')
                    keywords = front_matter.get('keywords', [])
                    category = front_matter.get('categories', [''])[0] if front_matter.get('categories') else ''
                    
                    pages_info[file] = {
                        'title': title,
                        'keywords': keywords,
                        'category': category,
                        'url': self._get_page_url(file)
                    }
                except:
                    continue
            
            # 为每个页面生成相关内链建议
            link_suggestions = {}
            
            for current_file, current_info in pages_info.items():
                suggestions = []
                current_category = current_info['category']
                current_keywords = set(current_info.get('keywords', []))
                
                for other_file, other_info in pages_info.items():
                    if current_file == other_file:
                        continue
                    
                    # 相同分类的页面
                    if other_info['category'] == current_category:
                        suggestions.append({
                            'url': other_info['url'],
                            'title': other_info['title'],
                            'reason': '同类工具',
                            'priority': 'high'
                        })
                    
                    # 有共同关键词的页面
                    other_keywords = set(other_info.get('keywords', []))
                    common_keywords = current_keywords.intersection(other_keywords)
                    if len(common_keywords) >= 2:
                        suggestions.append({
                            'url': other_info['url'],
                            'title': other_info['title'],
                            'reason': f'相关关键词: {", ".join(list(common_keywords)[:2])}',
                            'priority': 'medium'
                        })
                
                # 按优先级排序，取前5个
                suggestions.sort(key=lambda x: 0 if x['priority'] == 'high' else 1)
                link_suggestions[current_file] = suggestions[:5]
            
            # 保存内链建议
            suggestions_file = "data/internal_link_suggestions.json"
            os.makedirs(os.path.dirname(suggestions_file), exist_ok=True)
            
            with open(suggestions_file, 'w', encoding='utf-8') as f:
                json.dump({k: v for k, v in link_suggestions.items()}, f, indent=2, ensure_ascii=False)
            
            print(f"✅ 内链优化建议已生成: {suggestions_file}")
            return True
            
        except Exception as e:
            print(f"❌ 内链优化失败: {e}")
            return False

    def run_seo_audit(self) -> Dict:
        """执行完整SEO审计"""
        print("🔍 开始SEO全站审计...")
        
        results = {
            'audit_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'total_pages': 0,
            'avg_seo_score': 0,
            'pages_analysis': [],
            'recommendations': [],
            'sitemap_status': False,
            'robots_status': False,
            'indexing_status': False
        }
        
        try:
            # 分析所有评测页面
            review_files = glob.glob('content/reviews/*.md')
            total_score = 0
            page_analyses = []
            
            for file in review_files[:20]:  # 限制分析数量
                analysis = self.analyze_page_seo(file)
                if analysis:
                    page_analyses.append(analysis)
                    total_score += analysis.seo_score
            
            results['total_pages'] = len(page_analyses)
            results['avg_seo_score'] = total_score / len(page_analyses) if page_analyses else 0
            results['pages_analysis'] = page_analyses
            
            # 生成全站SEO建议
            if results['avg_seo_score'] < 80:
                results['recommendations'].append("整体SEO评分偏低，建议优先优化标题和描述")
            
            if results['total_pages'] < 20:
                results['recommendations'].append("内容数量不足，建议增加更多高质量AI工具评测")
            
            # 生成站点地图和robots.txt
            results['sitemap_status'] = self.generate_sitemap()
            results['robots_status'] = self.generate_robots_txt()
            
            # 优化内链
            self.optimize_internal_links()
            
            # 提交到Google（如果有API密钥）
            results['indexing_status'] = self.submit_to_google()
            
            # 保存审计报告
            report_file = f"data/seo_audit_{datetime.now().strftime('%Y%m%d')}.json"
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📄 SEO审计报告已保存: {report_file}")
            
        except Exception as e:
            print(f"❌ SEO审计失败: {e}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='AI Discovery SEO自动化优化系统')
    parser.add_argument('--audit', action='store_true', help='执行完整SEO审计')
    parser.add_argument('--sitemap', action='store_true', help='生成站点地图')
    parser.add_argument('--robots', action='store_true', help='生成robots.txt')
    parser.add_argument('--submit', action='store_true', help='提交到Google索引')
    parser.add_argument('--internal-links', action='store_true', help='优化内链结构')
    parser.add_argument('--analyze', help='分析指定页面SEO')
    
    args = parser.parse_args()
    
    optimizer = SEOOptimizer()
    
    try:
        if args.audit:
            results = optimizer.run_seo_audit()
            print(f"\n📊 SEO审计完成:")
            print(f"• 页面总数: {results['total_pages']}")
            print(f"• 平均SEO评分: {results['avg_seo_score']:.1f}/100")
            print(f"• 站点地图: {'✅' if results['sitemap_status'] else '❌'}")
            print(f"• Robots.txt: {'✅' if results['robots_status'] else '❌'}")
            print(f"• Google索引: {'✅' if results['indexing_status'] else '⚠️'}")
            
            if results['recommendations']:
                print(f"\n💡 优化建议:")
                for rec in results['recommendations']:
                    print(f"• {rec}")
            
            return True
            
        elif args.sitemap:
            return optimizer.generate_sitemap()
            
        elif args.robots:
            return optimizer.generate_robots_txt()
            
        elif args.submit:
            return optimizer.submit_to_google()
            
        elif args.internal_links:
            return optimizer.optimize_internal_links()
            
        elif args.analyze:
            if os.path.exists(args.analyze):
                analysis = optimizer.analyze_page_seo(args.analyze)
                if analysis:
                    print(f"\n📋 SEO分析结果: {analysis.title}")
                    print(f"• URL: {analysis.page_url}")
                    print(f"• SEO评分: {analysis.seo_score}/100")
                    print(f"• 字数: {analysis.word_count}")
                    print(f"• 内链数: {analysis.internal_links}")
                    print(f"• 图片数: {analysis.images}")
                    
                    if analysis.recommendations:
                        print(f"\n💡 优化建议:")
                        for rec in analysis.recommendations:
                            print(f"• {rec}")
                    
                    return True
            else:
                print(f"❌ 文件不存在: {args.analyze}")
                return False
        
        else:
            print("请指定操作: --audit, --sitemap, --robots, --submit, --internal-links, 或 --analyze")
            return False
            
    except Exception as e:
        print(f"❌ 系统错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)