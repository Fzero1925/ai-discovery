#!/usr/bin/env python3
"""
AI Discovery Keyword Analysis Telegram Notifier

Provides intelligent keyword analysis and business value notifications
for content generation activities.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re

@dataclass
class KeywordAnalysis:
    """Keyword analysis data structure"""
    primary_keyword: str
    search_volume: int
    competition_score: float  # 0-1, lower is better
    commercial_intent: float  # 0-1, higher is better
    cpc_estimate: float
    trend_score: float  # 0-1, higher is better
    monthly_revenue_estimate: float
    selection_reason: str
    alternative_keywords: List[Dict]

@dataclass  
class ContentGenerationReport:
    """Content generation report data"""
    tool_name: str
    article_title: str
    category: str
    keyword_analysis: KeywordAnalysis
    generation_timestamp: str
    article_word_count: int
    seo_score_estimate: float

class KeywordAnalysisNotifier:
    """
    Advanced keyword analysis and business intelligence notifier
    """
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        """Initialize the notifier"""
        self.bot_token = bot_token or os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('TELEGRAM_CHAT_ID') 
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        
        # Keyword analysis database (simulated API data)
        self.keyword_database = self._load_keyword_database()
    
    def _load_keyword_database(self) -> Dict:
        """Load keyword analysis database with commercial intelligence"""
        return {
            "chatgpt review": {
                "search_volume": 8200,
                "competition": 0.67,
                "commercial_intent": 0.94,
                "cpc": 2.15,
                "trend": 0.82,
                "related_keywords": [
                    {"keyword": "chatgpt vs claude", "volume": 3400, "cpc": 1.85},
                    {"keyword": "chatgpt pricing", "volume": 5100, "cpc": 2.45},
                    {"keyword": "best ai chatbot", "volume": 4200, "cpc": 1.95}
                ]
            },
            "claude ai guide": {
                "search_volume": 4600,
                "competition": 0.45,
                "commercial_intent": 0.89,
                "cpc": 1.95,
                "trend": 0.91,
                "related_keywords": [
                    {"keyword": "claude vs chatgpt", "volume": 3400, "cpc": 1.85},
                    {"keyword": "anthropic claude", "volume": 2800, "cpc": 1.75},
                    {"keyword": "claude ai features", "volume": 1900, "cpc": 1.65}
                ]
            },
            "midjourney tutorial": {
                "search_volume": 6800,
                "competition": 0.72,
                "commercial_intent": 0.87,
                "cpc": 2.35,
                "trend": 0.78,
                "related_keywords": [
                    {"keyword": "midjourney pricing", "volume": 2100, "cpc": 2.85},
                    {"keyword": "midjourney alternatives", "volume": 3200, "cpc": 2.15},
                    {"keyword": "ai art generator", "volume": 8900, "cpc": 1.95}
                ]
            },
            "dall-e 3 review": {
                "search_volume": 5400,
                "competition": 0.58,
                "commercial_intent": 0.91,
                "cpc": 2.25,
                "trend": 0.85,
                "related_keywords": [
                    {"keyword": "dall-e 3 vs midjourney", "volume": 2800, "cpc": 2.35},
                    {"keyword": "openai dall-e", "volume": 3600, "cpc": 2.05},
                    {"keyword": "best ai image generator", "volume": 4100, "cpc": 2.15}
                ]
            },
            "github copilot guide": {
                "search_volume": 3200,
                "competition": 0.52,
                "commercial_intent": 0.93,
                "cpc": 2.85,
                "trend": 0.88,
                "related_keywords": [
                    {"keyword": "github copilot pricing", "volume": 1400, "cpc": 3.15},
                    {"keyword": "copilot vs tabnine", "volume": 980, "cpc": 2.95},
                    {"keyword": "ai coding assistant", "volume": 2600, "cpc": 2.65}
                ]
            }
        }
    
    def analyze_keyword(self, keyword: str, tool_name: str, category: str) -> KeywordAnalysis:
        """Perform comprehensive keyword analysis"""
        
        # Normalize keyword for lookup
        keyword_key = keyword.lower()
        
        # Get keyword data (fallback to estimates if not in database)
        if keyword_key in self.keyword_database:
            data = self.keyword_database[keyword_key]
        else:
            # Generate estimates based on tool and category
            data = self._estimate_keyword_metrics(keyword, tool_name, category)
        
        # Calculate monthly revenue estimate
        monthly_revenue = self._calculate_revenue_estimate(
            data["search_volume"], 
            data["cpc"], 
            data["commercial_intent"]
        )
        
        # Generate selection reason
        selection_reason = self._generate_selection_reason(data, keyword, tool_name)
        
        return KeywordAnalysis(
            primary_keyword=keyword,
            search_volume=data["search_volume"],
            competition_score=data["competition"],
            commercial_intent=data["commercial_intent"],
            cpc_estimate=data["cpc"],
            trend_score=data["trend"],
            monthly_revenue_estimate=monthly_revenue,
            selection_reason=selection_reason,
            alternative_keywords=data.get("related_keywords", [])
        )
    
    def _estimate_keyword_metrics(self, keyword: str, tool_name: str, category: str) -> Dict:
        """Estimate keyword metrics for unknown keywords"""
        
        # Category-based estimates
        category_multipliers = {
            "content_creation": {"volume": 1.2, "cpc": 1.8, "intent": 0.85},
            "image_generation": {"volume": 1.0, "cpc": 2.1, "intent": 0.80},
            "code_assistance": {"volume": 0.8, "cpc": 2.5, "intent": 0.95},
            "productivity": {"volume": 1.1, "cpc": 1.9, "intent": 0.82}
        }
        
        base_volume = 2000 + len(tool_name) * 200
        mult = category_multipliers.get(category, {"volume": 1.0, "cpc": 2.0, "intent": 0.80})
        
        return {
            "search_volume": int(base_volume * mult["volume"]),
            "competition": 0.45 + (hash(keyword) % 30) / 100,  # 0.45-0.75
            "commercial_intent": mult["intent"],
            "cpc": mult["cpc"] + (hash(keyword) % 50) / 100,  # Add variance
            "trend": 0.75 + (hash(tool_name) % 20) / 100,  # 0.75-0.95
            "related_keywords": []
        }
    
    def _calculate_revenue_estimate(self, volume: int, cpc: float, intent: float) -> float:
        """Calculate estimated monthly revenue potential"""
        
        # Ensure volume is numeric
        if isinstance(volume, str):
            volume_match = re.search(r'(\d+)', volume.replace(',', ''))
            if volume_match:
                volume = int(volume_match.group(1))
                # Handle K and M suffixes
                if 'k' in volume.lower() or 'K' in volume:
                    volume *= 1000
                elif 'm' in volume.lower() or 'M' in volume:
                    volume *= 1000000
            else:
                volume = 500  # Default estimate
        elif not isinstance(volume, (int, float)):
            volume = 500
        
        # Assumptions for calculation
        organic_ctr = 0.03  # 3% organic CTR for target position
        conversion_rate = 0.15  # 15% click to monetization
        
        monthly_clicks = volume * organic_ctr
        revenue_per_click = cpc * intent * conversion_rate
        
        return monthly_clicks * revenue_per_click
    
    def _generate_selection_reason(self, data: Dict, keyword: str, tool_name: str) -> str:
        """Generate explanation for keyword selection"""
        
        reasons = []
        
        # Volume analysis
        if data["search_volume"] > 5000:
            reasons.append("high search volume")
        elif data["search_volume"] > 2000:
            reasons.append("moderate search volume")
        
        # Competition analysis  
        if data["competition"] < 0.5:
            reasons.append("low competition")
        elif data["competition"] < 0.7:
            reasons.append("manageable competition")
        
        # Commercial intent
        if data["commercial_intent"] > 0.9:
            reasons.append("excellent commercial intent")
        elif data["commercial_intent"] > 0.8:
            reasons.append("strong commercial intent")
        
        # Trend analysis
        if data["trend"] > 0.8:
            reasons.append("rising trend")
        
        return f"Selected for {', '.join(reasons)}"
    
    def send_content_generation_notification(self, report: ContentGenerationReport) -> bool:
        """Send comprehensive content generation notification"""
        
        try:
            # Format the advanced notification message
            message = self._format_advanced_notification(report)
            
            # Send via Telegram
            response = requests.post(
                f"{self.api_base}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("SUCCESS: Keyword analysis notification sent")
                return True
            else:
                print(f"ERROR: Telegram API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to send notification: {e}")
            return False
    
    def _format_advanced_notification(self, report: ContentGenerationReport) -> str:
        """Format comprehensive business intelligence notification"""
        
        ka = report.keyword_analysis
        
        # Generate trend indicator
        trend_emoji = "📈" if ka.trend_score > 0.8 else "📊" if ka.trend_score > 0.6 else "📉"
        
        # Competition difficulty
        comp_emoji = "🟢" if ka.competition_score < 0.5 else "🟡" if ka.competition_score < 0.7 else "🔴"
        
        message = f"""🎯 <b>AI Discovery Content Generated</b>

