# AI Discovery - 技术规格文档

**版本**: 1.0  
**更新时间**: 2025-09-04  
**技术负责**: AI Discovery Development Team

---

## 🏗️ **系统架构总览**

### **核心技术栈**
```yaml
静态站点生成: Hugo 0.149.0 Extended
内容管理: Python 3.11 + 自动化脚本
部署平台: Vercel + GitHub Actions CI/CD
监控系统: Telegram Bot + 健康检查
版本控制: Git + GitHub
CDN: Vercel Global Edge Network
```

### **系统架构图**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│ GitHub Actions  │───▶│   Vercel CDN    │
│                 │    │   CI/CD Pipeline │    │   Global Deploy │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Python Modules  │    │   Hugo Builder   │    │  Live Website   │
│ Content Engine  │    │  Static Compiler │    │  ai-discovery   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## 📁 **项目结构详解**

### **根目录结构**
```
ai-discovery/
├── .github/workflows/          # GitHub Actions自动化
├── content/                    # Hugo内容目录
├── data/ai_tools/             # AI工具数据库
├── layouts/                   # Hugo模板系统
├── modules/                   # Python自动化模块
├── static/                    # 静态资源
├── config.toml                # Hugo配置
├── vercel.json                # 部署配置
└── requirements.txt           # Python依赖
```

### **关键目录详细说明**

#### **`.github/workflows/`** - CI/CD自动化
```
vercel-deployment.yml         # 主部署流程
daily-content-generation.yml  # 每日内容生成
quality-monitoring.yml        # 质量监控
manual-content-update.yml     # 手动内容更新
```

#### **`content/`** - 内容管理
```
tools/                        # AI工具评测文章
  ├── chatgpt/               # ChatGPT详细评测
  ├── midjourney/            # Midjourney图像工具
  ├── claude/                # Claude AI助手
  └── [18+ more tools]/      # 其他工具评测
categories/                   # 工具分类页面
_index.md                    # 首页内容
```

#### **`modules/`** - Python自动化系统
```
content_generator/           # 内容生成引擎
  ├── generator.py          # 主生成脚本
  ├── templates/            # 内容模板
  └── keyword_analyzer.py   # 关键词分析
monitoring/                  # 监控系统
  ├── website_monitor.py    # 网站健康监控
  ├── telegram_bot.py       # Telegram通知
  └── performance_check.py  # 性能监控
keyword_tools/              # 关键词工具
  └── analyzer.py           # 关键词分析器
```

---

## 🔧 **核心技术实现**

### **1. Hugo静态站点生成**

#### **配置参数** (`config.toml`)
```toml
baseURL = "https://ai-discovery.vercel.app"
languageCode = "zh-cn"
title = "AI Discovery - 智能AI工具发现平台"
theme = "custom"

[params]
  description = "专业的AI工具评测和发现平台"
  keywords = "AI工具,人工智能,工具评测,ChatGPT,Midjourney"
  author = "AI Discovery Team"
  
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
```

#### **构建配置** (`vercel.json`)
```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.149.0"
    }
  },
  "buildCommand": "hugo --minify",
  "outputDirectory": "public",
  "installCommand": "echo 'Hugo will be installed automatically by Vercel'"
}
```

### **2. 内容生成系统**

#### **工具数据结构** (`data/ai_tools/`)
```yaml
# 示例：chatgpt.yaml
name: "ChatGPT"
category: "对话AI"
description: "OpenAI开发的大型语言模型"
features:
  - "自然语言对话"
  - "代码生成与调试"
  - "创意写作辅助"
pricing:
  free: "每月有限使用"
  paid: "$20/月无限使用"
website: "https://chat.openai.com"
rating: 4.8
```

#### **内容生成脚本** (`modules/content_generator/generator.py`)
```python
class ContentGenerator:
    def __init__(self, tools_data_path="data/ai_tools/"):
        self.tools_data = self.load_tools_data()
        
    def generate_tool_review(self, tool_name):
        """生成工具评测文章"""
        template = self.load_template("tool_review.md")
        tool_data = self.tools_data[tool_name]
        return template.format(**tool_data)
        
    def generate_category_page(self, category):
        """生成分类页面"""
        tools_in_category = self.filter_tools_by_category(category)
        return self.render_category_template(tools_in_category)
```

### **3. SEO和结构化数据**

#### **Schema.org实现** (`layouts/partials/seo-structured-data.html`)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "SoftwareApplication",
    "name": "{{ .Title }}",
    "applicationCategory": "AI工具",
    "operatingSystem": "Web, iOS, Android"
  },
  "author": {
    "@type": "Organization",
    "name": "AI Discovery"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "{{ .Params.rating }}",
    "bestRating": "5"
  }
}
</script>
```

#### **Meta标签优化**
```html
<meta name="description" content="{{ .Description }}">
<meta name="keywords" content="{{ .Keywords }}">
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ .Description }}">
<meta property="og:image" content="{{ .Params.featured_image }}">
<meta property="og:type" content="article">
```

### **4. 自动化部署流程**

#### **GitHub Actions主流程** (`.github/workflows/vercel-deployment.yml`)
```yaml
name: AI Discovery - Vercel Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.149.0'
          extended: true
          
      - name: Build Hugo site
        run: hugo --minify --environment production
        
      - name: Deploy to Vercel
        run: vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 📊 **性能优化策略**

