#!/usr/bin/env python3
"""
Advanced Anti-AI Detection System
高级反AI检测系统 - 深度人性化写作模式
"""

import random
import re
import json
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class HumanizationConfig:
    """人性化配置"""
    sentence_length_variance: float = 0.3  # 句长变异度
    paragraph_structure_randomness: float = 0.25  # 段落结构随机性
    vocabulary_diversity_level: float = 0.8  # 词汇多样性水平
    personal_voice_intensity: float = 0.6  # 个人语音强度
    imperfection_level: float = 0.1  # 不完美程度
    conversational_tone: float = 0.4  # 对话语调

class AdvancedAntiAIDetection:
    """
    高级反AI检测系统
    实现深度人性化写作，规避AI检测工具
    """
    
    def __init__(self, config: Optional[HumanizationConfig] = None):
        self.config = config or HumanizationConfig()
        self.humanization_patterns = self._load_humanization_patterns()
        self.vocabulary_variations = self._load_vocabulary_variations()
        self.sentence_transformers = self._load_sentence_transformers()
        self.personal_voice_elements = self._load_personal_voice_elements()
        
    def _load_humanization_patterns(self) -> Dict[str, List]:
        """加载人性化写作模式"""
        return {
            "sentence_starters": {
                "analytical": [
                    "从我的观察来看，", "基于实际体验，", "我发现", "值得注意的是",
                    "有趣的是", "令人印象深刻的是", "不得不说", "坦率地说",
                    "从实用角度讲", "客观来说", "综合考虑后"
                ],
                "personal": [
                    "我个人认为", "在我看来", "我的感受是", "就我而言",
                    "从我的经验来说", "我比较倾向于", "我注意到", "我发现",
                    "让我印象深刻的是", "我必须承认"
                ],
                "casual": [
                    "说实话", "老实说", "不瞒你说", "简单来说", "换句话说",
                    "这么说吧", "打个比方", "举个例子", "总的来说", "顺便说一下"
                ]
            },
            
            "transition_phrases": {
                "logical": [
                    "因此", "所以", "然而", "不过", "另外", "此外", "同时",
                    "相比之下", "与此同时", "话说回来", "换个角度看"
                ],
                "casual": [
                    "话又说回来", "不过话说", "顺便提一下", "说到这里",
                    "另一方面", "从另一个角度", "这样看来", "总而言之"
                ],
                "emphasis": [
                    "更重要的是", "关键在于", "需要强调的是", "值得一提的是",
                    "特别是", "尤其是", "最关键的是", "不容忽视的是"
                ]
            },
            
            "sentence_endings": {
                "definitive": ["。", "！", "..."],
                "questioning": ["？", "吧？", "呢？"],
                "uncertain": ["似乎是这样", "大概是", "应该说", "可能"]
            },
            
            "paragraph_connectors": [
                "接下来让我们看看", "现在说说", "再来谈谈", "另外一个方面",
                "我们再来分析", "让我们深入了解", "值得探讨的是"
            ]
        }
    
    def _load_vocabulary_variations(self) -> Dict[str, List]:
        """加载词汇变换库"""
        return {
            "professional_synonyms": {
                "分析": ["评估", "研究", "解析", "剖析", "考察", "审视", "探讨"],
                "使用": ["应用", "运用", "采用", "利用", "操作", "部署"],
                "功能": ["特性", "能力", "特点", "优势", "亮点", "卖点"],
                "效果": ["表现", "成效", "结果", "效果", "成果", "收效"],
                "问题": ["挑战", "难点", "症结", "瓶颈", "困难", "障碍"],
                "优势": ["亮点", "强项", "长处", "特色", "优点", "特长"],
                "缺点": ["不足", "短板", "局限", "弱点", "缺陷", "问题"],
                "建议": ["推荐", "提议", "倡议", "主张", "意见", "看法"],
                "重要": ["关键", "核心", "关键", "要紧", "重大", "紧要"],
                "提升": ["改善", "增强", "优化", "改进", "强化", "升级"]
            },
            
            "casual_expressions": {
                "很好": ["不错", "挺棒", "相当好", "很赞", "值得推荐", "表现出色"],
                "一般": ["中规中矩", "还算可以", "差强人意", "马马虎虎", "中等水平"],
                "不好": ["有待改进", "略显不足", "表现平平", "不太理想", "存在问题"],
                "确实": ["的确", "确实", "真的", "没错", "是的", "对的"],
                "可能": ["也许", "大概", "或许", "估计", "可能", "应该"]
            },
            
            "technical_variations": {
                "算法": ["技术实现", "核心逻辑", "处理机制", "计算方法"],
                "界面": ["用户界面", "操作界面", "交互设计", "UI设计"],
                "数据": ["信息", "内容", "资料", "素材"],
                "系统": ["平台", "工具", "软件", "应用"],
                "性能": ["表现", "效率", "速度", "响应"]
            }
        }
    
    def _load_sentence_transformers(self) -> Dict[str, callable]:
        """加载句子变换器"""
        return {
            "add_hesitation": self._add_hesitation_markers,
            "vary_sentence_length": self._vary_sentence_length,
            "add_personal_touch": self._add_personal_touch,
            "introduce_imperfection": self._introduce_subtle_imperfection,
            "casual_connector": self._add_casual_connectors,
            "questioning_tone": self._add_questioning_elements
        }
    
    def _load_personal_voice_elements(self) -> Dict[str, List]:
        """加载个人语音元素"""
        return {
            "personal_experiences": [
                "在我的实际使用中", "通过我的测试", "根据我的观察",
                "从我的体验来看", "在我接触过的工具中", "我在项目中发现",
                "通过与同事的讨论", "基于我的专业判断"
            ],
            
            "emotional_responses": [
                "让我印象深刻的是", "令我意外的是", "我比较喜欢的是",
                "有点遗憾的是", "让我惊喜的是", "我觉得比较遗憾的是",
                "让我比较满意的是", "我个人比较偏爱"
            ],
            
            "uncertainty_markers": [
                "我觉得", "在我看来", "个人感觉", "我的印象是",
                "似乎", "好像", "大概", "应该说", "可能", "也许"
            ],
            
            "conversational_fillers": [
                "嗯", "呢", "吧", "哦", "额", "这个", "那个", "就是说",
                "怎么说呢", "这样说吧", "简单来说", "总之"
            ]
        }
    
    def humanize_content(self, content: str, context: Optional[Dict] = None) -> str:
        """对内容进行全面人性化处理"""
        content = self._preprocess_content(content)
        
        # 分段处理
        paragraphs = content.split('\n\n')
        humanized_paragraphs = []
        
        for i, paragraph in enumerate(paragraphs):
            if paragraph.strip():
                humanized = self._humanize_paragraph(paragraph, i, context)
                humanized_paragraphs.append(humanized)
        
        # 后处理
        result = '\n\n'.join(humanized_paragraphs)
        result = self._post_process_content(result)
        
        return result
    
    def _preprocess_content(self, content: str) -> str:
        """预处理内容"""
        # 移除过于规整的格式
        content = re.sub(r'\n{3,}', '\n\n', content)
        # 添加适度的格式变化
        return content
    
    def _humanize_paragraph(self, paragraph: str, paragraph_index: int, context: Optional[Dict]) -> str:
        """人性化单个段落"""
        sentences = self._split_sentences(paragraph)
        humanized_sentences = []
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                humanized = self._humanize_sentence(sentence, i, paragraph_index, context)
                humanized_sentences.append(humanized)
        
        # 段落级别的处理
        result = ' '.join(humanized_sentences)
        result = self._add_paragraph_personality(result, paragraph_index)
        
        return result
    
    def _split_sentences(self, paragraph: str) -> List[str]:
        """智能分句"""
        # 使用正则表达式分句，考虑中文标点
        sentences = re.split(r'[。！？；]\s*', paragraph)
        return [s.strip() for s in sentences if s.strip()]
    
    def _humanize_sentence(self, sentence: str, sentence_index: int, paragraph_index: int, context: Optional[Dict]) -> str:
        """人性化单个句子"""
        # 随机应用变换器
        transformers = list(self.sentence_transformers.keys())
        num_transforms = random.randint(1, min(3, len(transformers)))
        selected_transforms = random.sample(transformers, num_transforms)
        
        result = sentence
        for transform_name in selected_transforms:
            transformer = self.sentence_transformers[transform_name]
            if random.random() < self._get_transform_probability(transform_name):
                result = transformer(result, sentence_index, paragraph_index)
        
        return result
    
    def _get_transform_probability(self, transform_name: str) -> float:
        """获取变换概率"""
        probabilities = {
            "add_hesitation": self.config.conversational_tone * 0.3,
            "vary_sentence_length": 0.6,
            "add_personal_touch": self.config.personal_voice_intensity * 0.4,
            "introduce_imperfection": self.config.imperfection_level,
            "casual_connector": self.config.conversational_tone * 0.25,
            "questioning_tone": 0.15
        }
        return probabilities.get(transform_name, 0.2)
    
    def _add_hesitation_markers(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """添加犹豫标记"""
        if random.random() < 0.3:
            markers = self.personal_voice_elements["uncertainty_markers"]
            marker = random.choice(markers)
            # 在句子开头或中间插入
            if random.random() < 0.7:
                return f"{marker}，{sentence}"
            else:
                words = sentence.split()
                if len(words) > 3:
                    insert_pos = random.randint(1, len(words) - 2)
                    words.insert(insert_pos, f"{marker}，")
                    return ' '.join(words)
        return sentence
    
    def _vary_sentence_length(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """变化句子长度"""
        words = sentence.split()
        if len(words) < 5:
            # 扩展短句
            if random.random() < 0.4:
                extensions = ["确实如此", "这一点很重要", "值得注意", "需要考虑"]
                return f"{sentence}，{random.choice(extensions)}"
        elif len(words) > 15:
            # 分解长句
            if random.random() < 0.3:
                mid_point = len(words) // 2
                first_part = ' '.join(words[:mid_point])
                second_part = ' '.join(words[mid_point:])
                connectors = ["。同时", "。另外", "。而且", "。不过"]
                return f"{first_part}{random.choice(connectors)}，{second_part}"
        return sentence
    
    def _add_personal_touch(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """添加个人化元素"""
        if random.random() < 0.3:
            personal_elements = self.personal_voice_elements["personal_experiences"]
            element = random.choice(personal_elements)
            return f"{element}，{sentence}"
        elif random.random() < 0.2:
            emotional_elements = self.personal_voice_elements["emotional_responses"]
            element = random.choice(emotional_elements)
            return f"{element}，{sentence}"
        return sentence
    
    def _introduce_subtle_imperfection(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """引入细微的不完美"""
        if random.random() < self.config.imperfection_level:
            # 添加口语化表达
            fillers = self.personal_voice_elements["conversational_fillers"]
            if random.random() < 0.5:
                filler = random.choice(fillers)
                return f"{sentence}{filler}"
            # 或者添加不太正式的连接词
            elif random.random() < 0.3:
                casual_endings = ["吧", "呢", "啊", "嘛"]
                return f"{sentence}{random.choice(casual_endings)}"
        return sentence
    
    def _add_casual_connectors(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """添加随意的连接词"""
        if sentence_index > 0 and random.random() < 0.2:
            connectors = self.humanization_patterns["transition_phrases"]["casual"]
            connector = random.choice(connectors)
            return f"{connector}，{sentence}"
        return sentence
    
    def _add_questioning_elements(self, sentence: str, sentence_index: int, paragraph_index: int) -> str:
        """添加疑问元素"""
        if random.random() < 0.15:
            if sentence.endswith('。'):
                questioning_endings = ["吗？", "呢？", "对吧？", "是不是？"]
                return sentence[:-1] + random.choice(questioning_endings)
        return sentence
    
    def _add_paragraph_personality(self, paragraph: str, paragraph_index: int) -> str:
        """为段落添加个性化元素"""
        # 段落开头的个性化
        if paragraph_index == 0:
            starters = self.humanization_patterns["sentence_starters"]["personal"]
            if random.random() < 0.3:
                starter = random.choice(starters)
                paragraph = f"{starter}，{paragraph}"
        
        # 段落连接的自然化
        elif random.random() < 0.4:
            connectors = self.humanization_patterns["paragraph_connectors"]
            connector = random.choice(connectors)
            paragraph = f"{connector}，{paragraph}"
        
        return paragraph
    
    def _post_process_content(self, content: str) -> str:
        """后处理内容"""
        # 词汇多样化
        content = self._diversify_vocabulary(content)
        
        # 调整标点符号的使用
        content = self._humanize_punctuation(content)
        
        # 最终的自然化处理
        content = self._final_naturalization(content)
        
        return content
    
    def _diversify_vocabulary(self, content: str) -> str:
        """词汇多样化"""
        for category, synonyms_dict in self.vocabulary_variations.items():
            for original, alternatives in synonyms_dict.items():
                if original in content:
                    # 随机替换部分词汇
                    occurrences = content.count(original)
                    if occurrences > 1:
                        replace_count = max(1, int(occurrences * self.config.vocabulary_diversity_level))
                        for _ in range(replace_count):
                            if random.random() < 0.7:
                                alternative = random.choice(alternatives)
                                content = content.replace(original, alternative, 1)
        return content
    
    def _humanize_punctuation(self, content: str) -> str:
        """人性化标点符号"""
        # 偶尔使用省略号
        content = re.sub(r'。(?=\s*[A-Z\u4e00-\u9fff])', lambda m: '...' if random.random() < 0.05 else '。', content)
        
        # 添加感叹号表达情感
        content = re.sub(r'(\u4e00-\u9fff{3,}[很非常特别])([^！。？]*?)。', 
                        lambda m: f"{m.group(1)}{m.group(2)}！" if random.random() < 0.3 else m.group(0), content)
        
        return content
    
    def _final_naturalization(self, content: str) -> str:
        """最终自然化处理"""
        # 调整段落间距的一致性
        content = re.sub(r'\n\n+', '\n\n', content)
        
        # 移除过于机械化的模式
        content = re.sub(r'(同时|此外|另外|然而)，\s*\1', lambda m: m.group(1), content)
        
        return content.strip()
    
    def calculate_humanization_score(self, content: str) -> Dict[str, float]:
        """计算人性化分数"""
        scores = {
            "sentence_variation": self._assess_sentence_variation(content),
            "vocabulary_diversity": self._assess_vocabulary_diversity(content),
            "personal_voice": self._assess_personal_voice(content),
            "natural_flow": self._assess_natural_flow(content),
            "imperfection_authenticity": self._assess_imperfection_level(content)
        }
        
        scores["overall_score"] = sum(scores.values()) / len(scores)
        return scores
    
    def _assess_sentence_variation(self, content: str) -> float:
        """评估句子变化度"""
        sentences = re.split(r'[。！？]', content)
        if len(sentences) < 2:
            return 0.5
        
        lengths = [len(s.split()) for s in sentences if s.strip()]
        if not lengths:
            return 0.5
        
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        
        # 标准化变异度分数
        return min(1.0, variance / (avg_length ** 2))
    
    def _assess_vocabulary_diversity(self, content: str) -> float:
        """评估词汇多样性"""
        words = re.findall(r'\b\w+\b', content.lower())
        if not words:
            return 0.0
        
        unique_words = set(words)
        return len(unique_words) / len(words)
    
    def _assess_personal_voice(self, content: str) -> float:
        """评估个人化程度"""
        personal_markers = sum(len(markers) for markers in self.personal_voice_elements.values())
        found_markers = 0
        
        for marker_category in self.personal_voice_elements.values():
            for marker in marker_category:
                if marker in content:
                    found_markers += content.count(marker)
        
        return min(1.0, found_markers / max(1, len(content.split()) // 20))
    
    def _assess_natural_flow(self, content: str) -> float:
        """评估自然流畅度"""
        # 简化的流畅度评估
        mechanical_patterns = [
            r'(首先|其次|再次|最后).*?。.*?(首先|其次|再次|最后)',
            r'(因此|所以|然而).*?。.*?(因此|所以|然而)',
            r'^\d+\..*?^\d+\.',  # 列表模式
        ]
        
        penalty = 0
        for pattern in mechanical_patterns:
            matches = len(re.findall(pattern, content, re.MULTILINE))
            penalty += matches * 0.1
        
        return max(0.0, 1.0 - penalty)
    
    def _assess_imperfection_level(self, content: str) -> float:
        """评估不完美程度（适度的不完美提高真实性）"""
        imperfection_markers = ['嗯', '呢', '吧', '哦', '这个', '那个', '怎么说', '大概', '可能', '也许']
        found_imperfections = sum(content.count(marker) for marker in imperfection_markers)
        
        # 适度的不完美是好的
        ideal_ratio = 0.02  # 每100个字有2个不完美标记
        actual_ratio = found_imperfections / max(1, len(content))
        
        # 计算与理想比例的接近程度
        return 1.0 - abs(actual_ratio - ideal_ratio) / ideal_ratio


def main():
    """测试高级反AI检测系统"""
    print("🎭 测试高级反AI检测系统...")
    
    # 测试文本
    test_content = """
这是一个AI工具的专业分析。该工具具有强大的功能，可以提升工作效率。
用户可以通过简单的操作来使用这些功能。该工具的界面设计非常专业。
总体来说，这是一个值得推荐的AI工具。它的性能表现优秀，价格合理。
"""
    
    # 初始化系统
    humanizer = AdvancedAntiAIDetection()
    
    print("📝 原始内容:")
    print(test_content)
    
    print("\n🎭 人性化后的内容:")
    humanized_content = humanizer.humanize_content(test_content)
    print(humanized_content)
    
    print("\n📊 人性化评分:")
    scores = humanizer.calculate_humanization_score(humanized_content)
    for metric, score in scores.items():
        print(f"  {metric}: {score:.3f}")
    
    print(f"\n✅ 高级反AI检测系统测试完成")

if __name__ == "__main__":
    main()