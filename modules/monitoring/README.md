# AI Discovery 监控和通知系统

**状态**: ✅ 已完成  
**版本**: v1.0  
**更新时间**: 2025-09-04

---

## 🎯 系统概述

AI Discovery监控系统是一个全面的24/7智能监控解决方案，提供实时网站监控、系统性能追踪和自动化Telegram通知。该系统专为AI Discovery平台设计，确保网站稳定运行和及时发现问题。

### ✨ 核心功能
- **🌐 网站状态监控**: 实时检查网站可用性和响应时间
- **⚡ 性能指标监控**: 监控系统CPU、内存、磁盘使用率
- **🔒 SSL证书监控**: 自动检查SSL证书有效期
- **📊 构建性能分析**: 监控Hugo构建时间和页面统计
- **🔔 智能通知系统**: Telegram机器人实时警报
- **📈 自动报告**: 定期性能和状态报告

---

## 🏗️ 系统架构

### 核心组件
```
监控启动器 (monitoring_launcher.py)
├── Telegram Bot (telegram_bot.py)
├── 网站监控器 (website_monitor.py)
├── 性能监控器 (performance_monitor.py)
└── 配置和日志系统
```

### 技术栈
- **Python 3.11+**: 核心开发语言
- **asyncio**: 异步监控任务
- **aiohttp**: HTTP客户端
- **psutil**: 系统性能监控
- **Telegram Bot API**: 通知系统

---

## 📋 功能详细说明

### 1. Telegram Bot通知系统 (`telegram_bot.py`)

**核心功能**:
- ✅ 异步消息发送
- ✅ 格式化状态报告
- ✅ 错误警报通知
- ✅ 构建状态通知
- ✅ SEO报告通知

**支持的消息类型**:
- 网站状态报告
- 系统性能警报  
- 构建成功/失败通知
- 内容更新通知
- 错误和异常警报

**示例代码**:
```python
from telegram_bot import TelegramBot

bot = TelegramBot(bot_token, chat_id)
await bot.send_message("🤖 监控系统启动成功!")
```

### 2. 网站监控器 (`website_monitor.py`)

**监控指标**:
- ✅ **响应时间**: 网站响应速度监控
- ✅ **状态码检查**: HTTP状态码验证
- ✅ **内容完整性**: 关键内容存在性检查
- ✅ **SSL证书**: 证书有效期监控
- ✅ **可用性统计**: 正常运行时间跟踪

**警报阈值**:
- 响应时间 > 2秒 (警告)
- 响应时间 > 5秒 (严重)
- SSL证书 < 30天 (警告)
- 网站不可用 (严重)

**配置示例**:
```json
{
  "websites": [
    {
      "name": "AI Discovery (Production)",
      "url": "https://ai-discovery.vercel.app",
      "check_interval": 300,
      "expected_status": [200, 301, 302],
      "check_ssl": true
    }
  ]
}
```

### 3. 性能监控器 (`performance_monitor.py`)

**系统指标**:
- ✅ **CPU使用率**: 实时CPU负载监控
- ✅ **内存使用率**: 内存占用情况
- ✅ **磁盘使用率**: 存储空间监控
- ✅ **网络IO**: 网络流量统计
- ✅ **进程数量**: 系统进程监控

**网站性能指标**:
- ✅ **页面加载时间**: 完整页面加载速度
- ✅ **页面大小**: 资源大小统计
- ✅ **性能评分**: 综合性能评估

**构建性能监控**:
- ✅ **构建时间**: Hugo构建耗时
- ✅ **页面统计**: 生成页面数量
- ✅ **文件大小**: 输出文件总大小

### 4. 集成启动器 (`monitoring_launcher.py`)

**功能特性**:
- ✅ 统一管理所有监控组件
- ✅ 自动重启异常任务
- ✅ 健康检查和状态报告
- ✅ 优雅关闭和资源清理
- ✅ 信号处理和异常恢复

---

## 🚀 快速开始

### 1. 安装依赖
```bash
cd modules/monitoring
pip install -r requirements.txt
```

### 2. 配置Telegram Bot

**步骤**:
1. 在Telegram中找到 @BotFather
2. 发送 `/newbot` 创建新机器人
3. 获取Bot Token
4. 获取Chat ID (使用 @userinfobot)
5. 配置环境变量

**环境变量设置**:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

或创建 `.env` 文件:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. 启动监控系统
```bash
python monitoring_launcher.py
```

### 4. 验证系统运行

启动后您应该看到:
```
🚀 AI Discovery 监控系统已启动
📊 实时监控网站性能和系统状态
🔔 异常情况将通过Telegram通知
按 Ctrl+C 停止监控系统
```

---

## ⚙️ 配置文件

### monitoring_config.json
```json
{
  "websites": [
    {
      "name": "AI Discovery (Production)",
      "url": "https://ai-discovery.vercel.app",
      "check_interval": 300,
      "timeout": 30,
      "expected_status": [200, 301, 302],
      "check_content": true,
      "expected_content": ["AI Discovery", "AI工具"],
      "check_ssl": true
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
  }
}
```

