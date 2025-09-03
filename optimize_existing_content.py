#!/usr/bin/env python3
"""
优化现有内容 - 使用增强版生成器重新生成高质量文章
Optimize existing content using enhanced generator
"""

import sys
import os
from pathlib import Path
from datetime import datetime
sys.path.append('.')

from enhanced_content_generator import EnhancedContentGenerator

def optimize_existing_articles():
    """使用增强版生成器优化现有文章"""
    print("=" * 60)
    print("AI Discovery - 内容优化升级")
    print("=" * 60)
    
    # 初始化增强版生成器
    try:
        generator = EnhancedContentGenerator()
        print("[SUCCESS] 增强版生成器初始化成功")
    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        return False
    
    # 选择要优化的文章（优先选择重要工具）
    optimization_targets = [
        {
            'tool': 'Claude',
            'keywords': ['Claude AI review', 'best AI assistant 2025', 'Claude vs ChatGPT', 'AI content creation'],
            'old_file': 'content/reviews/claude-comprehensive-review.md',
            'new_file': 'content/reviews/claude-ultimate-review-2025.md'
        },
        {
            'tool': 'Stable Diffusion', 
            'keywords': ['Stable Diffusion review', 'free AI image generator', 'open source AI art', 'SD tutorial'],
            'old_file': 'content/reviews/stable-diffusion-comprehensive-review.md',
            'new_file': 'content/reviews/stable-diffusion-complete-guide-2025.md'
        },
        {
            'tool': 'Grammarly',
            'keywords': ['Grammarly review', 'writing assistant tool', 'grammar checker 2025', 'writing improvement'],
            'old_file': 'content/reviews/grammarly-comprehensive-review.md', 
            'new_file': 'content/reviews/grammarly-detailed-review-2025.md'
        },
        {
            'tool': 'Codeium',
            'keywords': ['Codeium review', 'free AI coding assistant', 'code completion tool', 'programming AI'],
            'old_file': 'content/reviews/codeium-comprehensive-review.md',
            'new_file': 'content/reviews/codeium-developer-guide-2025.md'
        }
    ]
    
    optimization_results = {
        'successful': [],
        'failed': [],
        'metrics': {}
    }
    
    for i, target in enumerate(optimization_targets, 1):
        try:
            print(f"\n[{i}/{len(optimization_targets)}] 优化工具: {target['tool']}")
            
            # 生成增强版内容
            enhanced_content = generator.generate_enhanced_ai_tool_review(
                target['tool'], 
                target['keywords']
            )
            
            if enhanced_content:
                # 保存新文件
                new_file_path = Path(target['new_file'])
                new_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_content)
                
                # 计算改进指标
                old_size = 0
                if Path(target['old_file']).exists():
                    with open(target['old_file'], 'r', encoding='utf-8') as f:
                        old_content = f.read()
                        old_size = len(old_content)
                
                new_size = len(enhanced_content)
                improvement = ((new_size - old_size) / old_size * 100) if old_size > 0 else 0
                
                optimization_results['successful'].append({
                    'tool': target['tool'],
                    'old_size': old_size,
                    'new_size': new_size,
                    'improvement': improvement,
                    'file': target['new_file']
                })
                
                print(f"  [SUCCESS] 生成完成: {target['new_file']}")
                print(f"  [METRICS] 原文: {old_size} -> 新文: {new_size} 字符 ({improvement:+.1f}% 改进)")
                
            else:
                print(f"  [ERROR] 内容生成失败: {target['tool']}")
                optimization_results['failed'].append(target['tool'])
                
        except Exception as e:
            print(f"  [ERROR] 优化 {target['tool']} 失败: {e}")
            optimization_results['failed'].append(target['tool'])
    
    # 计算总体指标
    if optimization_results['successful']:
        total_old_size = sum(r['old_size'] for r in optimization_results['successful'])
        total_new_size = sum(r['new_size'] for r in optimization_results['successful'])
        avg_improvement = sum(r['improvement'] for r in optimization_results['successful']) / len(optimization_results['successful'])
        
        optimization_results['metrics'] = {
            'total_old_size': total_old_size,
            'total_new_size': total_new_size,
            'total_improvement': ((total_new_size - total_old_size) / total_old_size * 100) if total_old_size > 0 else 0,
            'average_improvement': avg_improvement,
            'successful_count': len(optimization_results['successful']),
            'failed_count': len(optimization_results['failed'])
        }
    
    return optimization_results

def print_optimization_report(results):
    """打印优化报告"""
    print("\n" + "=" * 60)
    print("内容优化完成报告")
    print("=" * 60)
    
    print(f"成功优化: {results['metrics']['successful_count']} 篇文章")
    print(f"优化失败: {results['metrics']['failed_count']} 篇文章")
    
    if results['metrics']:
        print(f"\n[总体改进指标]")
        print(f"原总字符数: {results['metrics']['total_old_size']:,}")
        print(f"新总字符数: {results['metrics']['total_new_size']:,}")
        print(f"总体内容增长: {results['metrics']['total_improvement']:+.1f}%")
        print(f"平均文章改进: {results['metrics']['average_improvement']:+.1f}%")
    
    if results['successful']:
        print(f"\n[成功优化的文章]")
        for result in results['successful']:
            print(f"  {result['tool']}: {result['improvement']:+.1f}% 改进 -> {result['file']}")
    
    if results['failed']:
        print(f"\n[优化失败的工具]")
        for tool in results['failed']:
            print(f"  - {tool}")

def create_content_comparison():
    """创建内容对比分析"""
    print(f"\n[分析] 创建内容质量对比")
    
    # 运行内容质量分析器对比新旧内容
    try:
        from content_quality_analyzer import ContentQualityAnalyzer
        analyzer = ContentQualityAnalyzer()
        
        # 分析优化后的内容
        results = analyzer.analyze_content_files()
        
        if results and 'quality_metrics' in results:
            metrics = results['quality_metrics']
            print(f"[新内容质量指标]")
            print(f"  平均字数: {metrics.get('average_word_count', 0):.1f}")
            print(f"  平均SEO得分: {metrics.get('average_seo_score', 0):.1f}%")
            print(f"  平均可读性: {metrics.get('average_readability', 0):.1f}")
            
        return results
        
    except Exception as e:
        print(f"[WARNING] 质量分析失败: {e}")
        return None

def main():
    """主函数"""
    # 执行内容优化
    results = optimize_existing_articles()
    
    if results:
        # 打印优化报告
        print_optimization_report(results)
        
        # 创建质量对比
        comparison = create_content_comparison()
        
        # 保存优化报告
        report_file = f"content_optimization_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        try:
            import json
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'optimization_results': results,
                    'quality_analysis': comparison,
                    'generated_at': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            print(f"\n[SUCCESS] 优化报告已保存: {report_file}")
        except Exception as e:
            print(f"[WARNING] 报告保存失败: {e}")
    
    # 提供下一步建议
    if results and results['metrics']['successful_count'] > 0:
        print(f"\n[下一步建议]")
        print("1. 检查生成的新文章质量和格式")
        print("2. 根据需要调整关键词和内容结构") 
        print("3. 运行Hugo构建测试确保无错误")
        print("4. 考虑逐步替换旧文章或保持两个版本")
        print("5. 监控搜索引擎收录和排名变化")
    
    return results

if __name__ == "__main__":
    main()