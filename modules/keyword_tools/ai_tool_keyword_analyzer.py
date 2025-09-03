"""
AI Tools Keyword Analyzer

Specialized keyword analysis system for AI tools and productivity software.
Uses Google Trends data to identify trending AI tools and related search queries.
"""

import json
import os
import random
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import pandas as pd
from pytrends.request import TrendReq
import requests
from pathlib import Path


@dataclass
class AIToolKeyword:
    """Container for AI tool keyword data"""
    keyword: str
    category: str
    trend_score: int
    related_queries: List[str]
    competition_level: str
    search_volume: str
    last_updated: str


class AIToolKeywordAnalyzer:
    """
    Analyzes trending AI tools and generates keyword insights
    for content creation targeting AI enthusiasts and professionals.
    """
    
    def __init__(self, cache_dir: str = "data"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize pytrends with random location
        self.pytrends = TrendReq(
            hl='en-US', 
            tz=360,
            retries=3,
            backoff_factor=0.5,
            requests_args={'verify': False}
        )
        
        # AI tool categories and seed keywords
        self.ai_tool_categories = {
            "content_creation": [
                "ChatGPT", "Claude AI", "Jasper AI", "Copy.ai", "Writesonic",
                "AI writing assistant", "content generator", "AI copywriting"
            ],
            "image_generation": [
                "Midjourney", "DALL-E", "Stable Diffusion", "Adobe Firefly",
                "AI image generator", "text to image", "AI art generator"
            ],
            "code_assistance": [
                "GitHub Copilot", "CodeWhisperer", "Tabnine", "Codeium",
                "AI coding assistant", "code completion", "programming AI"
            ],
            "productivity": [
                "Notion AI", "Todoist AI", "Zapier AI", "Calendly AI",
                "AI productivity tools", "task automation", "workflow AI"
            ],
            "data_analysis": [
                "DataRobot", "H2O.ai", "Tableau AI", "Power BI AI",
                "AI analytics", "data visualization AI", "business intelligence AI"
            ]
        }
        
        # Long-tail keyword patterns for AI tools
        self.keyword_patterns = [
            "{tool} review", "{tool} vs", "best {category} tools",
            "{tool} pricing", "how to use {tool}", "{tool} alternatives",
            "{tool} tutorial", "{tool} features", "is {tool} worth it",
            "{category} AI tools 2025", "free {category} AI", "{tool} comparison"
        ]
    
    def get_trending_ai_keywords(self, limit: int = 20) -> List[AIToolKeyword]:
        """
        Get currently trending AI tool keywords from Google Trends
        """
        trending_keywords = []
        
        for category, seed_keywords in self.ai_tool_categories.items():
            try:
                # Analyze trend for each seed keyword
                sample_keywords = random.sample(seed_keywords, min(3, len(seed_keywords)))
                
                for keyword in sample_keywords:
                    # Get trend data
                    self.pytrends.build_payload([keyword], timeframe='today 3-m')
                    
                    # Get interest over time
                    interest_data = self.pytrends.interest_over_time()
                    if not interest_data.empty:
                        trend_score = int(interest_data[keyword].mean())
                    else:
                        trend_score = 0
                    
                    # Get related queries
                    related_queries = self._get_related_queries(keyword)
                    
                    # Create keyword object
                    ai_keyword = AIToolKeyword(
                        keyword=keyword,
                        category=category,
                        trend_score=trend_score,
                        related_queries=related_queries,
                        competition_level=self._estimate_competition(trend_score),
                        search_volume=self._estimate_search_volume(trend_score),
                        last_updated=datetime.now().isoformat()
                    )
                    
                    trending_keywords.append(ai_keyword)
                    
                    # Rate limiting
                    time.sleep(random.uniform(2, 5))
                    
            except Exception as e:
                print(f"Error analyzing category {category}: {e}")
                continue
        
        # Sort by trend score and return top results
        trending_keywords.sort(key=lambda x: x.trend_score, reverse=True)
        return trending_keywords[:limit]
    
    def _get_related_queries(self, keyword: str) -> List[str]:
        """Get related search queries for a keyword"""
        try:
            self.pytrends.build_payload([keyword], timeframe='today 3-m')
            related_df = self.pytrends.related_queries()
            
            if keyword in related_df and related_df[keyword]['top'] is not None:
                return related_df[keyword]['top']['query'].tolist()[:10]
        except:
            pass
        
        return []
    
    def _estimate_competition(self, trend_score: int) -> str:
        """Estimate keyword competition level"""
        if trend_score >= 70:
            return "High"
        elif trend_score >= 40:
            return "Medium"
        else:
            return "Low"
    
    def _estimate_search_volume(self, trend_score: int) -> str:
        """Estimate search volume category"""
        if trend_score >= 80:
            return "10K-100K"
        elif trend_score >= 50:
            return "1K-10K"
        elif trend_score >= 20:
            return "100-1K"
        else:
            return "10-100"
    
    def generate_content_keywords(self, primary_keyword: str, category: str) -> List[str]:
        """
        Generate content-focused keywords around a primary AI tool
        """
        content_keywords = []
        
        # Apply keyword patterns
        for pattern in self.keyword_patterns:
            if "{tool}" in pattern:
                keyword = pattern.replace("{tool}", primary_keyword)
            elif "{category}" in pattern:
                keyword = pattern.replace("{category}", category.replace("_", " "))
            else:
                keyword = pattern
            
            content_keywords.append(keyword)
        
        # Add AI-specific modifiers
        ai_modifiers = [
            f"{primary_keyword} AI features",
            f"{primary_keyword} machine learning",
            f"{primary_keyword} automation",
            f"{primary_keyword} artificial intelligence",
            f"AI-powered {primary_keyword}",
            f"{primary_keyword} for beginners",
            f"{primary_keyword} professional use"
        ]
        
        content_keywords.extend(ai_modifiers)
        return content_keywords
    
    def save_analysis_cache(self, keywords: List[AIToolKeyword], filename: str = "ai_tool_keywords_cache.json"):
        """Save keyword analysis to cache file"""
        cache_file = self.cache_dir / filename
        
        # Convert to serializable format
        cache_data = {
            "generated_at": datetime.now().isoformat(),
            "keywords": [
                {
                    "keyword": kw.keyword,
                    "category": kw.category,
                    "trend_score": kw.trend_score,
                    "related_queries": kw.related_queries,
                    "competition_level": kw.competition_level,
                    "search_volume": kw.search_volume,
                    "last_updated": kw.last_updated
                }
                for kw in keywords
            ]
        }
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=2, ensure_ascii=False)
    
    def load_analysis_cache(self, filename: str = "ai_tool_keywords_cache.json") -> Optional[List[AIToolKeyword]]:
        """Load keyword analysis from cache file"""
        cache_file = self.cache_dir / filename
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache is recent (less than 24 hours)
            generated_time = datetime.fromisoformat(cache_data["generated_at"])
            if datetime.now() - generated_time > timedelta(hours=24):
                return None
            
            # Convert back to AIToolKeyword objects
            keywords = [
                AIToolKeyword(**kw_data)
                for kw_data in cache_data["keywords"]
            ]
            
            return keywords
            
        except Exception as e:
            print(f"Error loading cache: {e}")
            return None
    
    def get_daily_ai_keywords(self) -> List[AIToolKeyword]:
        """
        Get daily AI keywords - checks cache first, then generates if needed
        """
        # Try to load from cache
        cached_keywords = self.load_analysis_cache()
        if cached_keywords:
            return cached_keywords
        
        # Generate new analysis
        keywords = self.get_trending_ai_keywords(limit=15)
        
        # Save to cache
        self.save_analysis_cache(keywords)
        
        return keywords


def main():
    """Test the AI tool keyword analyzer"""
    analyzer = AIToolKeywordAnalyzer()
    
    print("🔍 Analyzing trending AI tools...")
    keywords = analyzer.get_daily_ai_keywords()
    
    print(f"\n📊 Found {len(keywords)} trending AI tool keywords:")
    for i, keyword in enumerate(keywords[:10], 1):
        print(f"{i}. {keyword.keyword} ({keyword.category})")
        print(f"   Trend Score: {keyword.trend_score}")
        print(f"   Competition: {keyword.competition_level}")
        print(f"   Est. Volume: {keyword.search_volume}")
        print(f"   Related: {', '.join(keyword.related_queries[:3])}")
        print()


if __name__ == "__main__":
    main()