### .env 配置文件
```env
# Telegram Bot配置
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# 监控配置
MONITORING_WEBSITE_URL=https://ai-discovery.vercel.app
MONITORING_LOCAL_URL=http://localhost:1315
MONITORING_INTERVAL=300

# 警报阈值
CPU_WARNING_THRESHOLD=80
CPU_CRITICAL_THRESHOLD=90
MEMORY_WARNING_THRESHOLD=85
MEMORY_CRITICAL_THRESHOLD=95
RESPONSE_TIME_WARNING=2000
RESPONSE_TIME_CRITICAL=5000
```

---

## 📊 监控指标和警报

### 系统性能警报

| 指标 | 警告阈值 | 严重阈值 | 说明 |
|------|----------|----------|------|
| CPU使用率 | 80% | 90% | 持续高CPU使用 |
| 内存使用率 | 85% | 95% | 内存不足风险 |
| 磁盘使用率 | 85% | 95% | 存储空间不足 |
| 响应时间 | 2000ms | 5000ms | 网站性能下降 |

### 网站监控警报

| 监控项 | 警报条件 | 通知方式 |
|--------|----------|----------|
| 网站不可用 | 状态码非2xx | 立即通知 |
| 响应时间异常 | >2秒或>5秒 | 立即通知 |
| SSL证书 | 30天内过期 | 每日提醒 |
| 内容异常 | 关键内容缺失 | 立即通知 |

---

## 📈 报告和通知

### 自动化报告

**每日性能报告** (每天上午9点):
```
📊 AI Discovery 每日性能报告

⏰ 报告时间: 2025-09-04 09:00:00
📈 报告周期: 24小时

🖥️ 系统性能:
• CPU平均使用率: 15.2%
• 内存使用率: 68.5%
• 磁盘使用率: 45.8%
• 综合评级: 优秀

🌐 网站性能:
• 响应时间: 1,250ms
• 性能评分: 85/100
• 服务状态: ONLINE
```

**实时警报通知**:
```
🚨 AI Discovery 错误警报

⚠️ 严重级别: WARNING
⏰ 发生时间: 2025-09-04 14:30:15
🔧 错误类型: CPU使用率警告

📝 错误详情:
CPU使用率达到 82%，超过警告阈值 80%

🛠️ 建议操作:
• 监控CPU使用趋势
• 优化资源密集型任务
```

---

## 🔧 高级功能

### 1. 自定义监控项

添加新的网站监控:
```python
# 在monitoring_config.json中添加
{
  "name": "新网站",
  "url": "https://example.com",
  "check_interval": 300,
  "expected_content": ["关键词1", "关键词2"]
}
```

### 2. 自定义警报阈值

修改性能阈值:
```json
{
  "performance_thresholds": {
    "cpu_warning": 70,
    "cpu_critical": 85,
    "response_time_warning": 1500
  }
}
```

### 3. 扩展通知格式

自定义消息格式:
```python
def custom_alert_format(alert_data):
    return f"🔔 自定义警报: {alert_data['message']}"
```

---

## 📁 文件结构

```
modules/monitoring/
├── README.md                 # 本文档
├── requirements.txt          # 依赖包列表
├── monitoring_launcher.py    # 主启动器
├── telegram_bot.py          # Telegram Bot
├── website_monitor.py       # 网站监控器
├── performance_monitor.py   # 性能监控器
├── monitoring_config.json   # 监控配置(自动生成)
├── .env.example            # 环境变量模板
└── logs/                   # 日志目录
    ├── monitoring/         # 监控日志
    └── performance/        # 性能日志
```

---

## 🚨 故障排除

### 常见问题

**Q: Telegram通知不工作？**
A: 检查环境变量配置，确保Bot Token和Chat ID正确

**Q: 监控系统异常退出？**
A: 查看logs目录下的日志文件，检查具体错误信息

**Q: 性能监控数据不准确？**  
A: 确保psutil库正确安装，检查系统权限

**Q: 网站监控误报？**
A: 调整monitoring_config.json中的expected_status和timeout设置

### 日志查看
```bash
# 查看监控日志
tail -f logs/monitoring_launcher_20250904.log

# 查看性能日志
tail -f logs/performance/performance_20250904.jsonl
```

---

## 🔄 系统更新和维护

### 定期维护
- **日志清理**: 每月清理超过30天的日志文件
- **配置检查**: 每季度审查监控配置和阈值
- **依赖更新**: 每半年更新Python依赖包

### 系统升级
```bash
# 更新依赖
pip install -r requirements.txt --upgrade

# 重启监控系统
python monitoring_launcher.py
```

---

## 📞 技术支持

### 联系信息
- **项目**: AI Discovery监控系统
- **版本**: v1.0
- **技术架构**: Python 3.11 + asyncio + Telegram Bot API

### 支持功能
- ✅ 24/7 自动监控
- ✅ 实时Telegram通知
- ✅ 完整性能报告
- ✅ 自动故障恢复
- ✅ 灵活配置管理

---

**监控系统状态**: 🟢 运行中  
**上次更新**: 2025-09-04  
**下次维护**: 按需进行

🤖 **AI Discovery 监控系统** - 7x24小时智能守护您的网站