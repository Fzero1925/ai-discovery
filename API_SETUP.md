# API Configuration Guide - 免费数据源配置指南

本文档详细说明如何申请和配置所有免费API，用于AI Discovery多源热门话题检测系统。

## 🚀 快速设置概览

配置完成后，你将拥有：
- Reddit API（完全免费）- AI社区讨论监控
- NewsAPI.org（免费1000次/天）- 实时AI新闻监控
- RSS Feeds（完全免费）- AI行业新闻聚合
- HackerNews API（完全免费）- 开发者社区趋势
- Product Hunt API（免费基础版）- 新AI工具发现

## 📋 必需的环境变量

在GitHub Secrets中设置以下环境变量：

```bash
# Reddit API (必需 - 社区趋势监控)
REDDIT_CLIENT_ID=你的client_id
REDDIT_CLIENT_SECRET=你的client_secret  
REDDIT_USER_AGENT=AI-Discovery/1.0

# News API (必需 - 新闻趋势监控)
NEWS_API_KEY=你的api_key

# Product Hunt (可选 - 新工具发现)
PRODUCTHUNT_TOKEN=你的token

# 现有的Telegram和图片APIs (保持不变)
TELEGRAM_BOT_TOKEN=你的bot_token
TELEGRAM_CHAT_ID=你的chat_id
UNSPLASH_ACCESS_KEY=你的unsplash_key
PEXELS_API_KEY=你的pexels_key
PIXABAY_API_KEY=你的pixabay_key
```

## 🔧 详细申请步骤

### 1. Reddit API（优先级：高）

**用途**：监控AI相关subreddits的热门讨论和争议话题

**申请步骤**：
1. 访问：https://www.reddit.com/prefs/apps
2. 登录你的Reddit账户
3. 点击"Create New Application"
4. 填写信息：
   - **name**: AI-Discovery-Bot
   - **App type**: 选择"script"
   - **description**: AI tools trending detection
   - **about url**: https://ai-discovery-nu.vercel.app/
   - **redirect uri**: http://localhost:8080
5. 点击"Create app"

**获取凭据**：
- `REDDIT_CLIENT_ID`: 应用程序下方的字符串（14位字符）
- `REDDIT_CLIENT_SECRET`: "secret"字段的值
- `REDDIT_USER_AGENT`: 填写`AI-Discovery/1.0`

**费用**：完全免费
**限制**：每分钟60个请求

### 2. NewsAPI.org（优先级：高）

**用途**：获取AI工具相关的最新新闻和媒体报道

**申请步骤**：
1. 访问：https://newsapi.org/register
2. 填写信息：
   - **First name**: 你的名字
   - **Last name**: 你的姓氏
   - **Email**: 你的邮箱
   - **Use case**: 选择"Personal project"
3. 点击"Submit"
4. 检查邮箱验证

**获取凭据**：
- 登录后在Dashboard获取`API Key`
- `NEWS_API_KEY`: 你的API密钥

**费用**：免费版1000次请求/天
**升级**：$449/月（生产环境可考虑）

### 3. Product Hunt API（优先级：中）

**用途**：发现新发布的AI工具和产品

**申请步骤**：
1. 访问：https://api.producthunt.com/v2/oauth/applications
2. 用Product Hunt账户登录
3. 点击"New Application"
4. 填写信息：
   - **Application name**: AI Discovery Tools Tracker
   - **Description**: Track new AI tools and products
   - **Website URL**: https://ai-discovery-nu.vercel.app/
5. 创建Developer Token

**获取凭据**：
- `PRODUCTHUNT_TOKEN`: 你的Developer Token

**费用**：基础版免费
**限制**：每小时500次请求

### 4. 配置GitHub Secrets

在GitHub仓库中设置环境变量：

1. 进入你的GitHub仓库
2. 点击"Settings" > "Secrets and variables" > "Actions"
3. 点击"New repository secret"
4. 逐一添加以下变量：

```bash
# 基础Reddit配置（必需）
REDDIT_CLIENT_ID          # 从Reddit app页面获取
REDDIT_CLIENT_SECRET       # 从Reddit app页面获取
REDDIT_USER_AGENT         # 填写: AI-Discovery/1.0

# 新闻API配置（必需）
NEWS_API_KEY              # 从newsapi.org获取

# 产品发现（可选）
PRODUCTHUNT_TOKEN         # 从Product Hunt获取

# 保持现有的API keys不变
TELEGRAM_BOT_TOKEN        # 现有值
TELEGRAM_CHAT_ID          # 现有值
UNSPLASH_ACCESS_KEY       # 现有值
PEXELS_API_KEY           # 现有值
PIXABAY_API_KEY          # 现有值
```

## 🧪 测试配置

配置完成后，你可以本地测试：

```bash
# 测试多源关键词检测
python scripts/multi_source_keywords.py

# 测试完整工作流
bash scripts/workflow_runner.sh

# 测试通知系统
python scripts/send_notification.py
```

## 📊 免费配额和限制

| API | 免费限额 | 功能 | 升级建议 |
|-----|---------|------|----------|
| Reddit | 60次/分钟 | 社区讨论监控 | 足够使用 |
| NewsAPI | 1000次/天 | 新闻趋势检测 | 月增长后升级 |
| HackerNews | 无限制 | 开发者趋势 | 无需升级 |
| RSS Feeds | 无限制 | 新闻聚合 | 无需升级 |
| Product Hunt | 500次/小时 | 新工具发现 | 可选升级 |

## 🔄 自动化配置验证

系统会自动检测API配置状态：

```python
# 在multi_source_detector.py中
def setup_apis(self):
    """初始化各种API客户端"""
    # Reddit API
    if all(key in os.environ for key in ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET']):
        self.reddit = praw.Reddit(...)
        print("✅ Reddit API initialized")
    else:
        print("❌ Reddit API credentials missing")
```

## 📈 数据源优先级策略

1. **高优先级**（必需配置）：
   - Reddit API：AI社区实时讨论
   - NewsAPI：主流媒体AI报道

2. **中优先级**（建议配置）：
   - Product Hunt API：新工具发现

3. **无需配置**（自动工作）：
   - HackerNews API：开发者社区
   - RSS Feeds：行业新闻聚合

## 🚨 常见问题

### Q: Reddit API申请被拒绝？
A: 确保填写真实信息，选择"script"类型，不要选择"web app"。

### Q: NewsAPI超出限额？
A: 免费版每天1000次，系统会自动降级到RSS feeds。

### Q: 通知系统不显示多源数据？
A: 检查notification_data.json文件是否正确生成，确认API配置正确。

### Q: 本地测试正常但GitHub Actions失败？
A: 检查GitHub Secrets是否正确设置，特别注意变量名大小写。

## 🎯 完成后的效果

配置完成后，Telegram通知将显示：
- 🔍 **Data Sources**: 🗣️ Reddit, 📰 News, 💻 HackerNews, 📡 RSS
- 📈 **Topics Analyzed**: 25 trending topics
- 💎 **High-Value Keywords**: 8 identified
- 🚨 **TRENDING CONTROVERSY DETECTED** (Score: 40/100)

## 📞 技术支持

如果遇到问题：
1. 检查本文档的配置步骤
2. 运行本地测试脚本验证API连接
3. 查看GitHub Actions日志中的错误信息
4. 确认所有环境变量已正确设置