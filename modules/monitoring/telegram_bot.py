#!/usr/bin/env python3
"""
AI Discovery - Telegram Bot 监控通知系统
Enhanced Telegram Bot for website monitoring and notifications
"""

import os
import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from pathlib import Path

class TelegramBot:
    """AI Discovery Telegram监控机器人"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        初始化Telegram Bot
        Args:
            bot_token: Telegram Bot Token
            chat_id: 目标聊天ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_base = f"https://api.telegram.org/bot{bot_token}"
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("TelegramBot")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger

    async def send_message(self, message: str, parse_mode: str = "HTML") -> Dict:
        """
        发送消息到Telegram
        Args:
            message: 消息内容
            parse_mode: 解析模式 (HTML/Markdown)
        Returns:
            API响应结果
        """
        url = f"{self.api_base}/sendMessage"
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    result = await response.json()
                    
                    if result.get("ok"):
                        self.logger.info(f"消息发送成功: {message[:50]}...")
                        return result
                    else:
                        self.logger.error(f"消息发送失败: {result.get('description', '未知错误')}")
                        return result
                        
        except Exception as e:
            self.logger.error(f"发送消息异常: {str(e)}")
            return {"ok": False, "error": str(e)}

    def send_sync_message(self, message: str) -> Dict:
        """
        同步发送消息 (用于非异步环境)
        Args:
            message: 消息内容
        Returns:
            API响应结果
        """
        url = f"{self.api_base}/sendMessage"
        
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                self.logger.info(f"消息发送成功: {message[:50]}...")
                return result
            else:
                self.logger.error(f"消息发送失败: {result.get('description', '未知错误')}")
                return result
                
        except Exception as e:
            self.logger.error(f"发送消息异常: {str(e)}")
            return {"ok": False, "error": str(e)}

    def format_website_status(self, status_data: Dict) -> str:
        """
        格式化网站状态消息
        Args:
            status_data: 网站状态数据
        Returns:
            格式化的HTML消息
        """
        status_icon = "🟢" if status_data.get("status") == "online" else "🔴"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🤖 <b>AI Discovery 网站状态报告</b>

{status_icon} <b>状态:</b> {status_data.get("status", "未知").upper()}
⏰ <b>检查时间:</b> {timestamp}
🌐 <b>网站URL:</b> {status_data.get("url", "N/A")}
⚡ <b>响应时间:</b> {status_data.get("response_time", "N/A")}ms
📊 <b>状态码:</b> {status_data.get("status_code", "N/A")}

{self._format_additional_metrics(status_data.get("metrics", {}))}

💡 <b>AI Discovery</b> - 智能AI工具发现平台
        """
        return message.strip()

    def format_build_notification(self, build_data: Dict) -> str:
        """
        格式化构建通知消息
        Args:
            build_data: 构建数据
        Returns:
            格式化的HTML消息
        """
        status_icon = "✅" if build_data.get("success") else "❌"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
🏗️ <b>AI Discovery 构建通知</b>

{status_icon} <b>构建状态:</b> {"成功" if build_data.get("success") else "失败"}
⏰ <b>构建时间:</b> {timestamp}
📦 <b>构建类型:</b> {build_data.get("build_type", "自动构建")}
⚡ <b>构建时长:</b> {build_data.get("duration", "N/A")}秒

📊 <b>构建统计:</b>
• 页面数: {build_data.get("pages", 0)}
• 文章数: {build_data.get("articles", 0)} 
• 文件大小: {build_data.get("size", "N/A")}

{self._format_build_details(build_data)}

🚀 <b>AI Discovery</b> - 持续部署成功
        """
        return message.strip()

    def format_seo_report(self, seo_data: Dict) -> str:
        """
        格式化SEO报告消息
        Args:
            seo_data: SEO数据
        Returns:
            格式化的HTML消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
📈 <b>AI Discovery SEO报告</b>

⏰ <b>报告时间:</b> {timestamp}
🎯 <b>监控周期:</b> {seo_data.get("period", "24小时")}

📊 <b>关键指标:</b>
• 收录页面: {seo_data.get("indexed_pages", "检测中")}
• 平均排名: {seo_data.get("avg_ranking", "检测中")}
• 有机流量: {seo_data.get("organic_traffic", "检测中")}
• 点击率: {seo_data.get("ctr", "检测中")}%

🔍 <b>热门关键词:</b>
{self._format_keywords(seo_data.get("keywords", []))}

📋 <b>建议优化:</b>
{self._format_seo_suggestions(seo_data.get("suggestions", []))}

