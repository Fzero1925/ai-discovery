#!/usr/bin/env python3
"""
AI Discovery - 性能监控系统
Performance monitoring system with SEO tracking and alerts
"""

import asyncio
import aiohttp
import json
import logging
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import subprocess
import requests
from urllib.parse import urlparse

from telegram_bot import TelegramBot, create_bot_from_env

class PerformanceMonitor:
    """AI Discovery性能监控系统"""
    
    def __init__(self, telegram_bot: Optional[TelegramBot] = None):
        """
        初始化性能监控器
        Args:
            telegram_bot: Telegram Bot实例
        """
        self.telegram_bot = telegram_bot
        self.logger = self._setup_logger()
        self.metrics_history = []
        self.last_report_time = None
        self.thresholds = self._load_thresholds()
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("PerformanceMonitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger

    def _load_thresholds(self) -> Dict:
        """加载性能阈值配置"""
        return {
            "cpu_warning": 80.0,       # CPU使用率警告阈值
            "cpu_critical": 90.0,      # CPU使用率严重阈值
            "memory_warning": 85.0,    # 内存使用率警告阈值  
            "memory_critical": 95.0,   # 内存使用率严重阈值
            "disk_warning": 85.0,      # 磁盘使用率警告阈值
            "disk_critical": 95.0,     # 磁盘使用率严重阈值
            "response_time_warning": 2000,  # 响应时间警告阈值(ms)
            "response_time_critical": 5000, # 响应时间严重阈值(ms)
            "page_size_warning": 5 * 1024 * 1024,  # 页面大小警告阈值(5MB)
            "build_time_warning": 300,  # 构建时间警告阈值(秒)
            "error_rate_warning": 5.0,  # 错误率警告阈值(%)
        }

    async def collect_system_metrics(self) -> Dict:
        """
        收集系统性能指标
        Returns:
            系统指标字典
        """
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # 网络IO
            net_io = psutil.net_io_counters()
            
            # 进程信息
            process_count = len(psutil.pids())
            
            # 负载平均值（仅Unix系统）
            try:
                load_avg = psutil.getloadavg()
            except AttributeError:
                load_avg = (0, 0, 0)  # Windows不支持getloadavg
            
            metrics = {
                "timestamp": datetime.now(),
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory_percent, 2),
                "memory_used_gb": round(memory.used / (1024**3), 2),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "disk_percent": round(disk_percent, 2),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "network_bytes_sent": net_io.bytes_sent,
                "network_bytes_recv": net_io.bytes_recv,
                "process_count": process_count,
                "load_avg_1min": round(load_avg[0], 2),
                "load_avg_5min": round(load_avg[1], 2),
                "load_avg_15min": round(load_avg[2], 2),
            }
            
            # 计算性能等级
            metrics.update(self._calculate_performance_grade(metrics))
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"收集系统指标失败: {e}")
            return {}

    async def collect_website_metrics(self, url: str = "http://localhost:1315") -> Dict:
        """
        收集网站性能指标
        Args:
            url: 网站URL
        Returns:
            网站指标字典
        """
        metrics = {
            "timestamp": datetime.now(),
            "url": url,
            "status": "unknown",
            "response_time": None,
            "page_size": None,
            "status_code": None,
            "headers": {},
            "performance_score": None
        }
        
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    end_time = time.time()
                    response_time = int((end_time - start_time) * 1000)
                    
                    # 读取响应内容
                    content = await response.read()
                    page_size = len(content)
                    
                    metrics.update({
                        "status": "online" if response.status == 200 else "error",
                        "response_time": response_time,
                        "page_size": page_size,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "content_type": response.headers.get('content-type', ''),
                        "server": response.headers.get('server', ''),
                    })
                    
                    # 计算性能分数
                    metrics["performance_score"] = self._calculate_performance_score(metrics)
                    
        except Exception as e:
            metrics.update({
                "status": "error",
                "error": str(e)
            })
            self.logger.warning(f"收集网站指标失败: {e}")
        
        return metrics

    async def collect_build_metrics(self) -> Dict:
        """
        收集构建性能指标
        Returns:
            构建指标字典
        """
        metrics = {
            "timestamp": datetime.now(),
            "status": "unknown",
            "build_time": None,
            "pages_count": 0,
            "file_size": 0,
            "error": None
        }
        
        try:
            # 执行Hugo构建
            start_time = time.time()
            result = subprocess.run(
                ["hugo", "--minify"],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            end_time = time.time()
            
            build_time = end_time - start_time
            
            if result.returncode == 0:
                # 解析Hugo输出获取统计信息
                output = result.stdout
                pages_count = self._parse_pages_count(output)
                
                # 计算输出目录大小
                public_dir = Path("public")
                if public_dir.exists():
                    file_size = self._calculate_directory_size(public_dir)
                
                metrics.update({
                    "status": "success",
                    "build_time": round(build_time, 2),
                    "pages_count": pages_count,
                    "file_size": file_size,
                    "output": output
                })
            else:
                metrics.update({
                    "status": "error",
                    "error": result.stderr,
                    "build_time": round(build_time, 2)
                })
                
        except subprocess.TimeoutExpired:
            metrics.update({
                "status": "timeout",
                "error": "构建超时"
            })
        except Exception as e:
            metrics.update({
                "status": "error", 
                "error": str(e)
            })
        
        return metrics

    def _calculate_performance_grade(self, metrics: Dict) -> Dict:
        """
        计算性能等级
        Args:
            metrics: 系统指标
        Returns:
            性能等级信息
        """
        grades = {}
        
        # CPU等级
        cpu = metrics.get("cpu_percent", 0)
        if cpu < 50:
            grades["cpu_grade"] = "优秀"
        elif cpu < 70:
            grades["cpu_grade"] = "良好"
        elif cpu < 85:
            grades["cpu_grade"] = "一般"
        else:
            grades["cpu_grade"] = "较差"
        
        # 内存等级
        memory = metrics.get("memory_percent", 0)
        if memory < 60:
            grades["memory_grade"] = "优秀"
        elif memory < 75:
            grades["memory_grade"] = "良好"
        elif memory < 90:
            grades["memory_grade"] = "一般"
        else:
            grades["memory_grade"] = "较差"
        
        # 磁盘等级
        disk = metrics.get("disk_percent", 0)
        if disk < 70:
            grades["disk_grade"] = "优秀"
        elif disk < 85:
            grades["disk_grade"] = "良好"
        elif disk < 95:
            grades["disk_grade"] = "一般"
        else:
            grades["disk_grade"] = "较差"
        
        # 综合等级
        avg_usage = (cpu + memory + disk) / 3
        if avg_usage < 60:
            grades["overall_grade"] = "优秀"
        elif avg_usage < 75:
            grades["overall_grade"] = "良好"
        elif avg_usage < 85:
            grades["overall_grade"] = "一般"
        else:
            grades["overall_grade"] = "较差"
        
        return grades

    def _calculate_performance_score(self, metrics: Dict) -> int:
        """
        计算网站性能分数
        Args:
            metrics: 网站指标
        Returns:
            性能分数 (0-100)
        """
        score = 100
        
        # 响应时间影响 (40分)
        response_time = metrics.get("response_time", 0)
        if response_time > 5000:
            score -= 40
        elif response_time > 3000:
            score -= 30
        elif response_time > 2000:
            score -= 20
        elif response_time > 1000:
            score -= 10
        
        # 页面大小影响 (30分)
        page_size = metrics.get("page_size", 0)
        if page_size > 10 * 1024 * 1024:  # 10MB
            score -= 30
        elif page_size > 5 * 1024 * 1024:  # 5MB
            score -= 20
        elif page_size > 2 * 1024 * 1024:  # 2MB
            score -= 10
        
        # 状态码影响 (30分)
        status_code = metrics.get("status_code", 200)
        if status_code != 200:
            score -= 30
        
        return max(0, min(100, score))

    def _parse_pages_count(self, hugo_output: str) -> int:
        """
        从Hugo输出解析页面数量
        Args:
            hugo_output: Hugo命令输出
        Returns:
            页面数量
        """
        try:
            lines = hugo_output.split('\n')
            for line in lines:
                if 'Pages' in line and '|' in line:
                    # 例如: " Pages            │ 96 │  8 "
                    parts = line.split('|')
                    if len(parts) >= 2:
                        return int(parts[1].strip())
            return 0
        except:
            return 0

    def _calculate_directory_size(self, directory: Path) -> int:
        """
        计算目录大小
        Args:
            directory: 目录路径
        Returns:
            目录大小(字节)
        """
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except:
            pass
        return total_size

    async def check_performance_alerts(self, system_metrics: Dict, website_metrics: Dict):
        """
        检查性能警报
        Args:
            system_metrics: 系统指标
            website_metrics: 网站指标
        """
        alerts = []
        
        # 检查系统指标
        cpu_percent = system_metrics.get("cpu_percent", 0)
        memory_percent = system_metrics.get("memory_percent", 0)
        disk_percent = system_metrics.get("disk_percent", 0)
        
        if cpu_percent > self.thresholds["cpu_critical"]:
            alerts.append({
                "severity": "critical",
                "type": "CPU使用率过高",
                "message": f"CPU使用率达到 {cpu_percent}%，超过严重阈值 {self.thresholds['cpu_critical']}%",
                "suggestions": ["检查高CPU占用进程", "考虑增加服务器资源", "优化应用程序性能"]
            })
        elif cpu_percent > self.thresholds["cpu_warning"]:
            alerts.append({
                "severity": "warning",
                "type": "CPU使用率警告",
                "message": f"CPU使用率达到 {cpu_percent}%，超过警告阈值 {self.thresholds['cpu_warning']}%",
                "suggestions": ["监控CPU使用趋势", "优化资源密集型任务"]
            })
        
        if memory_percent > self.thresholds["memory_critical"]:
            alerts.append({
                "severity": "critical",
                "type": "内存使用率过高",
                "message": f"内存使用率达到 {memory_percent}%，超过严重阈值 {self.thresholds['memory_critical']}%",
                "suggestions": ["重启高内存占用进程", "增加服务器内存", "检查内存泄漏"]
            })
        elif memory_percent > self.thresholds["memory_warning"]:
            alerts.append({
                "severity": "warning", 
                "type": "内存使用率警告",
                "message": f"内存使用率达到 {memory_percent}%，超过警告阈值 {self.thresholds['memory_warning']}%",
                "suggestions": ["清理不必要进程", "优化内存使用"]
            })
        
        # 检查网站指标
        response_time = website_metrics.get("response_time", 0)
        if response_time > self.thresholds["response_time_critical"]:
            alerts.append({
                "severity": "critical",
                "type": "网站响应时间过长",
                "message": f"网站响应时间 {response_time}ms，超过严重阈值 {self.thresholds['response_time_critical']}ms",
                "suggestions": ["检查服务器负载", "优化网站性能", "检查网络连接"]
            })
        elif response_time > self.thresholds["response_time_warning"]:
            alerts.append({
                "severity": "warning",
                "type": "网站响应时间警告",
                "message": f"网站响应时间 {response_time}ms，超过警告阈值 {self.thresholds['response_time_warning']}ms",
                "suggestions": ["优化页面加载", "压缩静态资源"]
            })
        
        # 发送警报
        for alert in alerts:
            await self.send_performance_alert(alert, system_metrics)

    async def send_performance_alert(self, alert: Dict, system_metrics: Dict):
        """
        发送性能警报
        Args:
            alert: 警报信息
            system_metrics: 系统指标
        """
        if not self.telegram_bot:
            return
        
        # 准备错误数据格式
        error_data = {
            "severity": alert["severity"],
            "type": alert["type"],
            "message": alert["message"],
            "location": "AI Discovery System",
            "cpu_usage": system_metrics.get("cpu_percent", 0),
            "memory_usage": system_metrics.get("memory_percent", 0),
            "disk_usage": system_metrics.get("disk_percent", 0),
            "suggestions": alert["suggestions"]
        }
        
        message = self.telegram_bot.format_error_alert(error_data)
        await self.telegram_bot.send_message(message)
        
        self.logger.warning(f"发送性能警报: {alert['type']} - {alert['severity']}")

    async def generate_daily_report(self):
        """生成每日性能报告"""
        if not self.telegram_bot:
            return
        
        # 收集当前指标
        system_metrics = await self.collect_system_metrics()
        website_metrics = await self.collect_website_metrics()
        build_metrics = await self.collect_build_metrics()
        
        # 准备报告数据
        report_data = {
            "period": "24小时",
            "system_performance": {
                "cpu_avg": system_metrics.get("cpu_percent", 0),
                "memory_avg": system_metrics.get("memory_percent", 0),
                "disk_usage": system_metrics.get("disk_percent", 0),
                "overall_grade": system_metrics.get("overall_grade", "未知")
            },
            "website_performance": {
                "response_time": website_metrics.get("response_time", 0),
                "performance_score": website_metrics.get("performance_score", 0),
                "status": website_metrics.get("status", "unknown")
            },
            "build_performance": {
                "status": build_metrics.get("status", "unknown"),
                "build_time": build_metrics.get("build_time", 0),
                "pages_count": build_metrics.get("pages_count", 0)
            }
        }
        
        # 发送报告
        message = self._format_daily_report(report_data)
        await self.telegram_bot.send_message(message)
        
        self.logger.info("发送每日性能报告")

    def _format_daily_report(self, data: Dict) -> str:
        """
        格式化每日报告
        Args:
            data: 报告数据
        Returns:
            格式化的HTML消息
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
📊 <b>AI Discovery 每日性能报告</b>

⏰ <b>报告时间:</b> {timestamp}
📈 <b>报告周期:</b> {data.get("period", "24小时")}

🖥️ <b>系统性能:</b>
• CPU平均使用率: {data['system_performance']['cpu_avg']}%
• 内存使用率: {data['system_performance']['memory_avg']}%
• 磁盘使用率: {data['system_performance']['disk_usage']}%
• 综合评级: {data['system_performance']['overall_grade']}

🌐 <b>网站性能:</b>
• 响应时间: {data['website_performance']['response_time']}ms
• 性能评分: {data['website_performance']['performance_score']}/100
• 服务状态: {data['website_performance']['status'].upper()}

🏗️ <b>构建性能:</b>
• 构建状态: {data['build_performance']['status'].upper()}
• 构建时间: {data['build_performance']['build_time']}秒
• 页面数量: {data['build_performance']['pages_count']}个

💡 <b>优化建议:</b>
{self._generate_optimization_suggestions(data)}

🚀 <b>AI Discovery</b> - 持续性能优化中
        """
        return message.strip()

    def _generate_optimization_suggestions(self, data: Dict) -> str:
        """
        生成优化建议
        Args:
            data: 性能数据
        Returns:
            优化建议文本
        """
        suggestions = []
        
        # 系统性能建议
        cpu_avg = data['system_performance']['cpu_avg']
        memory_avg = data['system_performance']['memory_avg']
        
        if cpu_avg > 70:
            suggestions.append("考虑优化CPU密集型任务")
        if memory_avg > 80:
            suggestions.append("监控内存使用，考虑增加内存")
        
        # 网站性能建议
        response_time = data['website_performance']['response_time']
        if response_time > 2000:
            suggestions.append("优化网站响应时间，压缩静态资源")
        
        # 构建性能建议
        build_time = data['build_performance']['build_time']
        if build_time > 120:  # 2分钟
            suggestions.append("优化构建流程，减少构建时间")
        
        if not suggestions:
            suggestions.append("当前性能表现良好，继续保持")
        
        return "\n".join([f"• {s}" for s in suggestions[:3]])

    async def run_monitoring_cycle(self):
        """执行一轮性能监控"""
        self.logger.info("开始性能监控周期")
        
        try:
            # 收集所有指标
            system_metrics = await self.collect_system_metrics()
            website_metrics = await self.collect_website_metrics()
            
            # 保存指标到历史记录
            combined_metrics = {
                **system_metrics,
                **{f"website_{k}": v for k, v in website_metrics.items()}
            }
            self.metrics_history.append(combined_metrics)
            
            # 只保留最近100条记录
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            # 检查性能警报
            await self.check_performance_alerts(system_metrics, website_metrics)
            
            # 保存监控数据
            self._save_performance_data(combined_metrics)
            
        except Exception as e:
            self.logger.error(f"性能监控周期异常: {e}")

    def _save_performance_data(self, metrics: Dict):
        """
        保存性能数据
        Args:
            metrics: 性能指标
        """
        try:
            log_dir = Path("logs/performance")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            log_file = log_dir / f"performance_{datetime.now().strftime('%Y%m%d')}.jsonl"
            
            # 创建可序列化的指标副本
            serializable_metrics = {
                k: v.isoformat() if isinstance(v, datetime) else v
                for k, v in metrics.items()
            }
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(serializable_metrics, ensure_ascii=False) + '\n')
                
        except Exception as e:
            self.logger.warning(f"保存性能数据失败: {e}")

    async def start_monitoring(self, report_interval: int = 3600):
        """
        启动性能监控
        Args:
            report_interval: 报告间隔(秒)
        """
        self.logger.info("AI Discovery 性能监控系统启动")
        
        if self.telegram_bot:
            startup_message = f"""
🚀 <b>AI Discovery 性能监控启动</b>

⏰ <b>启动时间:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 <b>监控类型:</b> 系统性能 + 网站性能 + 构建性能
🔔 <b>警报阈值:</b>
• CPU > {self.thresholds['cpu_warning']}% (警告)
• 内存 > {self.thresholds['memory_warning']}% (警告)
• 响应时间 > {self.thresholds['response_time_warning']}ms (警告)

💡 <b>监控功能:</b>
• 实时系统资源监控
• 网站响应时间跟踪
• 构建性能分析
• 自动警报通知

🤖 <b>AI Discovery</b> - 性能监控已就绪
            """
            await self.telegram_bot.send_message(startup_message.strip())
        
        next_report = datetime.now() + timedelta(seconds=report_interval)
        
        try:
            while True:
                await self.run_monitoring_cycle()
                
                # 检查是否需要发送定期报告
                current_time = datetime.now()
                if current_time >= next_report:
                    await self.generate_daily_report()
                    next_report = current_time + timedelta(seconds=report_interval)
                
                # 等待下次检查
                await asyncio.sleep(300)  # 5分钟间隔
                
        except KeyboardInterrupt:
            self.logger.info("性能监控系统被用户中断")
        except Exception as e:
            self.logger.error(f"性能监控系统异常: {e}")
            raise

async def main():
    """主函数"""
    telegram_bot = create_bot_from_env()
    
    if not telegram_bot:
        print("警告: 无法创建Telegram Bot，监控将在无通知模式下运行")
    
    monitor = PerformanceMonitor(telegram_bot)
    
    print("启动AI Discovery性能监控系统...")
    print("按 Ctrl+C 停止监控")
    
    try:
        await monitor.start_monitoring(report_interval=3600*24)  # 每天报告一次
    except KeyboardInterrupt:
        print("\n性能监控系统已停止")

if __name__ == "__main__":
    asyncio.run(main())