#!/usr/bin/env python3
"""
Multi-Source Trending Topics Detector
整合多个免费数据源检测AI工具热门话题和争议
"""

import json
import os
import requests
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import pandas as pd
from pathlib import Path
import feedparser
import praw
from pytrends.request import TrendReq

# Import advanced controversy detector
try:
    from .advanced_controversy_detector import AdvancedControversyDetector, ControversyAnalysis
except ImportError:
    # Fallback if import fails
    AdvancedControversyDetector = None
    ControversyAnalysis = None

@dataclass
class TrendingTopic:
    """热门话题数据结构"""
    keyword: str
    source: str  # reddit, news, hackernews, rss
    score: int  # 热度分数 0-100
    controversy_score: int  # 争议分数 0-100
    sentiment: str  # positive, negative, neutral
    related_terms: List[str]
    timestamp: str
    url: Optional[str] = None
    content_snippet: str = ""

class MultiSourceTrendDetector:
    """
    多数据源趋势检测器
    整合Reddit、新闻API、HackerNews、RSS等免费数据源
    """
    
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化高级争议检测器
        if AdvancedControversyDetector:
            self.advanced_controversy_detector = AdvancedControversyDetector(cache_dir)
            print("✅ 高级争议检测器已初始化")
        else:
            self.advanced_controversy_detector = None
            print("⚠️ 高级争议检测器加载失败，使用基础检测")
        
        # 保留原有的争议关键词库作为备用
        self.controversy_keywords = {
            'english': [
                'problem', 'issue', 'bug', 'error', 'fail', 'broken', 'worse', 
                'downgrade', 'decline', 'controversy', 'scandal', 'criticism',
                'lawsuit', 'banned', 'restricted', 'censored', 'terrible',
                'awful', 'horrible', 'disaster', 'scam', 'rip_off'
            ],
            'chinese': [
                '问题', '故障', '降智', '性能下降', '争议', '批评', '质疑',
                '投诉', '不满', '失望', '变差', '倒退', '翻车', '拉胯',
                '割韭菜', '智商税', '坑', '黑心'
            ]
        }
        
        # AI工具关键词
        self.ai_tools = [
            'ChatGPT', 'Claude AI', 'GPT-4', 'GPT-5', 'Gemini', 'Perplexity',
            'Character.AI', 'Midjourney', 'DALL-E', 'Stable Diffusion',
            'GitHub Copilot', 'Anthropic', 'OpenAI', 'Google AI'
        ]
        
        # 免费RSS源
        self.rss_feeds = [
            'https://feeds.feedburner.com/oreilly/radar/ai',
            'https://techcrunch.com/category/artificial-intelligence/feed/',
            'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
            'https://venturebeat.com/ai/feed/',
            'https://www.artificialintelligence-news.com/feed/'
        ]
        
        # 初始化各个API客户端
        self.setup_apis()
    
    def setup_apis(self):
        """初始化各种API客户端"""
        # Reddit API
        try:
            if all(key in os.environ for key in ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']):
                self.reddit = praw.Reddit(
                    client_id=os.environ.get('REDDIT_CLIENT_ID'),
                    client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    user_agent=os.environ.get('REDDIT_USER_AGENT', 'AI-Discovery/1.0')
                )
            else:
                self.reddit = None
                print("Reddit API credentials not found")
        except Exception as e:
            print(f"Reddit API setup failed: {e}")
            self.reddit = None
        
        # News API
        self.news_api_key = os.environ.get('NEWS_API_KEY')
        
        # PyTrends
        try:
            self.pytrends = TrendReq(
                hl='en-US', 
                tz=360,
                retries=2,
                backoff_factor=0.5
            )
        except:
            self.pytrends = None
        
        print(f"APIs initialized - Reddit: {'✓' if self.reddit else '✗'}, News: {'✓' if self.news_api_key else '✗'}")
    
    def detect_reddit_trends(self, limit: int = 20) -> List[TrendingTopic]:
        """检测Reddit AI相关热门话题"""
        topics = []
        
        if not self.reddit:
            return topics
            
        try:
            # 监控的AI相关subreddits
            subreddits = ['artificial', 'MachineLearning', 'OpenAI', 'ChatGPT', 'singularity']
            
            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # 获取热门帖子
                for post in subreddit.hot(limit=10):
                    if any(tool.lower() in post.title.lower() for tool in self.ai_tools):
                        post_timestamp = datetime.fromtimestamp(post.created_utc).isoformat()
                        controversy_score = self._calculate_controversy_score(
                            post.title + " " + (post.selftext or ""), 
                            f"reddit_{subreddit_name}", 
                            post_timestamp
                        )
                        
                        topic = TrendingTopic(
                            keyword=self._extract_main_keyword(post.title),
                            source=f"reddit_{subreddit_name}",
                            score=min(100, int(post.score / 10)),  # 转换为0-100分数
                            controversy_score=controversy_score,
                            sentiment=self._analyze_sentiment(post.title),
                            related_terms=self._extract_keywords(post.title),
                            timestamp=datetime.fromtimestamp(post.created_utc).isoformat(),
                            url=f"https://reddit.com{post.permalink}",
                            content_snippet=post.title[:200]
                        )
                        topics.append(topic)
                
                # 延迟避免限流
                time.sleep(1)
                
        except Exception as e:
            print(f"Reddit trend detection error: {e}")
        
        return sorted(topics, key=lambda x: x.score + x.controversy_score, reverse=True)[:limit]
    
    def detect_news_trends(self, limit: int = 15) -> List[TrendingTopic]:
        """检测新闻API中的AI话题趋势"""
        topics = []
        
        if not self.news_api_key:
            return topics
        
        try:
            # 搜索AI工具相关新闻
            for tool in self.ai_tools[:5]:  # 限制请求数量
                url = f"https://newsapi.org/v2/everything"
                params = {
                    'q': f'"{tool}"',
                    'language': 'en',
                    'sortBy': 'popularity',
                    'pageSize': 5,
                    'apiKey': self.news_api_key,
                    'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    for article in data.get('articles', []):
                        title = article.get('title', '')
                        description = article.get('description', '')
                        content = f"{title} {description}"
                        
                        controversy_score = self._calculate_controversy_score(
                            content, "news_api", article.get('publishedAt')
                        )
                        
                        topic = TrendingTopic(
                            keyword=tool,
                            source="news_api",
                            score=self._calculate_news_score(article),
                            controversy_score=controversy_score,
                            sentiment=self._analyze_sentiment(content),
                            related_terms=self._extract_keywords(title),
                            timestamp=article.get('publishedAt', datetime.now().isoformat()),
                            url=article.get('url', ''),
                            content_snippet=title
                        )
                        topics.append(topic)
                
                time.sleep(0.5)  # 限流
                
        except Exception as e:
            print(f"News API error: {e}")
        
        return sorted(topics, key=lambda x: x.score + x.controversy_score, reverse=True)[:limit]
    
    def detect_hackernews_trends(self, limit: int = 10) -> List[TrendingTopic]:
        """检测HackerNews上的AI话题趋势"""
        topics = []
        
        try:
            # 获取HackerNews热门故事
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(top_stories_url, timeout=10)
            
            if response.status_code == 200:
                story_ids = response.json()[:50]  # 获取前50个热门故事
                
                for story_id in story_ids[:20]:  # 检查前20个
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = requests.get(story_url, timeout=5)
                    
                    if story_response.status_code == 200:
                        story = story_response.json()
                        title = story.get('title', '')
                        
                        # 检查是否包含AI工具关键词
                        if any(tool.lower() in title.lower() for tool in self.ai_tools):
                            story_timestamp = datetime.fromtimestamp(story.get('time', time.time())).isoformat()
                            controversy_score = self._calculate_controversy_score(
                                title, "hackernews", story_timestamp
                            )
                            
                            topic = TrendingTopic(
                                keyword=self._extract_main_keyword(title),
                                source="hackernews",
                                score=min(100, story.get('score', 0)),
                                controversy_score=controversy_score,
                                sentiment=self._analyze_sentiment(title),
                                related_terms=self._extract_keywords(title),
                                timestamp=datetime.fromtimestamp(story.get('time', time.time())).isoformat(),
                                url=story.get('url', ''),
                                content_snippet=title
                            )
                            topics.append(topic)
                    
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"HackerNews detection error: {e}")
        
        return sorted(topics, key=lambda x: x.score + x.controversy_score, reverse=True)[:limit]
    
    def detect_rss_trends(self, limit: int = 15) -> List[TrendingTopic]:
        """检测RSS源中的AI话题趋势"""
        topics = []
        
        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:10]:  # 每个源取10条
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    content = f"{title} {summary}"
                    
                    # 检查是否包含AI工具
                    if any(tool.lower() in content.lower() for tool in self.ai_tools):
                        source_name = f"rss_{feed_url.split('/')[2]}"  # 提取域名
                        controversy_score = self._calculate_controversy_score(
                            content, source_name, entry.get('published')
                        )
                        
                        topic = TrendingTopic(
                            keyword=self._extract_main_keyword(title),
                            source=f"rss_{feed_url.split('/')[2]}",  # 提取域名
                            score=self._calculate_rss_score(entry),
                            controversy_score=controversy_score,
                            sentiment=self._analyze_sentiment(content),
                            related_terms=self._extract_keywords(title),
                            timestamp=entry.get('published', datetime.now().isoformat()),
                            url=entry.get('link', ''),
                            content_snippet=title
                        )
                        topics.append(topic)
                        
            except Exception as e:
                print(f"RSS feed error for {feed_url}: {e}")
                continue
        
        return sorted(topics, key=lambda x: x.score + x.controversy_score, reverse=True)[:limit]
    
    def _calculate_controversy_score(self, text: str, source: str = "unknown", timestamp: str = None) -> int:
        """计算争议分数，使用高级检测器或基础方法"""
        if self.advanced_controversy_detector and text:
            try:
                # 使用高级争议检测器
                signal = self.advanced_controversy_detector.analyze_controversy(
                    text, source, timestamp or datetime.now().isoformat()
                )
                return int(signal.intensity)
            except Exception as e:
                print(f"高级争议检测失败，使用基础方法: {e}")
        
        # 基础争议检测（备用方案）
        text_lower = text.lower()
        score = 0
        
        # 英文争议词
        for word in self.controversy_keywords['english']:
            score += text_lower.count(word) * 10
        
        # 中文争议词
        for word in self.controversy_keywords['chinese']:
            score += text.count(word) * 15  # 中文争议词权重更高
        
        return min(100, score)
    
    def _analyze_sentiment(self, text: str) -> str:
        """简单的情感分析"""
        positive_words = ['great', 'amazing', 'good', 'excellent', 'better', 'improved']
        negative_words = ['bad', 'terrible', 'worse', 'problem', 'issue', 'fail']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'
    
    def _extract_main_keyword(self, text: str) -> str:
        """提取主要关键词"""
        for tool in self.ai_tools:
            if tool.lower() in text.lower():
                return tool
        
        # 如果没找到特定工具，返回第一个有意义的词
        words = text.split()
        for word in words:
            if len(word) > 3 and word.lower() not in ['that', 'this', 'with', 'from']:
                return word
        
        return "AI"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取相关关键词"""
        words = text.lower().split()
        keywords = []
        
        for word in words:
            if (len(word) > 4 and 
                word not in ['that', 'this', 'with', 'from', 'they', 'have', 'been', 'will'] and
                not word.isdigit()):
                keywords.append(word)
        
        return keywords[:5]
    
    def _calculate_news_score(self, article: dict) -> int:
        """计算新闻文章分数"""
        # 基于发布时间的新鲜度
        published_at = article.get('publishedAt', '')
        if published_at:
            try:
                pub_time = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                hours_ago = (datetime.now() - pub_time.replace(tzinfo=None)).total_seconds() / 3600
                freshness = max(0, 100 - int(hours_ago))
            except:
                freshness = 50
        else:
            freshness = 50
        
        # 基于来源的权重
        source = article.get('source', {}).get('name', '').lower()
        source_weight = 80 if 'techcrunch' in source or 'reuters' in source else 50
        
        return min(100, (freshness + source_weight) // 2)
    
    def _calculate_rss_score(self, entry: dict) -> int:
        """计算RSS条目分数"""
        # 简单的时间新鲜度计算
        try:
            pub_time = datetime.strptime(entry.get('published', ''), '%a, %d %b %Y %H:%M:%S %z')
            hours_ago = (datetime.now() - pub_time.replace(tzinfo=None)).total_seconds() / 3600
            return max(30, 100 - int(hours_ago // 2))
        except:
            return 50
    
    def get_all_trending_topics(self, limit: int = 30) -> List[TrendingTopic]:
        """获取所有来源的热门话题"""
        all_topics = []
        
        print("🔍 Detecting trends from multiple sources...")
        
        # Reddit趋势
        reddit_topics = self.detect_reddit_trends(limit=8)
        all_topics.extend(reddit_topics)
        print(f"Reddit: {len(reddit_topics)} topics")
        
        # 新闻趋势
        news_topics = self.detect_news_trends(limit=8)
        all_topics.extend(news_topics)
        print(f"News API: {len(news_topics)} topics")
        
        # HackerNews趋势
        hn_topics = self.detect_hackernews_trends(limit=7)
        all_topics.extend(hn_topics)
        print(f"HackerNews: {len(hn_topics)} topics")
        
        # RSS趋势
        rss_topics = self.detect_rss_trends(limit=7)
        all_topics.extend(rss_topics)
        print(f"RSS Feeds: {len(rss_topics)} topics")
        
        # 去重和排序
        unique_topics = self._deduplicate_topics(all_topics)
        sorted_topics = sorted(unique_topics, 
                             key=lambda x: x.score + x.controversy_score * 1.5, 
                             reverse=True)
        
        return sorted_topics[:limit]
    
    def _deduplicate_topics(self, topics: List[TrendingTopic]) -> List[TrendingTopic]:
        """去重话题"""
        seen_keywords = set()
        unique_topics = []
        
        for topic in topics:
            key = topic.keyword.lower()
            if key not in seen_keywords:
                seen_keywords.add(key)
                unique_topics.append(topic)
        
        return unique_topics
    
    def save_trending_cache(self, topics: List[TrendingTopic], filename: str = "multi_source_trends.json"):
        """保存趋势数据到缓存"""
        cache_file = self.cache_dir / filename
        
        cache_data = {
            "generated_at": datetime.now().isoformat(),
            "total_topics": len(topics),
            "sources_used": list(set(topic.source for topic in topics)),
            "topics": [
                {
                    "keyword": topic.keyword,
                    "source": topic.source,
                    "score": topic.score,
                    "controversy_score": topic.controversy_score,
                    "sentiment": topic.sentiment,
                    "related_terms": topic.related_terms,
                    "timestamp": topic.timestamp,
                    "url": topic.url,
                    "content_snippet": topic.content_snippet
                }
                for topic in topics
            ]
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(topics)} trending topics to {cache_file}")
        return cache_file


def main():
    """测试多源趋势检测器"""
    detector = MultiSourceTrendDetector()
    
    print("🚀 Starting multi-source trend detection...")
    topics = detector.get_all_trending_topics(limit=20)
    
    print(f"\n📊 Found {len(topics)} trending AI topics:")
    for i, topic in enumerate(topics[:10], 1):
        print(f"\n{i}. {topic.keyword}")
        print(f"   Source: {topic.source}")
        print(f"   Score: {topic.score}, Controversy: {topic.controversy_score}")
        print(f"   Sentiment: {topic.sentiment}")
        print(f"   Content: {topic.content_snippet[:100]}...")
    
    # 保存结果
    detector.save_trending_cache(topics)


if __name__ == "__main__":
    main()