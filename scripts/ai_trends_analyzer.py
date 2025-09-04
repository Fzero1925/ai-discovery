#!/usr/bin/env python3
"""
AI工具趋势监控与关键词分析系统
专为变现优化设计，自动发现高收益AI工具机会
"""

import os
import sys
import json
import codecs
import requests
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import argparse

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

@dataclass
class AIToolTrend:
    """AI工具趋势数据结构"""
    keyword: str
    category: str
    search_volume: int
    trend_score: float
    competition_score: float
    commercial_intent: float
    difficulty: str
    affiliate_potential: str
    monthly_revenue_estimate: str
    reason: str
    data_sources: List[str]
    last_updated: str

class AITrendsAnalyzer:
    """AI工具趋势分析器"""
    
    def __init__(self):
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # AI工具分类映射
        self.ai_categories = {
            'content_creation': ['writing', 'content', 'copywriting', 'blog', 'article'],
            'image_generation': ['image', 'art', 'photo', 'design', 'visual', 'picture'],
            'code_assistance': ['code', 'programming', 'developer', 'coding', 'github'],
            'productivity': ['productivity', 'workflow', 'automation', 'task', 'organization'],
            'video_creation': ['video', 'animation', 'editing', 'movie', 'film'],
            'voice_ai': ['voice', 'speech', 'audio', 'sound', 'transcription'],
            'data_analysis': ['data', 'analytics', 'analysis', 'insights', 'dashboard']
        }
        
        # 高收益关键词种子库
        self.seed_keywords = [
            # 内容创作类
            'jasper ai review', 'copy.ai alternatives', 'chatgpt plus worth it', 
            'notion ai features', 'grammarly premium review', 'writesonic pricing',
            # 图像生成类  
            'midjourney alternatives', 'leonardo ai review', 'stable diffusion guide',
            'dall-e 3 review', 'adobe firefly pricing', 'canva ai features',
            # 代码辅助类
            'github copilot review', 'cursor ai pricing', 'tabnine alternatives',
            'codewhisperer vs copilot', 'replit ai review', 'codex openai',
            # 生产力工具类
            'notion ai pricing', 'zapier alternatives', 'monday.com ai',
            'asana ai features', 'trello ai review', 'clickup ai',
            # 新兴AI工具
            'claude ai review', 'perplexity ai pricing', 'character ai alternatives',
            'runway ml review', 'luma ai pricing', 'synthesia alternatives'
        ]

    def analyze_trending_ai_tools(self, limit: int = 10) -> List[AIToolTrend]:
        """分析当前趋势AI工具"""
        print("🔍 开始分析AI工具市场趋势...")
        
        trending_tools = []
        
        # 1. 基于种子关键词分析
        for keyword in self.seed_keywords[:limit*2]:  # 获取更多数据用于筛选
            try:
                tool_data = self._analyze_keyword(keyword)
                if tool_data and tool_data.commercial_intent > 0.7:  # 只保留高商业价值
                    trending_tools.append(tool_data)
                    print(f"✅ 分析完成: {keyword} (商业价值: {tool_data.commercial_intent:.2f})")
                else:
                    print(f"⚠️ 跳过低价值关键词: {keyword}")
                
                # 避免API限流
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ 分析失败 {keyword}: {e}")
                continue
        
        # 2. 按商业价值排序
        trending_tools.sort(key=lambda x: (x.commercial_intent * x.trend_score), reverse=True)
        
        # 3. 返回最有价值的工具
        top_tools = trending_tools[:limit]
        
        print(f"📊 发现 {len(top_tools)} 个高价值AI工具机会")
        return top_tools

    def _analyze_keyword(self, keyword: str) -> Optional[AIToolTrend]:
        """分析单个关键词"""
        try:
            # 1. 确定分类
            category = self._categorize_keyword(keyword)
            
            # 2. 模拟搜索量分析（实际部署中会使用真实API）
            search_data = self._get_search_volume(keyword)
            
            # 3. 竞争分析
            competition_data = self._analyze_competition(keyword)
            
            # 4. 商业价值评估
            commercial_analysis = self._assess_commercial_value(keyword, category)
            
            # 5. 联盟营销潜力
            affiliate_potential = self._assess_affiliate_potential(keyword, category)
            
            # 6. 收益预测
            revenue_estimate = self._estimate_monthly_revenue(
                search_data['volume'], 
                commercial_analysis['intent'], 
                affiliate_potential
            )
            
            return AIToolTrend(
                keyword=keyword,
                category=category,
                search_volume=search_data['volume'],
                trend_score=search_data['trend'],
                competition_score=competition_data['score'],
                commercial_intent=commercial_analysis['intent'],
                difficulty=competition_data['difficulty'],
                affiliate_potential=affiliate_potential,
                monthly_revenue_estimate=revenue_estimate,
                reason=commercial_analysis['reason'],
                data_sources=['internal_analysis', 'market_research'],
                last_updated=datetime.now().isoformat()
            )
            
        except Exception as e:
            print(f"❌ 关键词分析错误 {keyword}: {e}")
            return None

    def _categorize_keyword(self, keyword: str) -> str:
        """AI工具分类识别"""
        keyword_lower = keyword.lower()
        
        for category, terms in self.ai_categories.items():
            if any(term in keyword_lower for term in terms):
                return category
        
        # 特殊规则识别
        if any(term in keyword_lower for term in ['ai', 'artificial intelligence', 'machine learning']):
            if any(term in keyword_lower for term in ['write', 'content', 'blog', 'copy']):
                return 'content_creation'
            elif any(term in keyword_lower for term in ['image', 'picture', 'art', 'design']):
                return 'image_generation'
            elif any(term in keyword_lower for term in ['code', 'program', 'develop']):
                return 'code_assistance'
        
        return 'ai_tools'  # 默认分类

    def _get_search_volume(self, keyword: str) -> Dict:
        """获取搜索量数据（模拟实现）"""
        # 实际部署中会调用Google Keyword Planner API或SEMrush API
        
        # 基于关键词特征的智能估算
        base_volume = 5000
        
        # 品牌词通常搜索量更高
        if any(brand in keyword.lower() for brand in ['chatgpt', 'midjourney', 'notion', 'github']):
            base_volume *= 3
            
        # "review" 和 "alternatives" 关键词搜索量较高
        if 'review' in keyword.lower():
            base_volume *= 2
        if 'alternatives' in keyword.lower():
            base_volume *= 1.8
            
        # "pricing" 关键词表明购买意图
        if 'pricing' in keyword.lower() or 'price' in keyword.lower():
            base_volume *= 1.5
            
        # 计算趋势分数（基于关键词特征）
        trend_score = 0.75  # 基础趋势分数
        
        if any(term in keyword.lower() for term in ['2025', 'new', 'latest', 'best']):
            trend_score += 0.15
            
        if any(term in keyword.lower() for term in ['ai', 'artificial intelligence']):
            trend_score += 0.10  # AI工具整体趋势向上
            
        return {
            'volume': min(base_volume, 50000),  # 限制最大值
            'trend': min(trend_score, 1.0)
        }

    def _analyze_competition(self, keyword: str) -> Dict:
        """竞争分析"""
        # 基于关键词特征的竞争度分析
        competition_score = 0.5  # 基础竞争度
        
        # 品牌词竞争度通常更高
        brand_terms = ['chatgpt', 'midjourney', 'notion', 'github', 'openai', 'google']
        if any(brand in keyword.lower() for brand in brand_terms):
            competition_score += 0.2
            
        # "best" 和 "top" 关键词竞争激烈
        if any(term in keyword.lower() for term in ['best', 'top', 'compare']):
            competition_score += 0.15
            
        # "review" 竞争度中等
        if 'review' in keyword.lower():
            competition_score += 0.05
            
        # "alternatives" 竞争度相对较低
        if 'alternatives' in keyword.lower():
            competition_score -= 0.1
            
        competition_score = max(0.1, min(competition_score, 0.9))
        
        # 确定难度等级
        if competition_score < 0.4:
            difficulty = "Low"
        elif competition_score < 0.7:
            difficulty = "Medium"  
        else:
            difficulty = "High"
            
        return {
            'score': competition_score,
            'difficulty': difficulty
        }

    def _assess_commercial_value(self, keyword: str, category: str) -> Dict:
        """商业价值评估"""
        commercial_intent = 0.6  # 基础商业意图
        
        # 高商业意图关键词
        high_intent_terms = ['review', 'pricing', 'cost', 'buy', 'purchase', 'worth it', 'alternatives', 'vs', 'compare']
        intent_boost = sum(0.1 for term in high_intent_terms if term in keyword.lower())
        commercial_intent += intent_boost
        
        # 分类调整
        category_multipliers = {
            'content_creation': 0.95,  # 内容创作工具转化率高
            'code_assistance': 0.90,   # 开发工具B端付费意愿强
            'image_generation': 0.92,  # 设计工具需求旺盛
            'productivity': 0.88,      # 生产力工具市场成熟
            'video_creation': 0.85,    # 视频工具专业性强
            'voice_ai': 0.80,         # 语音AI市场新兴
            'data_analysis': 0.87      # 数据分析B端需求
        }
        
        commercial_intent *= category_multipliers.get(category, 0.75)
        commercial_intent = min(commercial_intent, 1.0)
        
        # 生成推荐理由
        reasons = []
        if 'review' in keyword.lower():
            reasons.append("评测类内容转化率高")
        if 'alternatives' in keyword.lower():
            reasons.append("用户寻找替代方案，购买意图明确")
        if 'pricing' in keyword.lower():
            reasons.append("价格相关搜索表明强烈购买意图")
        if commercial_intent > 0.85:
            reasons.append("AI工具市场快速增长")
            
        reason = " | ".join(reasons) if reasons else f"{category.replace('_', ' ').title()}市场需求旺盛"
        
        return {
            'intent': commercial_intent,
            'reason': reason
        }

    def _assess_affiliate_potential(self, keyword: str, category: str) -> str:
        """联盟营销潜力评估"""
        
        # 基于工具类型的联盟营销机会
        high_affiliate_categories = ['content_creation', 'image_generation', 'productivity']
        medium_affiliate_categories = ['code_assistance', 'video_creation', 'data_analysis']
        
        # 知名工具通常有联盟计划
        known_tools = ['jasper', 'copy.ai', 'notion', 'grammarly', 'canva', 'zapier']
        has_known_tool = any(tool in keyword.lower() for tool in known_tools)
        
        if category in high_affiliate_categories and has_known_tool:
            return "Very High"
        elif category in high_affiliate_categories or has_known_tool:
            return "High"
        elif category in medium_affiliate_categories:
            return "Medium"
        else:
            return "Low"

    def _estimate_monthly_revenue(self, search_volume: int, commercial_intent: float, affiliate_potential: str) -> str:
        """月收益预估"""
        
        # 基础收益计算
        base_revenue = (search_volume / 1000) * commercial_intent * 10
        
        # 联盟营销潜力调整
        affiliate_multipliers = {
            "Very High": 3.0,
            "High": 2.0,
            "Medium": 1.2,
            "Low": 0.8
        }
        
        base_revenue *= affiliate_multipliers.get(affiliate_potential, 1.0)
        
        # 计算收益区间
        min_revenue = int(base_revenue * 0.6)
        max_revenue = int(base_revenue * 1.8)
        
        # 确保合理范围
        min_revenue = max(min_revenue, 10)
        max_revenue = min(max_revenue, 500)
        
        return f"${min_revenue}-{max_revenue}"

    def save_trending_data(self, trends: List[AIToolTrend], filename: str = "data/trending_ai_tools_cache.json"):
        """保存趋势数据"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # 转换为可序列化格式
        trends_data = []
        for trend in trends:
            trends_data.append({
                'keyword': trend.keyword,
                'category': trend.category,
                'search_volume': trend.search_volume,
                'trend_score': trend.trend_score,
                'competition_score': trend.competition_score,
                'commercial_intent': trend.commercial_intent,
                'difficulty': trend.difficulty,
                'affiliate_potential': trend.affiliate_potential,
                'monthly_revenue_estimate': trend.monthly_revenue_estimate,
                'reason': trend.reason,
                'data_sources': trend.data_sources,
                'last_updated': trend.last_updated
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(trends_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 已保存 {len(trends_data)} 个AI工具趋势到 {filename}")

    def generate_market_report(self, trends: List[AIToolTrend]) -> str:
        """生成市场分析报告"""
        if not trends:
            return "暂无趋势数据"
        
        # 统计分析
        total_tools = len(trends)
        high_value_tools = len([t for t in trends if t.commercial_intent > 0.8])
        avg_search_volume = sum(t.search_volume for t in trends) // total_tools
        
        # 分类统计
        category_stats = {}
        for trend in trends:
            cat = trend.category
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'avg_revenue': 0}
            category_stats[cat]['count'] += 1
        
        # 生成报告
        report = f"""