🎯 <b>AI Discovery</b> - SEO持续优化中
        """
        return message.strip()

    def format_error_alert(self, error_data: Dict) -> str:
        """
        格式化错误警报消息
        Args:
            error_data: 错误数据
        Returns:
            格式化的HTML消息
        """
        severity_icons = {
            "critical": "🚨",
            "error": "❌", 
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        severity = error_data.get("severity", "error").lower()
        icon = severity_icons.get(severity, "❌")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
{icon} <b>AI Discovery 错误警报</b>

⚠️ <b>严重级别:</b> {severity.upper()}
⏰ <b>发生时间:</b> {timestamp}
🔧 <b>错误类型:</b> {error_data.get("type", "未知错误")}

📝 <b>错误详情:</b>
{error_data.get("message", "无详细信息")}

🔍 <b>错误位置:</b>
{error_data.get("location", "未知位置")}

📊 <b>系统状态:</b>
• CPU使用率: {error_data.get("cpu_usage", "N/A")}%
• 内存使用: {error_data.get("memory_usage", "N/A")}%
• 磁盘空间: {error_data.get("disk_usage", "N/A")}%

🛠️ <b>建议操作:</b>
{self._format_error_suggestions(error_data.get("suggestions", []))}

⚡ <b>AI Discovery</b> - 系统监控警报
        """
        return message.strip()

    def format_content_update(self, content_data: Dict) -> str:
        """
        格式化内容更新通知
        Args:
            content_data: 内容更新数据
        Returns:
            格式化的HTML消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
📝 <b>AI Discovery 内容更新</b>

⏰ <b>更新时间:</b> {timestamp}
🎯 <b>更新类型:</b> {content_data.get("update_type", "自动更新")}

📊 <b>更新统计:</b>
• 新增文章: {content_data.get("new_articles", 0)} 篇
• 更新文章: {content_data.get("updated_articles", 0)} 篇
• 总字数: {content_data.get("total_words", 0):,} 字

✨ <b>最新内容:</b>
{self._format_article_list(content_data.get("articles", []))}

📈 <b>质量指标:</b>
• 平均SEO得分: {content_data.get("avg_seo_score", 0)}/100
• 平均可读性: {content_data.get("avg_readability", 0)}/100
• 原创性评分: {content_data.get("originality", 0)}%

🤖 <b>AI Discovery</b> - 内容持续更新中
        """
        return message.strip()

    def _format_additional_metrics(self, metrics: Dict) -> str:
        """格式化附加指标"""
        if not metrics:
            return ""
            
        lines = ["📈 <b>性能指标:</b>"]
        
        if "uptime" in metrics:
            lines.append(f"• 运行时间: {metrics['uptime']}")
        if "ssl_expiry" in metrics:
            lines.append(f"• SSL到期: {metrics['ssl_expiry']}")
        if "page_load" in metrics:
            lines.append(f"• 页面加载: {metrics['page_load']}ms")
            
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_build_details(self, build_data: Dict) -> str:
        """格式化构建详情"""
        details = []
        
        if build_data.get("commit_hash"):
            details.append(f"🔗 <b>提交:</b> {build_data['commit_hash'][:8]}")
        if build_data.get("branch"):
            details.append(f"🌿 <b>分支:</b> {build_data['branch']}")
        if build_data.get("author"):
            details.append(f"👤 <b>作者:</b> {build_data['author']}")
            
        return "\n".join(details) if details else ""

    def _format_keywords(self, keywords: List[Dict]) -> str:
        """格式化关键词列表"""
        if not keywords:
            return "• 暂无数据"
            
        lines = []
        for i, kw in enumerate(keywords[:5], 1):  # 只显示前5个
            position = kw.get("position", "N/A")
            clicks = kw.get("clicks", 0)
            lines.append(f"• #{position} - {kw.get('query', 'N/A')} ({clicks} 点击)")
            
        return "\n".join(lines)

    def _format_seo_suggestions(self, suggestions: List[str]) -> str:
        """格式化SEO建议"""
        if not suggestions:
            return "• 当前优化良好，继续保持"
            
        return "\n".join([f"• {suggestion}" for suggestion in suggestions[:3]])

    def _format_error_suggestions(self, suggestions: List[str]) -> str:
        """格式化错误建议"""
        if not suggestions:
            return "• 请联系技术支持"
            
        return "\n".join([f"• {suggestion}" for suggestion in suggestions])

    def _format_article_list(self, articles: List[Dict]) -> str:
        """格式化文章列表"""
        if not articles:
            return "• 暂无新内容"
            
        lines = []
        for article in articles[:3]:  # 只显示前3篇
            title = article.get("title", "未知标题")[:50]
            words = article.get("word_count", 0)
            lines.append(f"• {title} ({words} 字)")
            
        return "\n".join(lines)

    def test_connection(self) -> Dict:
        """
        测试Telegram Bot连接
        Returns:
            测试结果
        """
        url = f"{self.api_base}/getMe"
        
        try:
            response = requests.get(url, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                bot_info = result.get("result", {})
                self.logger.info(f"Bot连接成功: {bot_info.get('first_name', 'Unknown Bot')}")
                return {
                    "success": True,
                    "bot_name": bot_info.get("first_name"),
                    "username": bot_info.get("username"),
                    "can_read_all_group_messages": bot_info.get("can_read_all_group_messages")
                }
            else:
                self.logger.error(f"Bot连接失败: {result.get('description', '未知错误')}")
                return {"success": False, "error": result.get('description')}
                
        except Exception as e:
            self.logger.error(f"测试连接异常: {str(e)}")
            return {"success": False, "error": str(e)}

def create_bot_from_env() -> Optional[TelegramBot]:
    """
    从环境变量创建Bot实例
    Returns:
        TelegramBot实例或None
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token:
        print("错误: 未找到TELEGRAM_BOT_TOKEN环境变量")
        return None
        
    if not chat_id:
        print("错误: 未找到TELEGRAM_CHAT_ID环境变量")
        return None
        
    return TelegramBot(bot_token, chat_id)

async def main():
    """测试主函数"""
    # 从环境变量或配置文件创建Bot
    bot = create_bot_from_env()
    
    if not bot:
        print("无法创建Telegram Bot，请检查环境变量配置")
        return
    
    # 测试连接
    connection_result = bot.test_connection()
    print(f"连接测试结果: {connection_result}")
    
    if connection_result.get("success"):
        # 发送测试消息
        test_message = """
🤖 <b>AI Discovery 监控系统启动</b>

✅ Telegram Bot 连接成功
⏰ 启动时间: {timestamp}
🌐 网站监控: 已启用
📊 数据收集: 运行中

🚀 AI Discovery - 智能监控系统已就绪
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        result = await bot.send_message(test_message)
        print(f"测试消息发送结果: {result.get('ok', False)}")

if __name__ == "__main__":
    asyncio.run(main())