### **1. 静态资源优化**
- **图片**: WebP格式，平均压缩率85%
- **CSS**: 压缩和内联关键CSS
- **JavaScript**: 最小化外部依赖
- **字体**: 子集化中文字体，减少加载大小

### **2. 缓存策略** (Vercel配置)
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {"key": "Cache-Control", "value": "public, max-age=3600"}
      ]
    },
    {
      "source": "/static/(.*)",
      "headers": [
        {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}
      ]
    }
  ]
}
```

### **3. SEO技术优化**
- **内部链接**: 每个工具页面平均15个相关链接
- **面包屑导航**: Schema.org标准实现
- **站点地图**: 自动生成XML sitemap
- **Robots.txt**: 搜索引擎抓取优化

---

## 🔒 **安全配置**

### **HTTP安全头**
```json
{
  "headers": [
    {"key": "X-Content-Type-Options", "value": "nosniff"},
    {"key": "X-Frame-Options", "value": "DENY"},
    {"key": "X-XSS-Protection", "value": "1; mode=block"},
    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}
  ]
}
```

### **内容安全策略**
- **HTTPS强制**: 所有连接强制SSL
- **外部链接**: nofollow和noreferrer属性
- **用户输入**: 无用户输入功能，避免XSS风险
- **API安全**: 仅内部API调用，无外部暴露

---

## 📈 **监控和分析**

### **1. 健康监控** (`modules/monitoring/website_monitor.py`)
```python
class WebsiteMonitor:
    def __init__(self):
        self.check_interval = 300  # 5分钟检查一次
        
    def check_website_health(self):
        """检查网站健康状态"""
        try:
            response = requests.get(self.base_url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            self.send_alert(f"网站健康检查失败: {e}")
            return False
            
    def send_telegram_notification(self, message):
        """发送Telegram通知"""
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        # 发送逻辑...
```

### **2. 性能监控**
- **构建时间**: 平均43秒
- **部署时间**: 平均2分钟
- **页面加载**: 平均3秒首次加载
- **CDN命中率**: 目标95%+

### **3. 内容监控**
- **页面完整性**: 自动检查所有页面是否正常加载
- **链接有效性**: 定期检查外部链接状态
- **图片加载**: 验证所有图片资源可访问
- **搜索功能**: 验证站内搜索正常工作

---

## 🚀 **扩展性设计**

### **1. 内容扩展**
```python
# 新增工具只需添加YAML配置文件
# data/ai_tools/new_tool.yaml
name: "New AI Tool"
category: "新分类"
# 其他配置...
```

### **2. 功能扩展架构**
- **多语言支持**: Hugo i18n框架已配置
- **用户系统**: 预留用户评价和收藏功能接口
- **API服务**: 可扩展为工具数据API提供商
- **移动应用**: PWA配置已准备

### **3. 基础设施扩展**
- **CDN**: Vercel全球边缘网络
- **数据库**: 可集成无服务器数据库
- **搜索**: 可集成Algolia或Elasticsearch
- **分析**: Google Analytics 4已配置

---

## 🔍 **故障排除指南**

### **常见问题解决方案**

#### **1. Hugo构建失败**
```bash
# 检查Hugo版本
hugo version
# 本地测试构建
hugo --minify --environment production
# 检查配置文件语法
hugo config
```

#### **2. Vercel部署失败**
```bash
# 验证vercel.json语法
cat vercel.json | python -m json.tool
# 检查环境变量
vercel env ls
# 本地测试部署
vercel dev
```

#### **3. 内容生成问题**
```bash
# 检查Python依赖
pip install -r requirements.txt
# 测试内容生成脚本
python modules/content_generator/generator.py
# 验证数据文件格式
python -c "import yaml; yaml.load(open('data/ai_tools/example.yaml'))"
```

---

## 📚 **维护和更新**

### **日常维护清单**
- [ ] 每周检查GitHub Actions运行状态
- [ ] 每月更新Hugo版本（如有必要）
- [ ] 每月审核和更新AI工具信息
- [ ] 每季度性能优化和安全审计

### **内容更新流程**
1. 在`data/ai_tools/`添加新工具YAML文件
2. 运行内容生成脚本更新页面
3. 本地测试验证
4. 提交到GitHub触发自动部署

### **版本管理**
- **主分支**: `main` - 生产环境代码
- **开发分支**: `dev` - 开发和测试
- **功能分支**: `feature/*` - 新功能开发
- **修复分支**: `hotfix/*` - 紧急修复

---

**📋 本技术文档涵盖AI Discovery平台的完整技术实现，为开发、部署和维护提供全面指导。**