📝 <b>New Article:</b> {report.article_title}
🔧 <b>AI Tool:</b> {report.tool_name}
📂 <b>Category:</b> {report.category.replace('_', ' ').title()}
📊 <b>Word Count:</b> {report.article_word_count:,}

🔍 <b>KEYWORD ANALYSIS</b>
━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Primary Keyword:</b> "<code>{ka.primary_keyword}</code>"
📈 <b>Search Volume:</b> {ka.search_volume:,}/month
💰 <b>CPC Estimate:</b> ${ka.cpc_estimate:.2f}
{comp_emoji} <b>Competition:</b> {ka.competition_score:.2f}/1.0
🛒 <b>Commercial Intent:</b> {ka.commercial_intent:.1%}
{trend_emoji} <b>Trend Score:</b> {ka.trend_score:.1%}

💡 <b>SELECTION REASONING</b>
━━━━━━━━━━━━━━━━━━━━━
{ka.selection_reason}

💵 <b>REVENUE POTENTIAL</b>
━━━━━━━━━━━━━━━━━━━━━
💰 <b>Estimated Monthly Revenue:</b> ${ka.monthly_revenue_estimate:.0f}
📊 <b>Revenue per 1K Views:</b> ${(ka.monthly_revenue_estimate / ka.search_volume * 1000):.2f}
🎯 <b>ROI Confidence:</b> {"High" if ka.commercial_intent > 0.9 else "Medium" if ka.commercial_intent > 0.8 else "Standard"}"""

        # Add alternative keywords section
        if ka.alternative_keywords:
            message += f"\n\n🔄 <b>ALTERNATIVE KEYWORDS ANALYZED</b>\n━━━━━━━━━━━━━━━━━━━━━"
            
            for i, alt in enumerate(ka.alternative_keywords[:3], 1):
                revenue_est = self._calculate_revenue_estimate(alt["volume"], alt["cpc"], 0.85)
                message += f"\n{i}. \"<code>{alt['keyword']}</code>\" - {alt['volume']:,}/mo, ${alt['cpc']:.2f} CPC, ~${revenue_est:.0f}/mo"
        
        # Add strategic insights
        message += f"\n\n🧠 <b>STRATEGIC INSIGHTS</b>\n━━━━━━━━━━━━━━━━━━━━━"
        
        if ka.competition_score < 0.5:
            message += "\n• 🎯 <b>Quick Win Opportunity</b> - Low competition allows fast ranking"
        
        if ka.commercial_intent > 0.9:
            message += "\n• 💎 <b>High-Value Content</b> - Excellent monetization potential"
            
        if ka.trend_score > 0.8:
            message += "\n• 🚀 <b>Trending Topic</b> - Capitalize on growing interest"
        
        # Performance expectations
        ranking_time = "2-4 weeks" if ka.competition_score < 0.5 else "1-3 months" if ka.competition_score < 0.7 else "3-6 months"
        message += f"\n• ⏱️ <b>Expected Ranking Time:</b> {ranking_time}"
        
        message += f"\n\n🕐 <b>Generated:</b> {report.generation_timestamp}"
        message += f"\n🌐 <b>Website:</b> ai-discovery-nu.vercel.app"
        
        return message
    
    def notify_keyword_research_complete(self, total_keywords: int, selected_keyword: str, 
                                       category: str, estimated_value: float) -> bool:
        """Send keyword research completion notification"""
        
        message = f"""🔬 <b>Keyword Research Complete</b>

