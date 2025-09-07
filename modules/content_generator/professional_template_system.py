#!/usr/bin/env python3
"""
Professional First-Person Content Template System
第一人称专业化内容模板系统 - 支持争议话题和SEO优化
"""

import json
import random
import re
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ProfessionalProfile:
    """专业身份配置"""
    title: str  # AI工具分析师、数字营销专家等
    experience_years: int  # 从业年限
    specialization: List[str]  # 专业领域
    credentials: List[str]  # 资质认证
    voice_style: str  # 语言风格：professional, approachable, expert

@dataclass
class ContentContext:
    """内容上下文"""
    tool_name: str
    category: str
    is_controversial: bool
    controversy_level: str  # low, medium, high, critical
    target_keywords: List[str]
    user_intent: str  # research, comparison, purchase, troubleshooting
    content_angle: str  # neutral_analysis, problem_solving, comparison, recommendation

class ProfessionalTemplateSystem:
    """
    专业化第一人称模板系统
    支持多种专业身份、争议话题处理和SEO优化
    """
    
    def __init__(self, profile: Optional[ProfessionalProfile] = None):
        self.profile = profile or self._create_default_profile()
        self.templates = self._load_professional_templates()
        self.seo_patterns = self._load_seo_patterns()
        self.controversy_handlers = self._load_controversy_handlers()
        
    def _create_default_profile(self) -> ProfessionalProfile:
        """创建默认专业身份"""
        return ProfessionalProfile(
            title="AI工具分析师",
            experience_years=5,
            specialization=["人工智能工具评估", "企业数字化转型", "生产力优化"],
            credentials=["数字营销认证", "AI产品分析专家"],
            voice_style="professional"
        )
    
    def _load_professional_templates(self) -> Dict[str, Dict]:
        """加载专业化模板库"""
        return {
            "introduction_patterns": {
                "neutral_analysis": [
                    "作为一名从业{years}年的{title}，我在过去几个月中深入测试了{tool_name}，以下是我的专业分析。",
                    "基于我在{specialization}领域的实际经验，我对{tool_name}进行了全面的专业评估。",
                    "从我的{title}视角来看，{tool_name}在{category}领域的表现值得仔细分析。",
                    "作为专注于{specialization}的专业人士，我花了数周时间测试{tool_name}的各项功能。"
                ],
                "problem_solving": [
                    "近期我收到多位客户关于{tool_name}问题的咨询，作为{title}，我认为有必要提供专业的解决方案分析。",
                    "基于我处理过的数百个{category}工具案例，{tool_name}的当前状况需要专业的解读。",
                    "从我的专业经验来看，{tool_name}最近遇到的问题反映了{category}行业的一些典型挑战。"
                ],
                "comparison": [
                    "在我的{specialization}实践中，经常需要为客户选择最适合的{category}工具。今天我将专业对比{tool_name}与其主要竞品。",
                    "基于我在{years}年专业经验中测试过的数十款{category}工具，以下是{tool_name}的客观分析。"
                ]
            },
            
            "expertise_markers": {
                "experience_based": [
                    "在我{years}年的专业实践中",
                    "基于我处理过的{number}+个类似案例",
                    "从我的实际项目经验来看",
                    "根据我在{specialization}领域的深度研究",
                    "结合我为{number}+企业提供咨询的经验"
                ],
                "professional_judgment": [
                    "从专业角度分析",
                    "基于行业最佳实践",
                    "从技术实现角度评估",
                    "考虑到企业级应用需求",
                    "结合市场趋势和用户反馈"
                ],
                "credibility_indicators": [
                    "我的{credentials}认证经验表明",
                    "在我参与的{number}个项目中",
                    "通过与行业专家的深度交流",
                    "基于我的专业评估框架"
                ]
            },
            
            "personal_insights": {
                "testing_experience": [
                    "在我的实际测试中发现",
                    "通过我的深度使用体验",
                    "从我连续{days}天的测试结果看",
                    "我在实际项目中应用{tool_name}时注意到",
                    "基于我与{number}位用户的访谈"
                ],
                "professional_observations": [
                    "我观察到的一个关键趋势是",
                    "从我的专业观察来看",
                    "我注意到一个重要的模式",
                    "基于我的行业洞察",
                    "我发现了一个有趣的现象"
                ],
                "recommendations": [
                    "基于我的专业建议",
                    "我强烈推荐的做法是",
                    "从我的实践经验来看，最佳策略是",
                    "我的专业建议是",
                    "考虑到实际应用场景，我建议"
                ]
            },
            
            "conclusion_patterns": {
                "balanced_assessment": [
                    "综合我的专业评估，{tool_name}在{category}领域{assessment}。",
                    "基于我的{years}年专业经验，我认为{tool_name}{conclusion}。",
                    "从我的专业角度看，{tool_name}适合{target_users}，但需要注意{considerations}。"
                ],
                "professional_recommendation": [
                    "作为{title}，我的专业建议是：{recommendation}。",
                    "基于我的实践经验，我建议{advice}。",
                    "从投资回报角度分析，{tool_name}{roi_assessment}。"
                ]
            }
        }
    
    def _load_seo_patterns(self) -> Dict[str, List]:
        """加载SEO优化模式"""
        return {
            "question_based_headings": [
                "{tool_name}真的值得投资吗？我的专业分析",
                "为什么{tool_name}在{category}领域备受争议？",
                "{tool_name} vs 竞品：哪个更适合企业用户？",
                "如何正确使用{tool_name}？专家指南",
                "{tool_name}的隐藏成本：你需要知道的真相",
                "2025年{tool_name}还值得选择吗？"
            ],
            "long_tail_keywords": [
                "{tool_name} 专业评测",
                "{tool_name} 企业级应用",
                "{tool_name} 最佳替代方案",
                "{tool_name} 成本效益分析",
                "{tool_name} 实际使用体验",
                "{tool_name} 专家推荐指数"
            ],
            "user_intent_phrases": [
                "寻找{tool_name}替代方案的用户",
                "考虑投资{category}工具的企业",
                "希望提升{use_case}效率的专业人士",
                "对{tool_name}效果存疑的用户"
            ],
            "semantic_clusters": [
                ["功能特性", "核心优势", "技术亮点", "实用功能"],
                ["使用场景", "应用领域", "适用人群", "业务价值"],
                ["成本分析", "投资回报", "价格对比", "性价比评估"],
                ["问题解决", "使用技巧", "最佳实践", "专家建议"]
            ]
        }
    
    def _load_controversy_handlers(self) -> Dict[str, Dict]:
        """加载争议话题处理模板"""
        return {
            "controversy_acknowledgment": {
                "low": [
                    "我注意到最近一些用户对{tool_name}提出了质疑，作为专业分析师，我认为有必要客观分析这些问题。",
                    "虽然{tool_name}最近面临一些争议，但基于我的专业评估，情况比表面看起来更复杂。"
                ],
                "medium": [
                    "作为{title}，我必须诚实地说，{tool_name}最近确实遇到了一些值得关注的问题。",
                    "基于我的专业观察，{tool_name}当前的争议反映了{category}行业面临的更深层次挑战。",
                    "从我的实际测试来看，关于{tool_name}的争议既有合理之处，也存在一些误解。"
                ],
                "high": [
                    "作为一名负责任的{title}，我不能忽视{tool_name}最近引发的重大争议。",
                    "基于我的专业判断，{tool_name}当前面临的问题需要用户认真考虑。",
                    "从行业专家的角度看，{tool_name}的争议性问题确实值得深度分析。"
                ]
            },
            
            "balanced_analysis": {
                "acknowledge_concerns": [
                    "用户的担忧确实有其合理性",
                    "这些问题不应该被忽视",
                    "从用户体验角度看，这些反馈很有价值",
                    "专业的态度是正视这些挑战"
                ],
                "provide_context": [
                    "但我们需要将这些问题放在更大的背景下理解",
                    "从技术发展的角度来看",
                    "考虑到{category}行业的整体发展趋势",
                    "基于我对类似工具的长期观察"
                ],
                "professional_perspective": [
                    "从我的专业经验来看",
                    "基于我的技术分析",
                    "结合行业发展规律",
                    "从投资回报角度考虑"
                ]
            },
            
            "solution_oriented": {
                "immediate_actions": [
                    "针对当前问题，我建议用户采取以下措施",
                    "基于我的专业建议，可以通过以下方式缓解问题",
                    "从实用角度出发，以下策略可能有帮助"
                ],
                "alternative_solutions": [
                    "如果{tool_name}无法满足需求，我推荐以下替代方案",
                    "基于我的评估，以下工具可能更适合当前情况",
                    "从风险管控角度，建议考虑这些备选方案"
                ],
                "long_term_outlook": [
                    "从长期发展看，我对{tool_name}的前景{outlook}",
                    "基于行业趋势分析，{prediction}",
                    "从专业投资角度考虑，{recommendation}"
                ]
            }
        }
    
    def generate_professional_content(self, context: ContentContext) -> Dict[str, str]:
        """生成专业化第一人称内容"""
        content_sections = {}
        
        # 1. 专业介绍段落
        content_sections["introduction"] = self._generate_professional_introduction(context)
        
        # 2. 专业分析框架
        content_sections["analysis_framework"] = self._generate_analysis_framework(context)
        
        # 3. 实际测试体验
        content_sections["testing_experience"] = self._generate_testing_experience(context)
        
        # 4. 专业评估
        content_sections["professional_assessment"] = self._generate_professional_assessment(context)
        
        # 5. 争议话题处理（如果适用）
        if context.is_controversial:
            content_sections["controversy_analysis"] = self._generate_controversy_analysis(context)
        
        # 6. 使用建议和最佳实践
        content_sections["recommendations"] = self._generate_professional_recommendations(context)
        
        # 7. 专业结论
        content_sections["conclusion"] = self._generate_professional_conclusion(context)
        
        return content_sections
    
    def _generate_professional_introduction(self, context: ContentContext) -> str:
        """生成专业介绍"""
        profile = self.profile
        
        # 选择适合的介绍模式
        intro_patterns = self.templates["introduction_patterns"][context.content_angle]
        base_intro = random.choice(intro_patterns)
        
        # 填充专业身份信息
        intro = base_intro.format(
            title=profile.title,
            years=profile.experience_years,
            tool_name=context.tool_name,
            category=context.category,
            specialization=random.choice(profile.specialization)
        )
        
        # 添加专业资质说明
        if profile.credentials:
            credential = random.choice(profile.credentials)
            intro += f" 基于我的{credential}和实际项目经验，这篇分析将为你提供专业且实用的见解。"
        
        # 添加内容预告
        preview_elements = [
            "详细的功能测试结果",
            "实际应用场景分析",
            "与竞品的专业对比",
            "投资回报评估",
            "实用的使用建议"
        ]
        
        preview = "、".join(random.sample(preview_elements, 3))
        intro += f"\n\n在这篇深度分析中，我将分享{preview}，帮助你做出明智的决策。"
        
        return intro
    
    def _generate_analysis_framework(self, context: ContentContext) -> str:
        """生成分析框架说明"""
        framework = f"""## 我的专业评估框架

作为{self.profile.title}，我使用以下标准化框架来评估{context.category}工具：

### 核心评估维度

**功能完整性** (权重30%)
- 核心功能实现质量
- 功能覆盖范围
- 创新特性评估

**用户体验** (权重25%)
- 界面设计合理性  
- 学习曲线陡峭程度
- 工作流程效率

**技术稳定性** (权重20%)
- 系统可靠性
- 响应速度表现
- 数据安全保障

**商业价值** (权重15%)
- 投资回报分析
- 成本效益比较
- 长期价值评估

**生态集成** (权重10%)
- 第三方工具兼容性
- API开放程度
- 企业级功能支持

> 💡 **专业提示**: 这套评估体系是我在{self.profile.experience_years}年专业实践中不断完善的，已成功应用于200+款工具的评估。"""

        return framework
    
    def _generate_testing_experience(self, context: ContentContext) -> str:
        """生成测试体验内容"""
        testing_scenarios = [
            f"在我为一家中型企业进行{context.category}工具选型时",
            f"我连续30天将{context.tool_name}应用于实际项目中",
            f"通过与{random.randint(15, 25)}位不同行业用户的深度访谈",
            f"我在{random.randint(3, 5)}个不同规模的项目中测试了{context.tool_name}"
        ]
        
        testing_intro = random.choice(testing_scenarios)
        
        testing_content = f"""## 实际测试体验分析

### 我的测试方法

{testing_intro}，发现了一些值得分享的关键洞察。

我的测试覆盖了以下场景：
- **小团队协作** (2-5人团队的使用体验)
- **中型项目管理** (涉及10-20个利益相关者)
- **企业级部署** (100+用户的规模化应用)
- **跨部门集成** (与现有工具链的兼容性)

### 核心发现

通过我的专业测试，我发现{context.tool_name}在以下方面表现{random.choice(['突出', '良好', '有待改进'])}：

"""
        
        # 添加具体测试发现
        findings = [
            f"**响应时间**: 在我的测试中，平均响应时间为{random.uniform(0.5, 3.0):.1f}秒",
            f"**准确率**: 基于我的{random.randint(100, 500)}次测试，准确率达到{random.randint(85, 98)}%",
            f"**稳定性**: 在{random.randint(7, 30)}天的连续使用中，遇到{random.randint(0, 3)}次系统问题",
            f"**学习成本**: 新用户完全掌握需要{random.randint(1, 7)}天时间"
        ]
        
        testing_content += "\n".join(f"- {finding}" for finding in random.sample(findings, 3))
        
        return testing_content
    
    def _generate_professional_assessment(self, context: ContentContext) -> str:
        """生成专业评估内容"""
        assessment = f"""## 专业深度评估

### 技术架构分析

从我的{self.profile.title}视角来看，{context.tool_name}的技术实现{random.choice(['具有前瞻性', '相对成熟', '仍需优化'])}。

**核心优势识别**：
"""
        
        # 添加专业优势分析
        advantages = [
            "算法优化程度高，处理效率显著",
            "用户界面设计符合企业级应用标准",
            "数据处理能力在同类产品中处于领先地位",
            "系统集成能力强，适应性好",
            "安全机制完善，符合企业合规要求"
        ]
        
        for i, advantage in enumerate(random.sample(advantages, 3), 1):
            assessment += f"\n{i}. **{advantage}**: 基于我的实际测试和行业对比分析。"
        
        assessment += f"""

### 应用场景适配度

根据我在{random.choice(self.profile.specialization)}领域的经验，{context.tool_name}最适合以下场景：

- **{random.choice(['初创团队', '中小企业', '大型企业', '个人用户'])}**: 特别是需要{random.choice(['快速迭代', '成本控制', '规模化应用', '简单易用'])}的情况
- **{random.choice(['项目管理', '内容创作', '数据分析', '客户服务'])}**: 在我的测试中，这个场景下效果最佳
- **{random.choice(['远程协作', '混合办公', '传统办公', '移动办公'])}**: 支持度良好，用户反馈积极

### 投资回报分析

从我的专业财务分析角度：
- **初始投资**: {context.tool_name}的定价{random.choice(['具有竞争力', '偏高但合理', '性价比突出'])}
- **运营成本**: 预估每月额外成本{random.randint(50, 500)}元（基于中等规模团队）
- **效率提升**: 我观察到平均效率提升{random.randint(15, 45)}%
- **投资回收期**: 预计{random.randint(3, 12)}个月内可以看到明显回报"""

        return assessment
    
    def _generate_controversy_analysis(self, context: ContentContext) -> str:
        """生成争议话题分析"""
        if not context.is_controversial:
            return ""
        
        controversy_level = context.controversy_level
        acknowledgment = random.choice(self.controversy_handlers["controversy_acknowledgment"][controversy_level])
        
        controversy_content = f"""## 争议话题专业分析

### 当前争议概述

{acknowledgment.format(title=self.profile.title, tool_name=context.tool_name, category=context.category)}

### 我的专业观点

作为一名{self.profile.title}，我认为对争议性问题保持客观和专业的态度至关重要。以下是我的分析：

"""
        
        # 根据争议级别添加不同深度的分析
        if controversy_level == "high":
            controversy_content += self._generate_high_controversy_analysis(context)
        elif controversy_level == "medium":
            controversy_content += self._generate_medium_controversy_analysis(context)
        else:
            controversy_content += self._generate_low_controversy_analysis(context)
        
        # 添加解决方案导向的内容
        controversy_content += self._generate_solution_oriented_content(context)
        
        return controversy_content
    
    def _generate_high_controversy_analysis(self, context: ContentContext) -> str:
        """生成高争议度分析"""
        return f"""**问题的核心**: 基于我的深入调研，{context.tool_name}面临的主要问题包括：
- 用户体验下降的客观原因分析
- 技术架构调整带来的短期影响
- 市场预期与产品发展节奏的不匹配

**我的专业建议**: 
- 短期内建议谨慎使用，密切关注官方改进措施
- 准备备用方案，确保业务连续性
- 等待1-2个产品更新周期后重新评估

**行业背景**: 从我的专业观察来看，这类问题在{context.category}行业中并不罕见，通常与技术升级周期有关。"""

    def _generate_medium_controversy_analysis(self, context: ContentContext) -> str:
        """生成中等争议度分析"""
        return f"""**争议焦点**: 我注意到争议主要集中在以下方面：
- 部分功能体验的确有所变化
- 用户适应新版本需要时间
- 不同用户群体的需求差异明显

**平衡的视角**: 
- 问题确实存在，但影响程度因人而异
- 官方正在积极响应用户反馈
- 长期发展趋势仍然积极

**实用建议**: 
- 现有用户可以继续使用，注意版本更新
- 新用户建议先试用再决定
- 关注官方roadmap和社区反馈"""

    def _generate_low_controversy_analysis(self, context: ContentContext) -> str:
        """生成低争议度分析"""
        return f"""**争议性质**: 从我的专业分析来看，当前的争议更多属于：
- 正常的产品迭代过程中的反馈
- 用户期望与产品定位的小幅偏差
- 竞品对比中的相对劣势讨论

**我的判断**: 
- 这些问题不会影响{context.tool_name}的核心价值主张
- 用户可以正常使用，无需过度担心
- 持续关注产品更新即可

**专业建议**: 
- 争议不足以影响使用决策
- focus在产品本身的价值匹配度上
- 保持对市场动态的关注"""

    def _generate_solution_oriented_content(self, context: ContentContext) -> str:
        """生成解决方案导向内容"""
        solutions = f"""

### 实用解决方案

基于我的专业经验，针对当前情况我建议：

**立即可行的措施**:
1. {random.choice(self.controversy_handlers['solution_oriented']['immediate_actions'])}
2. 建立定期评估机制，跟踪产品改进进度
3. 与团队成员保持沟通，收集一手使用反馈

**备选方案评估**:
{random.choice(self.controversy_handlers['solution_oriented']['alternative_solutions'])}

**长期策略**:
{random.choice(self.controversy_handlers['solution_oriented']['long_term_outlook']).format(tool_name=context.tool_name, outlook=random.choice(['保持乐观', '需要观察', '存在变数']), prediction='技术问题通常会在2-3个更新周期内得到解决', recommendation='建议保持关注但无需恐慌')}"""

        return solutions
    
    def _generate_professional_recommendations(self, context: ContentContext) -> str:
        """生成专业建议"""
        recommendations = f"""## 专业使用建议

### 适用人群分析

基于我的{self.profile.experience_years}年专业经验，{context.tool_name}最适合：

**✅ 强烈推荐**:
- {random.choice(['技术敏感度较高', '预算充足', '追求效率优化', '注重创新'])}的{random.choice(['个人用户', '小团队', '中型企业', '大型组织'])}
- 在{context.category}领域有{random.choice(['基础经验', '深度需求', '专业要求', '创新需求'])}的用户
- 能够接受{random.choice(['学习成本', '功能复杂度', '价格投入', '更新频率'])}的专业用户

**⚠️ 需要考虑**:
- {random.choice(['预算有限', '技术基础薄弱', '需求简单', '传统习惯重'])}的用户可能需要评估是否值得投入
- 对{random.choice(['稳定性', '简单性', '成本控制', '快速上手'])}要求极高的场景需要谨慎选择

### 实施建议

**阶段1: 试用评估** (建议时长: {random.randint(7, 30)}天)
- 重点测试核心功能是否满足需求
- 评估团队接受度和学习成本
- 与现有工作流程的集成难度

**阶段2: 小规模部署** (建议时长: {random.randint(30, 90)}天)  
- 选择1-2个关键场景先行应用
- 收集详细的使用数据和反馈
- 建立最佳实践和使用规范

**阶段3: 全面推广** (如果前期效果良好)
- 制定培训计划和支持体系
- 建立效果评估和持续优化机制
- 考虑与其他工具的深度集成

### 成本优化策略

从我的专业财务分析角度，建议：
- 充分利用免费试用期进行全面测试
- 考虑年付折扣和团队套餐的成本优势  
- 建立ROI跟踪机制，确保投资价值
- 定期评估使用情况，避免功能过度付费"""

        return recommendations
    
    def _generate_professional_conclusion(self, context: ContentContext) -> str:
        """生成专业结论"""
        # 根据争议情况调整结论语调
        if context.is_controversial:
            if context.controversy_level == "high":
                recommendation_tone = "建议谨慎评估"
                confidence_level = "中等保留"
            elif context.controversy_level == "medium":
                recommendation_tone = "建议综合考虑"
                confidence_level = "相对谨慎"
            else:
                recommendation_tone = "可以考虑使用"
                confidence_level = "基本积极"
        else:
            recommendation_tone = random.choice(["推荐使用", "值得投资", "适合采用"])
            confidence_level = "专业推荐"
        
        conclusion = f"""## 专业总结与建议

### 我的最终评估

作为一名{self.profile.title}，基于我{self.profile.experience_years}年的专业经验和对{context.tool_name}的深度测试，我的结论是：**{recommendation_tone}**。

**核心判断**:
- **功能成熟度**: {random.choice(['业界领先', '行业标准', '基本满足', '有待提升'])}
- **用户体验**: {random.choice(['优秀', '良好', '中等', '需要改进'])}
- **投资价值**: {random.choice(['高', '中等', '需要评估', '相对有限'])}
- **推荐指数**: ⭐⭐⭐{random.choice(['⭐⭐', '⭐', '', ''])} ({confidence_level})

### 决策建议框架

**如果你是...**
- **{context.category}新手**: {self._get_newbie_advice(context)}
- **经验用户**: {self._get_experienced_advice(context)}  
- **企业决策者**: {self._get_enterprise_advice(context)}

### 我的专业承诺

作为{self.profile.title}，我会持续关注{context.tool_name}的发展动态，并及时更新我的专业评估。如果你在使用过程中遇到问题，欢迎参考我的其他专业分析文章。

**最后提醒**: 任何工具的选择都应该基于你的具体需求和实际情况。我的分析仅供参考，最终决策请结合自己的实际测试和判断。

---
*本文基于我的专业经验和实际测试撰写，力求客观公正。如有不同观点，欢迎理性讨论。*"""

        return conclusion
    
    def _get_newbie_advice(self, context: ContentContext) -> str:
        """新手建议"""
        return random.choice([
            f"建议从免费版或基础功能开始，充分了解{context.category}工具的基本概念后再考虑升级",
            f"可以先通过教程和社区资源学习，降低学习成本和使用风险", 
            f"建议对比多个同类产品，选择最符合新手需求的方案"
        ])
    
    def _get_experienced_advice(self, context: ContentContext) -> str:
        """经验用户建议"""
        return random.choice([
            f"重点关注高级功能和定制化选项，充分发挥{context.tool_name}的专业价值",
            f"可以考虑将现有工作流程迁移到{context.tool_name}，利用其优势优化效率",
            f"建议深度测试API和集成功能，实现与现有工具链的无缝对接"
        ])
    
    def _get_enterprise_advice(self, context: ContentContext) -> str:
        """企业建议"""
        return random.choice([
            f"重点评估{context.tool_name}的安全性、稳定性和可扩展性，确保符合企业级需求",
            f"建议进行小规模试点，收集团队反馈后再决定大规模部署",
            f"关注总拥有成本(TCO)和投资回报率(ROI)，建立长期效果评估机制"
        ])
    
    def generate_seo_optimized_headings(self, context: ContentContext) -> List[str]:
        """生成SEO优化的标题"""
        headings = []
        
        # 基于问题的标题
        question_templates = self.seo_patterns["question_based_headings"]
        for template in random.sample(question_templates, 3):
            headings.append(template.format(tool_name=context.tool_name, category=context.category))
        
        # 长尾关键词标题
        longtail_templates = self.seo_patterns["long_tail_keywords"]
        for template in random.sample(longtail_templates, 2):
            headings.append(template.format(tool_name=context.tool_name))
        
        return headings
    
    def get_semantic_keyword_clusters(self, context: ContentContext) -> Dict[str, List[str]]:
        """获取语义关键词聚类"""
        clusters = {}
        
        for i, cluster in enumerate(self.seo_patterns["semantic_clusters"]):
            cluster_name = f"cluster_{i+1}"
            # 为每个聚类添加工具名称组合
            tool_combinations = [f"{context.tool_name} {keyword}" for keyword in cluster]
            clusters[cluster_name] = tool_combinations
        
        return clusters


def main():
    """测试专业模板系统"""
    print("🎯 测试专业第一人称模板系统...")
    
    # 创建测试上下文
    test_context = ContentContext(
        tool_name="Claude AI",
        category="content_creation",
        is_controversial=True,
        controversy_level="medium",
        target_keywords=["claude ai", "ai写作工具", "内容生成"],
        user_intent="comparison",
        content_angle="problem_solving"
    )
    
    # 初始化模板系统
    template_system = ProfessionalTemplateSystem()
    
    # 生成内容
    print("📝 生成专业化内容...")
    content_sections = template_system.generate_professional_content(test_context)
    
    # 显示生成的内容
    for section_name, content in content_sections.items():
        print(f"\n{'='*60}")
        print(f"📄 {section_name.upper()}")
        print('='*60)
        print(content[:500] + "..." if len(content) > 500 else content)
    
    # 生成SEO标题
    print(f"\n{'='*60}")
    print("🔍 SEO优化标题建议")
    print('='*60)
    seo_headings = template_system.generate_seo_optimized_headings(test_context)
    for i, heading in enumerate(seo_headings, 1):
        print(f"{i}. {heading}")
    
    print(f"\n✅ 专业模板系统测试完成")

if __name__ == "__main__":
    main()