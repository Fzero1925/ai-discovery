#!/usr/bin/env python3
"""
AI Discovery - 内容质量分析器
Analyze the quality of generated AI tool reviews
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime

# Add modules to path
sys.path.append('modules')
from content_generator.ai_tool_content_generator import AIToolContentGenerator

class ContentQualityAnalyzer:
    """分析AI工具评测内容的质量"""
    
    def __init__(self):
        self.content_dir = Path('content/reviews')
        self.generator = AIToolContentGenerator()
        
    def analyze_content_files(self) -> Dict:
        """分析所有评测文件的质量指标"""
        print("=" * 60)
        print("AI Discovery - 内容质量分析")
        print("=" * 60)
        
        if not self.content_dir.exists():
            print("[ERROR] 内容目录不存在")
            return {}
        
        files = list(self.content_dir.glob('*.md'))
        print(f"[INFO] 发现 {len(files)} 个评测文件")
        
        results = {
            'total_files': len(files),
            'total_words': 0,
            'total_characters': 0,
            'files_analysis': [],
            'quality_metrics': {},
            'seo_analysis': {},
            'generated_at': datetime.now().isoformat()
        }
        
        for file_path in files:
            file_analysis = self._analyze_single_file(file_path)
            results['files_analysis'].append(file_analysis)
            
        # 计算总体统计
        results['total_words'] = sum(f['word_count'] for f in results['files_analysis'])
        results['total_characters'] = sum(f['character_count'] for f in results['files_analysis'])
        
        # 质量指标分析
        results['quality_metrics'] = self._calculate_quality_metrics(results['files_analysis'])
        
        # SEO分析
        results['seo_analysis'] = self._analyze_seo_quality(results['files_analysis'])
        
        return results
    
    def _analyze_single_file(self, file_path: Path) -> Dict:
        """分析单个文件的质量"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 分离Front Matter和内容
            parts = content.split('---', 2)
            if len(parts) >= 3:
                front_matter = parts[1].strip()
                body_content = parts[2].strip()
            else:
                front_matter = ""
                body_content = content
            
            # 基本统计
            word_count = len(re.findall(r'\b\w+\b', body_content))
            character_count = len(body_content)
            
            # 结构分析
            structure_analysis = self._analyze_structure(body_content)
            
            # SEO分析
            seo_analysis = self._analyze_seo_elements(front_matter, body_content)
            
            # 可读性分析
            readability = self._analyze_readability(body_content)
            
            return {
                'filename': file_path.name,
                'word_count': word_count,
                'character_count': character_count,
                'structure': structure_analysis,
                'seo': seo_analysis,
                'readability': readability,
                'front_matter_valid': bool(front_matter),
            }
            
        except Exception as e:
            print(f"[ERROR] 分析文件 {file_path.name} 失败: {e}")
            return {
                'filename': file_path.name,
                'error': str(e)
            }
    
    def _analyze_structure(self, content: str) -> Dict:
        """分析文章结构"""
        # 统计标题数量
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        h3_count = len(re.findall(r'^### ', content, re.MULTILINE))
        
        # 检查是否包含标准6个模块
        required_sections = [
            "工具简介", "Tool Introduction", "Introduction",
            "核心亮点", "Core Features", "Features", 
            "使用场景", "Use Cases", "Applications",
            "社区评测", "Community Reviews", "Reviews",
            "使用渠道", "Access Information", "Pricing",
            "FAQ", "注意事项", "Notes"
        ]
        
        sections_found = 0
        for section in required_sections:
            if section.lower() in content.lower():
                sections_found += 1
                break  # Count each type only once
        
        return {
            'h1_count': h1_count,
            'h2_count': h2_count, 
            'h3_count': h3_count,
            'total_headings': h1_count + h2_count + h3_count,
            'has_standard_structure': sections_found >= 4  # At least 4 of 6 sections
        }
    
    def _analyze_seo_elements(self, front_matter: str, content: str) -> Dict:
        """分析SEO元素"""
        seo_score = 0
        total_checks = 7
        
        # 检查title
        has_title = 'title:' in front_matter
        if has_title:
            seo_score += 1
            title_match = re.search(r'title:\s*["\']?([^"\']+)["\']?', front_matter)
            title_length = len(title_match.group(1)) if title_match else 0
        else:
            title_length = 0
        
        # 检查description
        has_description = 'description:' in front_matter
        if has_description:
            seo_score += 1
            desc_match = re.search(r'description:\s*["\']?([^"\']+)["\']?', front_matter)
            desc_length = len(desc_match.group(1)) if desc_match else 0
        else:
            desc_length = 0
        
        # 检查tags
        has_tags = 'tags:' in front_matter
        if has_tags:
            seo_score += 1
        
        # 检查categories
        has_categories = 'categories:' in front_matter
        if has_categories:
            seo_score += 1
        
        # 检查内容长度（SEO友好）
        word_count = len(re.findall(r'\b\w+\b', content))
        if word_count >= 2000:  # 长文章对SEO有利
            seo_score += 1
        
        # 检查内链
        internal_links = len(re.findall(r'\[([^\]]+)\]\((?!http)', content))
        if internal_links > 0:
            seo_score += 1
        
        # 检查关键词密度适中（避免过度优化）
        ai_keyword_count = len(re.findall(r'\bAI\b', content, re.IGNORECASE))
        total_words = len(re.findall(r'\b\w+\b', content))
        keyword_density = (ai_keyword_count / total_words * 100) if total_words > 0 else 0
        if 1 <= keyword_density <= 3:  # 1-3%的关键词密度较好
            seo_score += 1
        
        return {
            'seo_score': seo_score,
            'seo_percentage': (seo_score / total_checks) * 100,
            'has_title': has_title,
            'title_length': title_length,
            'has_description': has_description,
            'description_length': desc_length,
            'has_tags': has_tags,
            'has_categories': has_categories,
            'word_count': word_count,
            'internal_links': internal_links,
            'keyword_density': keyword_density
        }
    
    def _analyze_readability(self, content: str) -> Dict:
        """分析内容可读性"""
        sentences = len(re.split(r'[.!?]+', content))
        words = len(re.findall(r'\b\w+\b', content))
        paragraphs = len(re.split(r'\n\s*\n', content.strip()))
        
        # 平均句子长度
        avg_sentence_length = words / sentences if sentences > 0 else 0
        
        # 平均段落长度
        avg_paragraph_length = words / paragraphs if paragraphs > 0 else 0
        
        # 可读性评分（简化版）
        readability_score = 100
        if avg_sentence_length > 25:  # 句子太长扣分
            readability_score -= 10
        if avg_paragraph_length > 150:  # 段落太长扣分
            readability_score -= 10
        if sentences / paragraphs < 2:  # 段落句子太少扣分
            readability_score -= 5
        
        return {
            'sentences': sentences,
            'words': words,
            'paragraphs': paragraphs,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_paragraph_length': round(avg_paragraph_length, 1),
            'readability_score': max(0, readability_score)
        }
    
    def _calculate_quality_metrics(self, files_analysis: List[Dict]) -> Dict:
        """计算整体质量指标"""
        if not files_analysis:
            return {}
        
        # 过滤出有效的分析结果
        valid_files = [f for f in files_analysis if 'error' not in f]
        
        if not valid_files:
            return {'error': 'No valid files to analyze'}
        
        # 计算平均值
        avg_word_count = sum(f['word_count'] for f in valid_files) / len(valid_files)
        avg_char_count = sum(f['character_count'] for f in valid_files) / len(valid_files)
        avg_seo_score = sum(f['seo']['seo_percentage'] for f in valid_files) / len(valid_files)
        avg_readability = sum(f['readability']['readability_score'] for f in valid_files) / len(valid_files)
        
        # 结构完整性
        structure_complete = sum(1 for f in valid_files if f['structure']['has_standard_structure'])
        structure_percentage = (structure_complete / len(valid_files)) * 100
        
        return {
            'average_word_count': round(avg_word_count, 1),
            'average_character_count': round(avg_char_count, 1),
            'average_seo_score': round(avg_seo_score, 1),
            'average_readability': round(avg_readability, 1),
            'structure_complete_percentage': round(structure_percentage, 1),
            'total_valid_files': len(valid_files),
            'files_with_errors': len(files_analysis) - len(valid_files)
        }
    
    def _analyze_seo_quality(self, files_analysis: List[Dict]) -> Dict:
        """分析SEO质量"""
        valid_files = [f for f in files_analysis if 'error' not in f]
        
        if not valid_files:
            return {}
        
        # SEO指标统计
        titles_good = sum(1 for f in valid_files 
                         if f['seo']['has_title'] and 30 <= f['seo']['title_length'] <= 60)
        descriptions_good = sum(1 for f in valid_files 
                               if f['seo']['has_description'] and 120 <= f['seo']['description_length'] <= 160)
        
        return {
            'titles_optimal_length': f"{titles_good}/{len(valid_files)}",
            'descriptions_optimal_length': f"{descriptions_good}/{len(valid_files)}",
            'average_keyword_density': round(sum(f['seo']['keyword_density'] for f in valid_files) / len(valid_files), 2)
        }
    
    def print_analysis_report(self, results: Dict):
        """打印分析报告"""
        print(f"\n[REPORT] 内容质量分析报告")
        print("=" * 50)
        
        print(f"总文件数量: {results['total_files']}")
        print(f"总字数: {results['total_words']:,}")
        print(f"总字符数: {results['total_characters']:,}")
        
        if 'quality_metrics' in results and results['quality_metrics']:
            metrics = results['quality_metrics']
            print(f"\n[QUALITY METRICS]")
            print(f"平均字数: {metrics['average_word_count']}")
            print(f"平均字符数: {metrics['average_character_count']}")
            print(f"平均SEO得分: {metrics['average_seo_score']:.1f}%")
            print(f"平均可读性得分: {metrics['average_readability']:.1f}")
            print(f"结构完整性: {metrics['structure_complete_percentage']:.1f}%")
        
        if 'seo_analysis' in results and results['seo_analysis']:
            seo = results['seo_analysis']
            print(f"\n[SEO ANALYSIS]")
            print(f"标题长度优化: {seo['titles_optimal_length']}")
            print(f"描述长度优化: {seo['descriptions_optimal_length']}")
            print(f"平均关键词密度: {seo['average_keyword_density']:.2f}%")
        
        # 显示每个文件的详细信息
        print(f"\n[FILES DETAILS]")
        for file_analysis in results.get('files_analysis', [])[:5]:  # 只显示前5个
            if 'error' not in file_analysis:
                print(f"  {file_analysis['filename']}: {file_analysis['word_count']} words, SEO: {file_analysis['seo']['seo_percentage']:.1f}%")
        
        if len(results.get('files_analysis', [])) > 5:
            print(f"  ... and {len(results['files_analysis']) - 5} more files")
    
    def save_analysis_report(self, results: Dict, filename: str = "content_quality_report.json"):
        """保存分析报告到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n[SUCCESS] 分析报告已保存至: {filename}")
        except Exception as e:
            print(f"[ERROR] 保存报告失败: {e}")

def main():
    analyzer = ContentQualityAnalyzer()
    results = analyzer.analyze_content_files()
    
    if results:
        analyzer.print_analysis_report(results)
        analyzer.save_analysis_report(results)
        
        # 给出优化建议
        if 'quality_metrics' in results and results['quality_metrics']:
            metrics = results['quality_metrics']
            print(f"\n[RECOMMENDATIONS]")
            if metrics['average_seo_score'] < 80:
                print("- 建议优化SEO元素（标题、描述、标签）")
            if metrics['average_word_count'] < 2000:
                print("- 建议增加文章长度以提升SEO效果")
            if metrics['structure_complete_percentage'] < 90:
                print("- 建议完善文章结构（6模块评测体系）")
    
    return results

if __name__ == "__main__":
    main()