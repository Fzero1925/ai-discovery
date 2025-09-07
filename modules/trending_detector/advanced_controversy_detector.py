#!/usr/bin/env python3
"""
Advanced Controversy Detection System
多维度智能争议话题检测系统 - 专为AI工具热点事件设计
"""

import json
import os
import re
import math
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from collections import Counter
import requests
from pathlib import Path

@dataclass
class ControversySignal:
    """争议信号数据结构"""
    keyword: str
    source: str
    intensity: float  # 争议强度 0-100
    sentiment_score: float  # 情感分数 -1到1
    time_decay_factor: float  # 时间衰减因子
    context_relevance: float  # 语境相关性
    social_amplification: float  # 社交放大效应
    timestamp: str

@dataclass 
class ControversyAnalysis:
    """争议分析结果"""
    topic: str
    overall_score: float  # 综合争议分数
    confidence: float  # 置信度
    category: str  # 争议类型
    signals: List[ControversySignal]
    risk_level: str  # 风险等级
    recommended_action: str  # 推荐行动
    trend_prediction: str  # 趋势预测

class AdvancedControversyDetector:
    """
    高级争议检测器
    集成多维度分析、时间权重、语境理解和社交验证
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 多层级争议词库
        self.controversy_lexicon = self._build_advanced_lexicon()
        
        # 情感强度映射
        self.sentiment_weights = self._build_sentiment_weights()
        
        # 时间衰减参数
        self.time_decay_hours = {
            'critical': 6,    # 严重争议6小时内权重最高
            'major': 24,      # 重大争议24小时内保持高权重
            'minor': 72       # 轻微争议72小时内有效
        }
        
        # 社交验证阈值
        self.social_validation_threshold = 2  # 至少2个数据源确认
        
    def _build_advanced_lexicon(self) -> Dict[str, Dict[str, float]]:
        """构建高级争议词库，包含权重和语境信息"""
        return {
            'ai_specific_issues': {
                # AI特定问题词汇
                '降智': 25.0, 'intelligence_drop': 25.0, '智商下降': 25.0,
                '模型退化': 20.0, 'model_degradation': 20.0, 'performance_decline': 20.0,
                '响应变慢': 15.0, 'slow_response': 15.0, '延迟增加': 15.0,
                '准确率下降': 18.0, 'accuracy_drop': 18.0, 'quality_decline': 18.0,
                '服务中断': 22.0, 'service_outage': 22.0, 'downtime': 22.0,
                '数据泄露': 30.0, 'data_breach': 30.0, 'privacy_leak': 30.0,
                '算法偏见': 20.0, 'algorithm_bias': 20.0, 'unfair_results': 20.0,
                '版权争议': 25.0, 'copyright_dispute': 25.0, 'legal_issues': 25.0,
            },
            
            'intensity_amplifiers': {
                # 强度放大词
                '严重': 2.0, 'severe': 2.0, 'seriously': 2.0,
                '大量': 1.8, 'massive': 1.8, 'widespread': 1.8,
                '频繁': 1.6, 'frequent': 1.6, 'repeatedly': 1.6,
                '突然': 1.5, 'suddenly': 1.5, 'abruptly': 1.5,
                '完全': 2.2, 'completely': 2.2, 'totally': 2.2,
            },
            
            'emotional_intensifiers': {
                # 情感强化词
                '愤怒': 20.0, 'angry': 20.0, 'furious': 25.0,
                '失望': 15.0, 'disappointed': 15.0, 'let_down': 15.0,
                '质疑': 12.0, 'question': 12.0, 'doubt': 12.0,
                '抗议': 18.0, 'protest': 18.0, 'oppose': 18.0,
                '抵制': 22.0, 'boycott': 22.0, 'resist': 18.0,
                '投诉': 16.0, 'complain': 16.0, 'report_issue': 16.0,
            },
            
            'social_media_markers': {
                # 网络热词和俚语
                '翻车': 25.0, 'epic_fail': 25.0, 'disaster': 25.0,
                '拉胯': 20.0, 'sucks': 20.0, 'terrible': 20.0,
                '割韭菜': 28.0, 'scam': 28.0, 'rip_off': 25.0,
                '智商税': 22.0, 'waste_of_money': 18.0, 'overpriced': 15.0,
                '坑': 18.0, 'trap': 18.0, 'misleading': 16.0,
                '黑心': 24.0, 'unethical': 20.0, 'dishonest': 18.0,
            },
            
            'urgency_indicators': {
                # 紧急性指标
                '紧急': 2.5, 'urgent': 2.5, 'critical': 2.8,
                '立即': 2.2, 'immediately': 2.2, 'asap': 2.0,
                '警告': 2.3, 'warning': 2.3, 'alert': 2.1,
                '危险': 2.6, 'dangerous': 2.6, 'risky': 2.2,
            },
            
            'temporal_markers': {
                # 时间相关标记
                '最近': 1.8, 'recently': 1.8, 'lately': 1.6,
                '今天': 2.0, 'today': 2.0, 'right_now': 2.2,
                '刚刚': 2.5, 'just_now': 2.5, 'moments_ago': 2.3,
                '突破性': 1.5, 'breaking': 2.8, 'developing': 2.0,
            }
        }
    
    def _build_sentiment_weights(self) -> Dict[str, float]:
        """构建情感权重映射"""
        return {
            'extremely_negative': -0.9,  # 极度负面
            'very_negative': -0.7,       # 非常负面
            'negative': -0.5,            # 负面
            'slightly_negative': -0.3,   # 轻微负面
            'neutral': 0.0,              # 中性
            'slightly_positive': 0.3,    # 轻微正面
            'positive': 0.5,             # 正面
            'very_positive': 0.7,        # 非常正面
            'extremely_positive': 0.9    # 极度正面
        }
    
    def analyze_controversy(self, text: str, source: str, timestamp: Optional[str] = None) -> ControversySignal:
        """分析单个文本的争议性"""
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        # 1. 基础争议分数计算
        base_score = self._calculate_base_controversy_score(text)
        
        # 2. 情感分析
        sentiment_score = self._analyze_sentiment_intensity(text)
        
        # 3. 时间衰减因子
        time_decay = self._calculate_time_decay(timestamp)
        
        # 4. 语境相关性
        context_relevance = self._assess_context_relevance(text, source)
        
        # 5. 社交放大效应
        social_amplification = self._estimate_social_amplification(text, source)
        
        # 6. 综合强度计算
        intensity = self._calculate_comprehensive_intensity(
            base_score, sentiment_score, time_decay, 
            context_relevance, social_amplification
        )
        
        # 提取主要关键词
        main_keyword = self._extract_primary_keyword(text)
        
        return ControversySignal(
            keyword=main_keyword,
            source=source,
            intensity=intensity,
            sentiment_score=sentiment_score,
            time_decay_factor=time_decay,
            context_relevance=context_relevance,
            social_amplification=social_amplification,
            timestamp=timestamp
        )
    
    def _calculate_base_controversy_score(self, text: str) -> float:
        """计算基础争议分数，使用加权词汇匹配"""
        text_lower = text.lower()
        total_score = 0.0
        matched_terms = 0
        
        for category, terms in self.controversy_lexicon.items():
            for term, weight in terms.items():
                if category == 'intensity_amplifiers' or category == 'urgency_indicators' or category == 'temporal_markers':
                    continue  # 这些词汇用于修饰，不单独计分
                    
                count = len(re.findall(r'\b' + re.escape(term.replace('_', r'\s*')) + r'\b', text_lower))
                if count > 0:
                    # 应用强度放大器效果
                    amplifier = self._find_intensity_amplifier(text_lower, term)
                    score_contribution = weight * count * amplifier
                    total_score += score_contribution
                    matched_terms += count
        
        # 标准化分数 (0-100)
        if matched_terms == 0:
            return 0.0
        
        # 使用对数函数防止分数过高
        normalized_score = min(100.0, 30 * math.log(1 + total_score / 10))
        return normalized_score
    
    def _find_intensity_amplifier(self, text: str, base_term: str) -> float:
        """寻找强度放大器词汇"""
        amplifier = 1.0
        
        # 在base_term前后20个字符内寻找放大器
        term_pos = text.find(base_term.replace('_', ' '))
        if term_pos == -1:
            return amplifier
            
        context_start = max(0, term_pos - 50)
        context_end = min(len(text), term_pos + len(base_term) + 50)
        context = text[context_start:context_end]
        
        for category in ['intensity_amplifiers', 'urgency_indicators', 'temporal_markers']:
            for amp_term, amp_weight in self.controversy_lexicon[category].items():
                if amp_term.replace('_', ' ') in context:
                    amplifier = max(amplifier, amp_weight)
        
        return amplifier
    
    def _analyze_sentiment_intensity(self, text: str) -> float:
        """分析情感强度，返回-1到1的分数"""
        negative_indicators = [
            'terrible', 'awful', 'horrible', 'disgusting', 'hate', 'angry',
            '糟糕', '可怕', '讨厌', '愤怒', '失望', '不满'
        ]
        
        positive_indicators = [
            'great', 'amazing', 'excellent', 'wonderful', 'love', 'perfect',
            '很好', '棒', '优秀', '完美', '喜欢', '满意'
        ]
        
        text_lower = text.lower()
        negative_count = sum(1 for indicator in negative_indicators if indicator in text_lower)
        positive_count = sum(1 for indicator in positive_indicators if indicator in text_lower)
        
        # 计算情感分数
        if negative_count + positive_count == 0:
            return 0.0
        
        sentiment_score = (positive_count - negative_count) / (positive_count + negative_count)
        return sentiment_score
    
    def _calculate_time_decay(self, timestamp: str) -> float:
        """计算时间衰减因子，越近的时间权重越高"""
        try:
            post_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            if post_time.tzinfo is None:
                post_time = post_time.replace(tzinfo=None)
            current_time = datetime.now()
            
            hours_elapsed = (current_time - post_time.replace(tzinfo=None)).total_seconds() / 3600
            
            # 使用指数衰减，24小时内保持高权重
            if hours_elapsed <= 6:
                return 1.0  # 6小时内全权重
            elif hours_elapsed <= 24:
                return 0.8  # 24小时内0.8权重
            elif hours_elapsed <= 72:
                return 0.6 * math.exp(-hours_elapsed / 72)  # 72小时内指数衰减
            else:
                return 0.1  # 72小时后低权重
                
        except:
            return 0.5  # 无法解析时间时给予中等权重
    
    def _assess_context_relevance(self, text: str, source: str) -> float:
        """评估语境相关性，判断争议是否与AI工具相关"""
        ai_context_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'gpt',
            'claude', 'gemini', 'copilot', 'midjourney', 'dall-e',
            '人工智能', 'AI工具', '机器学习', '算法', '模型'
        ]
        
        text_lower = text.lower()
        relevance_score = 0.0
        
        for keyword in ai_context_keywords:
            if keyword in text_lower:
                relevance_score += 0.2
        
        # 根据数据源调整相关性
        source_weights = {
            'reddit_artificial': 1.2,
            'reddit_chatgpt': 1.3,
            'news_api': 1.0,
            'hackernews': 1.1,
            'rss_techcrunch': 1.1
        }
        
        source_weight = source_weights.get(source, 1.0)
        relevance_score *= source_weight
        
        return min(1.0, relevance_score)
    
    def _estimate_social_amplification(self, text: str, source: str) -> float:
        """估算社交放大效应"""
        viral_indicators = [
            'viral', 'trending', 'breaking', 'everyone', 'massive', 
            '火了', '热搜', '刷屏', '疯传', '爆料'
        ]
        
        text_lower = text.lower()
        amplification = 1.0
        
        for indicator in viral_indicators:
            if indicator in text_lower:
                amplification += 0.3
        
        # 社交媒体平台有更高的放大效应
        if 'reddit' in source:
            amplification *= 1.2
        elif 'hackernews' in source:
            amplification *= 1.1
        
        return min(2.0, amplification)
    
    def _calculate_comprehensive_intensity(self, base_score: float, sentiment: float, 
                                         time_decay: float, relevance: float, 
                                         amplification: float) -> float:
        """计算综合争议强度"""
        # 负面情感增强争议，正面情感减弱争议
        sentiment_modifier = 1.0 + (-sentiment * 0.5)  # 负面情感会增加争议强度
        
        # 综合计算
        intensity = base_score * sentiment_modifier * time_decay * relevance * amplification
        
        # 确保在0-100范围内
        return min(100.0, max(0.0, intensity))
    
    def _extract_primary_keyword(self, text: str) -> str:
        """提取主要关键词"""
        ai_tools = [
            'chatgpt', 'claude', 'gpt-4', 'gpt-5', 'gemini', 'perplexity',
            'character.ai', 'midjourney', 'dall-e', 'stable diffusion',
            'github copilot', 'anthropic', 'openai', 'google ai'
        ]
        
        text_lower = text.lower()
        for tool in ai_tools:
            if tool in text_lower:
                return tool.title()
        
        # 如果没找到特定工具，提取最重要的争议词
        for category, terms in self.controversy_lexicon.items():
            if category in ['ai_specific_issues', 'emotional_intensifiers']:
                for term, weight in sorted(terms.items(), key=lambda x: x[1], reverse=True):
                    if term.replace('_', ' ') in text_lower:
                        return term.replace('_', ' ').title()
        
        return "AI工具争议"
    
    def multi_source_controversy_analysis(self, signals: List[ControversySignal]) -> ControversyAnalysis:
        """多源争议分析，提供综合判断"""
        if not signals:
            return self._create_empty_analysis()
        
        # 1. 计算综合分数
        weighted_scores = []
        source_count = Counter(signal.source for signal in signals)
        
        for signal in signals:
            # 多源验证加权
            source_validation_weight = min(2.0, source_count[signal.source] * 0.5)
            weighted_score = signal.intensity * source_validation_weight
            weighted_scores.append(weighted_score)
        
        overall_score = sum(weighted_scores) / len(weighted_scores) if weighted_scores else 0
        
        # 2. 计算置信度
        unique_sources = len(set(signal.source for signal in signals))
        confidence = min(1.0, unique_sources / self.social_validation_threshold)
        
        # 3. 确定争议类别和风险等级
        category, risk_level = self._categorize_controversy(overall_score, signals)
        
        # 4. 生成推荐行动和趋势预测
        recommended_action = self._generate_recommendation(overall_score, risk_level, signals)
        trend_prediction = self._predict_trend(signals)
        
        # 5. 选择代表性主题
        topic = self._extract_representative_topic(signals)
        
        return ControversyAnalysis(
            topic=topic,
            overall_score=overall_score,
            confidence=confidence,
            category=category,
            signals=signals,
            risk_level=risk_level,
            recommended_action=recommended_action,
            trend_prediction=trend_prediction
        )
    
    def _categorize_controversy(self, score: float, signals: List[ControversySignal]) -> Tuple[str, str]:
        """分类争议类型和风险等级"""
        # 分析主要争议类型
        categories = {
            'performance': ['降智', 'performance_decline', '响应变慢', 'slow_response'],
            'reliability': ['服务中断', 'service_outage', 'downtime', '故障'],
            'privacy': ['数据泄露', 'data_breach', 'privacy_leak', '隐私'],
            'ethical': ['算法偏见', 'algorithm_bias', '歧视', 'unfair'],
            'commercial': ['割韭菜', 'scam', '智商税', 'overpriced'],
            'quality': ['质量下降', 'quality_decline', '准确率下降', 'accuracy_drop']
        }
        
        category_scores = {cat: 0 for cat in categories}
        
        for signal in signals:
            for cat, keywords in categories.items():
                if any(keyword in signal.keyword.lower() for keyword in keywords):
                    category_scores[cat] += signal.intensity
        
        primary_category = max(category_scores.items(), key=lambda x: x[1])[0] if any(category_scores.values()) else 'general'
        
        # 确定风险等级
        if score >= 70:
            risk_level = "严重"  # Critical
        elif score >= 50:
            risk_level = "重大"  # Major  
        elif score >= 30:
            risk_level = "中等"  # Moderate
        elif score >= 15:
            risk_level = "轻微"  # Minor
        else:
            risk_level = "极低"  # Minimal
        
        return primary_category, risk_level
    
    def _generate_recommendation(self, score: float, risk_level: str, signals: List[ControversySignal]) -> str:
        """生成推荐行动"""
        if score >= 70:
            return "立即生成热点分析文章，抓住流量红利，提供解决方案和替代建议"
        elif score >= 50:
            return "优先生成深度分析内容，平衡报道争议焦点和客观评估"
        elif score >= 30:
            return "适度关注，可生成相关内容但避免过度渲染争议"
        elif score >= 15:
            return "持续监控，根据发展情况决定是否生成内容"
        else:
            return "暂不生成争议相关内容，关注其他话题"
    
    def _predict_trend(self, signals: List[ControversySignal]) -> str:
        """预测争议发展趋势"""
        if not signals:
            return "无法预测"
        
        # 分析时间趋势
        recent_signals = [s for s in signals if s.time_decay_factor > 0.8]
        older_signals = [s for s in signals if s.time_decay_factor <= 0.8]
        
        if len(recent_signals) > len(older_signals) * 2:
            return "争议热度上升中，建议密切关注"
        elif len(recent_signals) < len(older_signals) * 0.5:
            return "争议热度下降中，可考虑理性分析文章"
        else:
            return "争议热度稳定，适合深度分析"
    
    def _extract_representative_topic(self, signals: List[ControversySignal]) -> str:
        """提取代表性话题"""
        keyword_weights = Counter()
        
        for signal in signals:
            keyword_weights[signal.keyword] += signal.intensity
        
        if keyword_weights:
            return keyword_weights.most_common(1)[0][0]
        else:
            return "AI工具争议话题"
    
    def _create_empty_analysis(self) -> ControversyAnalysis:
        """创建空的分析结果"""
        return ControversyAnalysis(
            topic="无争议检测",
            overall_score=0.0,
            confidence=0.0,
            category="none",
            signals=[],
            risk_level="无",
            recommended_action="正常内容生成",
            trend_prediction="无趋势数据"
        )
    
    def save_analysis_cache(self, analysis: ControversyAnalysis, filename: str = "controversy_analysis_cache.json"):
        """保存争议分析缓存"""
        cache_file = self.data_dir / filename
        
        cache_data = {
            "generated_at": datetime.now().isoformat(),
            "analysis": {
                "topic": analysis.topic,
                "overall_score": analysis.overall_score,
                "confidence": analysis.confidence,
                "category": analysis.category,
                "risk_level": analysis.risk_level,
                "recommended_action": analysis.recommended_action,
                "trend_prediction": analysis.trend_prediction,
                "signals_count": len(analysis.signals),
                "top_signals": [
                    {
                        "keyword": signal.keyword,
                        "source": signal.source,
                        "intensity": signal.intensity,
                        "sentiment_score": signal.sentiment_score
                    }
                    for signal in sorted(analysis.signals, key=lambda x: x.intensity, reverse=True)[:5]
                ]
            }
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 争议分析结果已保存到 {cache_file}")


def main():
    """测试高级争议检测器"""
    detector = AdvancedControversyDetector()
    
    # 测试案例
    test_cases = [
        ("ChatGPT最近严重降智了，回答质量明显下降，很多用户都在抱怨", "reddit_chatgpt", datetime.now().isoformat()),
        ("Claude AI appears to have performance issues lately, users reporting slower responses", "news_api", datetime.now().isoformat()),
        ("OpenAI服务中断导致大量用户无法正常使用", "rss_techcrunch", (datetime.now() - timedelta(hours=2)).isoformat()),
        ("Midjourney涨价被批评是割韭菜行为", "hackernews", (datetime.now() - timedelta(hours=6)).isoformat()),
    ]
    
    print("🔍 高级争议检测测试开始...")
    
    signals = []
    for text, source, timestamp in test_cases:
        signal = detector.analyze_controversy(text, source, timestamp)
        signals.append(signal)
        
        print(f"\n📊 单项分析结果:")
        print(f"  文本: {text[:50]}...")
        print(f"  关键词: {signal.keyword}")
        print(f"  争议强度: {signal.intensity:.1f}")
        print(f"  情感分数: {signal.sentiment_score:.2f}")
        print(f"  时间衰减: {signal.time_decay_factor:.2f}")
        print(f"  语境相关性: {signal.context_relevance:.2f}")
    
    # 多源综合分析
    print(f"\n🧠 多源综合分析结果:")
    analysis = detector.multi_source_controversy_analysis(signals)
    
    print(f"  争议话题: {analysis.topic}")
    print(f"  综合分数: {analysis.overall_score:.1f}/100")
    print(f"  置信度: {analysis.confidence:.1f}")
    print(f"  争议类型: {analysis.category}")
    print(f"  风险等级: {analysis.risk_level}")
    print(f"  推荐行动: {analysis.recommended_action}")
    print(f"  趋势预测: {analysis.trend_prediction}")
    
    # 保存结果
    detector.save_analysis_cache(analysis)
    
    print(f"\n✅ 高级争议检测测试完成")

if __name__ == "__main__":
    main()