📊 <b>Analysis Summary:</b>
• Analyzed {total_keywords} potential keywords
• Selected: "<code>{selected_keyword}</code>"
• Category: {category.replace('_', ' ').title()}
• Est. Monthly Value: ${estimated_value:.0f}

🎯 Next: Content generation starting...
"""
        
        try:
            response = requests.post(
                f"{self.api_base}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                },
                timeout=10
            )
            return response.status_code == 200
        except:
            return False


def create_sample_report() -> ContentGenerationReport:
    """Create a sample report for testing"""
    
    notifier = KeywordAnalysisNotifier()
    keyword_analysis = notifier.analyze_keyword("chatgpt review", "ChatGPT", "content_creation")
    
    return ContentGenerationReport(
        tool_name="ChatGPT",
        article_title="ChatGPT Complete Guide: Features, Pricing & Best Use Cases 2024",
        category="content_creation",
        keyword_analysis=keyword_analysis,
        generation_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        article_word_count=3250,
        seo_score_estimate=8.7
    )


def main():
    """Test the notification system"""
    
    notifier = KeywordAnalysisNotifier()
    
    if not notifier.bot_token or not notifier.chat_id:
        print("ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return
    
    # Create and send test report
    report = create_sample_report()
    success = notifier.send_content_generation_notification(report)
    
    if success:
        print("SUCCESS: Test notification sent!")
    else:
        print("ERROR: Failed to send test notification")


if __name__ == "__main__":
    main()