📊 AI工具市场趋势分析报告
时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

🎯 核心指标:
• 分析工具总数: {total_tools}个
• 高价值工具: {high_value_tools}个 ({high_value_tools/total_tools*100:.1f}%)
• 平均搜索量: {avg_search_volume:,}/月
• 预估总收益潜力: ${sum(int(t.monthly_revenue_estimate.replace('$', '').split('-')[1]) for t in trends if '-' in t.monthly_revenue_estimate)}+/月

📈 分类分布:
""" + "\n".join([f"• {cat.replace('_', ' ').title()}: {stats['count']}个工具" 
                for cat, stats in category_stats.items()]) + f"""

💎 顶级机会:
""" + "\n".join([f"• {trend.keyword} | 收益预估: {trend.monthly_revenue_estimate} | 联盟潜力: {trend.affiliate_potential}"
                for trend in trends[:3]]) + """

🚀 建议行动:
1. 优先制作前3个工具的详细评测
2. 重点关注high_value_tools个高商业价值工具
3. 建立长期跟踪和更新机制
"""
        
        return report

def main():
    parser = argparse.ArgumentParser(description='AI工具趋势分析系统')
    parser.add_argument('--limit', type=int, default=10, help='分析工具数量限制')
    parser.add_argument('--save', action='store_true', help='保存分析结果')
    parser.add_argument('--report', action='store_true', help='生成市场报告')
    parser.add_argument('--category', help='指定分析的工具分类')
    
    args = parser.parse_args()
    
    print("🚀 启动AI工具趋势分析系统...")
    print(f"🎯 目标: 发现 {args.limit} 个高收益AI工具机会")
    
    analyzer = AITrendsAnalyzer()
    
    try:
        # 执行趋势分析
        trending_tools = analyzer.analyze_trending_ai_tools(limit=args.limit)
        
        if not trending_tools:
            print("❌ 未发现任何趋势数据")
            return False
        
        # 保存结果
        if args.save:
            analyzer.save_trending_data(trending_tools)
        
        # 生成报告
        if args.report:
            report = analyzer.generate_market_report(trending_tools)
            print("\n" + "="*60)
            print(report)
            print("="*60)
            
            # 保存报告
            report_file = f"data/market_report_{datetime.now().strftime('%Y%m%d')}.txt"
            os.makedirs(os.path.dirname(report_file), exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 市场报告已保存: {report_file}")
        
        # 显示结果摘要
        print(f"\n✅ 分析完成! 发现 {len(trending_tools)} 个高价值AI工具机会")
        print("\n🏆 Top 3 推荐:")
        for i, tool in enumerate(trending_tools[:3], 1):
            print(f"{i}. {tool.keyword}")
            print(f"   收益预估: {tool.monthly_revenue_estimate}/月")
            print(f"   商业价值: {tool.commercial_intent:.2f}")
            print(f"   联盟潜力: {tool.affiliate_potential}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ 系统错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)