#!/usr/bin/env python3
"""
AI Discovery - 监控系统启动器
Integrated monitoring system launcher with Telegram notifications
"""

import asyncio
import logging
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json

# 添加模块路径
sys.path.append(str(Path(__file__).parent))

from telegram_bot import TelegramBot, create_bot_from_env
from website_monitor import WebsiteMonitor
from performance_monitor import PerformanceMonitor

class MonitoringLauncher:
    """监控系统集成启动器"""
    
    def __init__(self):
        """初始化监控启动器"""
        self.logger = self._setup_logger()
        self.telegram_bot = None
        self.monitors = {}
        self.running = False
        self.tasks = []
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("MonitoringLauncher")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # 确保日志目录存在
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            file_handler = logging.FileHandler(
                log_dir / f"monitoring_launcher_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
            
        return logger

    def _setup_signal_handlers(self):
        """设置信号处理器"""
        def signal_handler(signum, frame):
            self.logger.info(f"接收到信号 {signum}，正在关闭监控系统...")
            self.stop_monitoring()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    async def initialize_telegram_bot(self) -> bool:
        """
        初始化Telegram Bot
        Returns:
            初始化是否成功
        """
        try:
            self.telegram_bot = create_bot_from_env()
            
            if not self.telegram_bot:
                self.logger.warning("未配置Telegram Bot，监控将在无通知模式下运行")
                return False
            
            # 测试连接
            connection_result = self.telegram_bot.test_connection()
            
            if connection_result.get("success"):
                bot_name = connection_result.get("bot_name", "Unknown Bot")
                self.logger.info(f"Telegram Bot连接成功: {bot_name}")
                
                # 发送启动通知
                await self.send_startup_notification()
                return True
            else:
                error = connection_result.get("error", "未知错误")
                self.logger.error(f"Telegram Bot连接失败: {error}")
                return False
                
        except Exception as e:
            self.logger.error(f"初始化Telegram Bot异常: {e}")
            return False

    async def send_startup_notification(self):
        """发送监控系统启动通知"""
        if not self.telegram_bot:
            return
        
        startup_message = f"""
🚀 <b>AI Discovery 集成监控系统启动</b>

⏰ <b>启动时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🤖 <b>Bot状态:</b> 已连接并正常工作

🛡️ <b>监控模块:</b>
• 🌐 网站状态监控 (5分钟间隔)
• ⚡ 性能指标监控 (5分钟间隔)  
• 📊 系统资源监控 (实时)
• 🔔 智能警报系统 (即时)

📈 <b>监控范围:</b>
• 网站可用性和响应时间
• 服务器CPU、内存、磁盘使用率
• Hugo构建性能和页面统计
• SSL证书有效期检查

⚙️ <b>警报设置:</b>
• CPU > 80% (警告) / 90% (严重)
• 内存 > 85% (警告) / 95% (严重)
• 响应时间 > 2秒 (警告) / 5秒 (严重)

💡 监控系统将24/7运行，异常情况会立即通知您

🚀 <b>AI Discovery</b> - 智能监控系统已就绪
        """
        
        await self.telegram_bot.send_message(startup_message.strip())

    async def create_monitors(self):
        """创建监控实例"""
        try:
            # 创建网站监控器
            self.monitors["website"] = WebsiteMonitor(self.telegram_bot)
            self.logger.info("网站监控器创建成功")
            
            # 创建性能监控器
            self.monitors["performance"] = PerformanceMonitor(self.telegram_bot)
            self.logger.info("性能监控器创建成功")
            
            self.logger.info(f"成功创建 {len(self.monitors)} 个监控器")
            
        except Exception as e:
            self.logger.error(f"创建监控器异常: {e}")
            raise

    async def start_monitoring_tasks(self):
        """启动所有监控任务"""
        self.running = True
        
        try:
            # 启动网站监控任务
            if "website" in self.monitors:
                website_task = asyncio.create_task(
                    self.monitors["website"].start_monitoring(continuous=True)
                )
                self.tasks.append(website_task)
                self.logger.info("网站监控任务已启动")
            
            # 启动性能监控任务
            if "performance" in self.monitors:
                performance_task = asyncio.create_task(
                    self.monitors["performance"].start_monitoring(report_interval=3600*6)  # 6小时报告一次
                )
                self.tasks.append(performance_task)
                self.logger.info("性能监控任务已启动")
            
            # 启动健康检查任务
            health_task = asyncio.create_task(self.health_check_loop())
            self.tasks.append(health_task)
            self.logger.info("健康检查任务已启动")
            
            self.logger.info(f"总共启动 {len(self.tasks)} 个监控任务")
            
        except Exception as e:
            self.logger.error(f"启动监控任务异常: {e}")
            raise

    async def health_check_loop(self):
        """健康检查循环"""
        self.logger.info("健康检查任务启动")
        
        while self.running:
            try:
                # 检查所有任务状态
                active_tasks = [task for task in self.tasks if not task.done()]
                completed_tasks = [task for task in self.tasks if task.done()]
                
                if completed_tasks:
                    self.logger.warning(f"发现 {len(completed_tasks)} 个已完成的任务")
                    
                    # 检查是否有异常完成的任务
                    for task in completed_tasks:
                        if task.exception():
                            exception = task.exception()
                            self.logger.error(f"监控任务异常完成: {exception}")
                            
                            if self.telegram_bot:
                                error_message = f"""
❌ <b>AI Discovery 监控任务异常</b>

⚠️ <b>任务异常:</b> 监控任务意外停止
📝 <b>异常信息:</b> {str(exception)}
⏰ <b>发生时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 <b>系统将尝试重启监控任务</b>

🤖 <b>AI Discovery</b> - 监控系统警报
                                """
                                await self.telegram_bot.send_message(error_message.strip())
                
                # 记录健康状态
                self.logger.info(f"健康检查: {len(active_tasks)} 个任务运行中")
                
                # 等待下次检查
                await asyncio.sleep(600)  # 10分钟检查一次
                
            except Exception as e:
                self.logger.error(f"健康检查异常: {e}")
                await asyncio.sleep(60)  # 异常时1分钟后重试

    def stop_monitoring(self):
        """停止监控系统"""
        self.logger.info("正在停止监控系统...")
        self.running = False
        
        # 取消所有任务
        for task in self.tasks:
            if not task.done():
                task.cancel()
                self.logger.info(f"取消任务: {task.get_name() if hasattr(task, 'get_name') else 'Unknown'}")

    async def send_shutdown_notification(self):
        """发送关闭通知"""
        if self.telegram_bot:
            shutdown_message = f"""
🔴 <b>AI Discovery 监控系统关闭</b>

⏰ <b>关闭时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 <b>运行统计:</b>
• 监控器数量: {len(self.monitors)}
• 运行任务数: {len(self.tasks)}

💡 监控系统已安全关闭，所有任务已停止

🤖 <b>AI Discovery</b> - 监控系统已下线
            """
            
            await self.telegram_bot.send_message(shutdown_message.strip())

    async def run(self):
        """运行监控系统"""
        self.logger.info("AI Discovery 集成监控系统启动中...")
        
        try:
            # 设置信号处理器
            self._setup_signal_handlers()
            
            # 初始化Telegram Bot
            await self.initialize_telegram_bot()
            
            # 创建监控器
            await self.create_monitors()
            
            # 启动监控任务
            await self.start_monitoring_tasks()
            
            self.logger.info("监控系统启动完成，开始监控...")
            print("\n" + "="*60)
            print("🚀 AI Discovery 监控系统已启动")
            print("📊 实时监控网站性能和系统状态")
            print("🔔 异常情况将通过Telegram通知")
            print("按 Ctrl+C 停止监控系统")
            print("="*60 + "\n")
            
            # 等待所有任务完成
            await asyncio.gather(*self.tasks, return_exceptions=True)
            
        except KeyboardInterrupt:
            self.logger.info("用户中断监控系统")
        except Exception as e:
            self.logger.error(f"监控系统运行异常: {e}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """清理资源"""
        self.logger.info("清理监控系统资源...")
        
        # 发送关闭通知
        await self.send_shutdown_notification()
        
        # 停止监控
        self.stop_monitoring()
        
        # 等待所有任务取消
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        self.logger.info("监控系统已完全关闭")

def create_env_template():
    """创建环境变量模板文件"""
    env_template = """# AI Discovery Monitoring System Configuration
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Monitoring Configuration  
MONITORING_WEBSITE_URL=https://ai-discovery.vercel.app
MONITORING_LOCAL_URL=http://localhost:1315
MONITORING_INTERVAL=300

# Alert Thresholds
CPU_WARNING_THRESHOLD=80
CPU_CRITICAL_THRESHOLD=90
MEMORY_WARNING_THRESHOLD=85
MEMORY_CRITICAL_THRESHOLD=95
RESPONSE_TIME_WARNING=2000
RESPONSE_TIME_CRITICAL=5000

# Report Settings
DAILY_REPORT_HOUR=9
WEEKLY_REPORT_DAY=1
"""
    
    env_file = Path(".env.example")
    if not env_file.exists():
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_template.strip())
        print(f"创建环境变量模板: {env_file}")

def create_monitoring_config():
    """创建监控配置文件"""
    config = {
        "websites": [
            {
                "name": "AI Discovery (Production)",
                "url": "https://ai-discovery.vercel.app",
                "check_interval": 300,
                "timeout": 30,
                "expected_status": [200, 301, 302],
                "check_content": True,
                "expected_content": ["AI Discovery", "AI工具"],
                "check_ssl": True
            },
            {
                "name": "AI Discovery (Development)",
                "url": "http://localhost:1315",
                "check_interval": 600,
                "timeout": 10,
                "expected_status": [200],
                "check_content": True,
                "expected_content": ["AI Discovery"],
                "check_ssl": False
            }
        ],
        "alert_settings": {
            "cooldown_minutes": 15,
            "max_retries": 3,
            "retry_interval": 60
        },
        "performance_thresholds": {
            "response_time_warning": 2000,
            "response_time_critical": 5000,
            "uptime_warning": 95.0,
            "ssl_expiry_warning": 30
        },
        "report_schedule": {
            "daily_report_enabled": True,
            "daily_report_hour": 9,
            "weekly_report_enabled": True,
            "weekly_report_day": 1
        }
    }
    
    config_file = Path("monitoring_config.json")
    if not config_file.exists():
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"创建监控配置文件: {config_file}")

def main():
    """主函数"""
    # 创建必要的配置文件
    create_env_template()
    create_monitoring_config()
    
    # 检查环境变量
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("\n" + "="*60)
        print("⚠️  Telegram Bot 配置缺失")
        print("="*60)
        print("请完成以下步骤配置Telegram通知:")
        print("1. 创建Telegram Bot: @BotFather")
        print("2. 获取Bot Token")
        print("3. 获取Chat ID: @userinfobot")
        print("4. 在.env文件中配置:")
        print("   TELEGRAM_BOT_TOKEN=your_bot_token")
        print("   TELEGRAM_CHAT_ID=your_chat_id")
        print("5. 重新运行监控系统")
        print("="*60)
        print("⚠️  监控系统将在无通知模式下运行")
        print("="*60 + "\n")
        
        input("按回车键继续运行 (或Ctrl+C退出)...")
    
    # 启动监控系统
    launcher = MonitoringLauncher()
    
    try:
        asyncio.run(launcher.run())
    except Exception as e:
        print(f"监控系统启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()