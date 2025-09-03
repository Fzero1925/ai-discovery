#!/usr/bin/env python3
"""
AI Discovery - 网站监控系统
Website monitoring system with Telegram notifications
"""

import asyncio
import aiohttp
import time
import json
import logging
import ssl
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import socket
from urllib.parse import urlparse
import subprocess

from telegram_bot import TelegramBot, create_bot_from_env

class WebsiteMonitor:
    """AI Discovery网站监控系统"""
    
    def __init__(self, telegram_bot: Optional[TelegramBot] = None):
        """
        初始化网站监控器
        Args:
            telegram_bot: Telegram Bot实例
        """
        self.telegram_bot = telegram_bot
        self.logger = self._setup_logger()
        self.monitoring_config = self._load_config()
        self.last_status = {}
        self.alert_cooldown = {}  # 防止重复报警
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("WebsiteMonitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(
                log_dir / f"monitoring_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
            
        return logger

    def _load_config(self) -> Dict:
        """加载监控配置"""
        default_config = {
            "websites": [
                {
                    "name": "AI Discovery (Production)",
                    "url": "https://ai-discovery.vercel.app",
                    "check_interval": 300,  # 5分钟
                    "timeout": 30,
                    "expected_status": [200, 301, 302],
                    "check_content": True,
                    "expected_content": ["AI Discovery", "AI工具"],
                    "check_ssl": True
                },
                {
                    "name": "AI Discovery (Development)", 
                    "url": "http://localhost:1315",
                    "check_interval": 600,  # 10分钟
                    "timeout": 10,
                    "expected_status": [200],
                    "check_content": True,
                    "expected_content": ["AI Discovery"],
                    "check_ssl": False
                }
            ],
            "alert_settings": {
                "cooldown_minutes": 15,  # 15分钟内不重复报警
                "max_retries": 3,
                "retry_interval": 60
            },
            "performance_thresholds": {
                "response_time_warning": 3000,  # 3秒
                "response_time_critical": 5000,  # 5秒
                "uptime_warning": 95.0,  # 95%
                "ssl_expiry_warning": 30  # 30天
            }
        }
        
        config_file = Path("monitoring_config.json")
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并用户配置和默认配置
                    default_config.update(user_config)
                    self.logger.info("加载用户监控配置成功")
            except Exception as e:
                self.logger.warning(f"加载用户配置失败，使用默认配置: {e}")
        
        return default_config

    async def check_website(self, site_config: Dict) -> Dict:
        """
        检查单个网站状态
        Args:
            site_config: 网站配置
        Returns:
            检查结果
        """
        start_time = time.time()
        site_name = site_config["name"]
        url = site_config["url"]
        
        self.logger.info(f"开始检查网站: {site_name} - {url}")
        
        result = {
            "name": site_name,
            "url": url,
            "timestamp": datetime.now(),
            "status": "unknown",
            "status_code": None,
            "response_time": None,
            "error": None,
            "ssl_info": None,
            "content_check": False,
            "metrics": {}
        }
        
        try:
            timeout = aiohttp.ClientTimeout(total=site_config.get("timeout", 30))
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, allow_redirects=True) as response:
                    end_time = time.time()
                    response_time = int((end_time - start_time) * 1000)  # 毫秒
                    
                    result.update({
                        "status_code": response.status,
                        "response_time": response_time,
                        "headers": dict(response.headers)
                    })
                    
                    # 检查状态码
                    expected_status = site_config.get("expected_status", [200])
                    if response.status in expected_status:
                        result["status"] = "online"
                    else:
                        result["status"] = "error"
                        result["error"] = f"意外状态码: {response.status}"
                    
                    # 检查内容
                    if site_config.get("check_content", False):
                        try:
                            content = await response.text()
                            expected_content = site_config.get("expected_content", [])
                            
                            if expected_content:
                                found_content = any(text in content for text in expected_content)
                                result["content_check"] = found_content
                                
                                if not found_content:
                                    result["status"] = "warning"
                                    result["error"] = "网站内容异常，未找到预期内容"
                            else:
                                result["content_check"] = len(content) > 100  # 至少有一些内容
                                
                        except Exception as e:
                            result["content_check"] = False
                            self.logger.warning(f"内容检查失败: {e}")
                    
                    # SSL检查
                    if site_config.get("check_ssl", False) and url.startswith("https"):
                        ssl_info = await self._check_ssl_expiry(url)
                        result["ssl_info"] = ssl_info
                        
                        if ssl_info and ssl_info.get("days_until_expiry", 0) < 30:
                            result["status"] = "warning"
                            result["error"] = f"SSL证书将在{ssl_info['days_until_expiry']}天后过期"
                    
                    # 性能指标
                    thresholds = self.monitoring_config.get("performance_thresholds", {})
                    if response_time > thresholds.get("response_time_critical", 5000):
                        result["status"] = "critical" if result["status"] == "online" else result["status"]
                        result["error"] = f"响应时间过长: {response_time}ms"
                    elif response_time > thresholds.get("response_time_warning", 3000):
                        result["status"] = "warning" if result["status"] == "online" else result["status"]
                        
                    result["metrics"] = self._calculate_metrics(result, site_config)
                    
        except asyncio.TimeoutError:
            result.update({
                "status": "timeout",
                "error": f"请求超时 (>{site_config.get('timeout', 30)}秒)"
            })
        except aiohttp.ClientError as e:
            result.update({
                "status": "error", 
                "error": f"连接错误: {str(e)}"
            })
        except Exception as e:
            result.update({
                "status": "error",
                "error": f"检查异常: {str(e)}"
            })
        
        self.logger.info(
            f"网站检查完成: {site_name} - 状态: {result['status']} - "
            f"响应时间: {result.get('response_time', 'N/A')}ms"
        )
        
        return result

    async def _check_ssl_expiry(self, url: str) -> Optional[Dict]:
        """
        检查SSL证书过期时间
        Args:
            url: 网站URL
        Returns:
            SSL证书信息
        """
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # 解析过期时间
                    expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (expiry_date - datetime.now()).days
                    
                    return {
                        "subject": dict(x[0] for x in cert.get('subject', [])),
                        "issuer": dict(x[0] for x in cert.get('issuer', [])),
                        "expiry_date": expiry_date.strftime('%Y-%m-%d'),
                        "days_until_expiry": days_until_expiry,
                        "valid": days_until_expiry > 0
                    }
                    
        except Exception as e:
            self.logger.warning(f"SSL检查失败 {url}: {e}")
            return None

    def _calculate_metrics(self, result: Dict, site_config: Dict) -> Dict:
        """
        计算性能指标
        Args:
            result: 检查结果
            site_config: 网站配置
        Returns:
            指标字典
        """
        metrics = {}
        
        # 响应时间等级
        response_time = result.get("response_time", 0)
        if response_time > 0:
            if response_time < 1000:
                metrics["response_grade"] = "优秀"
            elif response_time < 3000:
                metrics["response_grade"] = "良好"
            elif response_time < 5000:
                metrics["response_grade"] = "一般"
            else:
                metrics["response_grade"] = "较差"
        
        # 可用性状态
        status = result.get("status", "unknown")
        metrics["availability"] = "正常" if status in ["online", "warning"] else "异常"
        
        # SSL状态
        ssl_info = result.get("ssl_info")
        if ssl_info:
            days = ssl_info.get("days_until_expiry", 0)
            if days > 30:
                metrics["ssl_status"] = "安全"
            elif days > 7:
                metrics["ssl_status"] = "即将过期"
            else:
                metrics["ssl_status"] = "紧急续期"
        
        return metrics

    async def should_send_alert(self, site_name: str, current_status: str) -> bool:
        """
        判断是否应该发送警报
        Args:
            site_name: 网站名称
            current_status: 当前状态
        Returns:
            是否发送警报
        """
        # 检查冷却时间
        cooldown_key = f"{site_name}_{current_status}"
        cooldown_minutes = self.monitoring_config.get("alert_settings", {}).get("cooldown_minutes", 15)
        
        if cooldown_key in self.alert_cooldown:
            last_alert = self.alert_cooldown[cooldown_key]
            if datetime.now() - last_alert < timedelta(minutes=cooldown_minutes):
                return False
        
        # 检查状态变化
        last_status = self.last_status.get(site_name, "unknown")
        
        # 状态从正常变为异常，或从异常变为正常时发送警报
        should_alert = (
            (last_status in ["online", "unknown"] and current_status in ["error", "critical", "timeout"]) or
            (last_status in ["error", "critical", "timeout"] and current_status == "online") or
            (current_status == "warning" and last_status != "warning")
        )
        
        if should_alert:
            self.alert_cooldown[cooldown_key] = datetime.now()
        
        return should_alert

    async def send_status_notification(self, result: Dict):
        """
        发送状态通知
        Args:
            result: 检查结果
        """
        if not self.telegram_bot:
            return
            
        site_name = result["name"]
        current_status = result["status"]
        
        # 判断是否发送警报
        should_alert = await self.should_send_alert(site_name, current_status)
        
        if should_alert:
            # 格式化状态数据用于Telegram消息
            status_data = {
                "status": "online" if current_status in ["online", "warning"] else "offline",
                "url": result["url"],
                "response_time": result.get("response_time"),
                "status_code": result.get("status_code"),
                "metrics": result.get("metrics", {}),
                "error": result.get("error"),
                "ssl_info": result.get("ssl_info")
            }
            
            # 添加更多指标
            if result.get("ssl_info"):
                ssl_info = result["ssl_info"]
                status_data["metrics"]["ssl_expiry"] = f"{ssl_info.get('days_until_expiry', 'N/A')} 天"
            
            message = self.telegram_bot.format_website_status(status_data)
            await self.telegram_bot.send_message(message)
            
            self.logger.info(f"发送状态通知: {site_name} - {current_status}")
        
        # 更新最后状态
        self.last_status[site_name] = current_status

    async def run_monitoring_cycle(self):
        """执行一轮监控检查"""
        websites = self.monitoring_config.get("websites", [])
        
        self.logger.info(f"开始监控周期，检查 {len(websites)} 个网站")
        
        for site_config in websites:
            try:
                result = await self.check_website(site_config)
                await self.send_status_notification(result)
                
                # 保存检查结果到日志文件
                self._save_monitoring_result(result)
                
                # 短暂延迟，避免过快请求
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"监控异常 {site_config.get('name', 'Unknown')}: {e}")

    def _save_monitoring_result(self, result: Dict):
        """
        保存监控结果到文件
        Args:
            result: 检查结果
        """
        try:
            log_dir = Path("logs/monitoring")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"monitoring_{datetime.now().strftime('%Y%m%d')}.jsonl"
            
            # 创建可序列化的结果副本
            serializable_result = {
                "timestamp": result["timestamp"].isoformat(),
                "name": result["name"],
                "url": result["url"],
                "status": result["status"],
                "status_code": result.get("status_code"),
                "response_time": result.get("response_time"),
                "error": result.get("error"),
                "metrics": result.get("metrics", {})
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(serializable_result, ensure_ascii=False) + '\n')
                
        except Exception as e:
            self.logger.warning(f"保存监控结果失败: {e}")

    async def start_monitoring(self, continuous: bool = True):
        """
        启动监控系统
        Args:
            continuous: 是否持续监控
        """
        self.logger.info("AI Discovery 网站监控系统启动")
        
        if self.telegram_bot:
            # 发送启动通知
            startup_message = f"""
🚀 <b>AI Discovery 监控系统启动</b>

⏰ <b>启动时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌐 <b>监控网站:</b> {len(self.monitoring_config.get('websites', []))} 个
📊 <b>检查间隔:</b> 5-10分钟
🔔 <b>通知状态:</b> 已启用

💡 <b>监控项目:</b>
• 网站可用性检查
• 响应时间监控
• SSL证书监控
• 内容完整性验证

🤖 <b>AI Discovery</b> - 24/7 智能监控已就绪
            """
            
            await self.telegram_bot.send_message(startup_message.strip())
        
        try:
            while True:
                await self.run_monitoring_cycle()
                
                if not continuous:
                    break
                
                # 计算下次检查时间（使用最小检查间隔）
                min_interval = min(
                    site.get("check_interval", 300) 
                    for site in self.monitoring_config.get("websites", [])
                )
                
                self.logger.info(f"监控周期完成，{min_interval}秒后进行下次检查")
                await asyncio.sleep(min_interval)
                
        except KeyboardInterrupt:
            self.logger.info("监控系统被用户中断")
        except Exception as e:
            self.logger.error(f"监控系统异常: {e}")
            if self.telegram_bot:
                error_message = f"""
❌ <b>AI Discovery 监控系统异常</b>

⚠️ <b>错误信息:</b> {str(e)}
⏰ <b>发生时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 <b>系统将尝试自动重启</b>

🤖 <b>AI Discovery</b> - 监控系统警报
                """
                await self.telegram_bot.send_message(error_message.strip())
            raise

async def main():
    """主函数"""
    # 创建Telegram Bot
    telegram_bot = create_bot_from_env()
    
    if not telegram_bot:
        print("警告: 无法创建Telegram Bot，监控将在无通知模式下运行")
    else:
        # 测试Bot连接
        connection_test = telegram_bot.test_connection()
        if not connection_test.get("success"):
            print(f"警告: Telegram Bot连接失败: {connection_test.get('error')}")
            telegram_bot = None
    
    # 创建监控器
    monitor = WebsiteMonitor(telegram_bot)
    
    print("启动AI Discovery网站监控系统...")
    print("按 Ctrl+C 停止监控")
    
    try:
        await monitor.start_monitoring(continuous=True)
    except KeyboardInterrupt:
        print("\n监控系统已停止")

if __name__ == "__main__":
    asyncio.run(main())