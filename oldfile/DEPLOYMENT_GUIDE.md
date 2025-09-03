# 部署实施指南

## 🎯 部署概览

本指南提供AI Discovery平台从零开始到完全自动化运营的完整部署流程，包括技术搭建、内容初始化、变现配置和监控部署。

## 📋 部署准备清单

### 必需账户和服务
```yaml
核心服务账户:
  - GitHub: ✅ 代码管理和自动化
  - Vercel: ✅ 静态网站部署
  - Google Analytics: ✅ 流量分析  
  - Google Search Console: ✅ SEO监控
  - Google AdSense: ✅ 广告变现
  - Telegram Bot: ✅ 自动化通知

可选增强服务:
  - Cloudflare: 🔄 CDN和安全
  - Amazon Associates: 🔄 联盟营销
  - Semrush API: 🔄 关键词研究
  - Airtable: 🔄 数据管理
```

### 开发环境要求
```bash
系统要求:
  - Node.js 18.0+
  - Python 3.11+
  - Git 2.30+
  - Hugo 0.120.0+

推荐开发工具:
  - VS Code + Hugo插件
  - Python虚拟环境
  - Postman (API测试)
```

## 🚀 阶段一：基础架构部署

### Step 1: 项目初始化
```bash
# 1. 克隆项目模板
git clone https://github.com/yourusername/ai-discovery-template.git
cd ai-discovery-template

# 2. 设置Python虚拟环境
python -m venv ai-discovery-env
source ai-discovery-env/bin/activate  # Linux/Mac
# 或 ai-discovery-env\Scripts\activate  # Windows

# 3. 安装Python依赖
pip install -r requirements.txt

# 4. 安装Hugo
# Linux/Mac
wget https://github.com/gohugoio/hugo/releases/download/v0.120.0/hugo_extended_0.120.0_Linux-64bit.tar.gz
tar -xvf hugo_extended_0.120.0_Linux-64bit.tar.gz
sudo mv hugo /usr/local/bin/

# Windows
# 下载并安装 Hugo Extended版本

# 5. 验证安装
hugo version
python --version
```

### Step 2: 项目结构创建
```bash
# 创建Hugo网站
hugo new site ai-discovery
cd ai-discovery

# 创建项目目录结构
mkdir -p {scripts,data/{keywords,products,analytics},config,docs}
mkdir -p content/{posts,tools,pages}
mkdir -p themes/ai-discovery/{layouts,static,assets}

# 创建必要配置文件
touch config/hugo.toml
touch config/requirements.txt
touch config/secrets.env.example
```

### Step 3: Hugo主题配置
```toml
# config/hugo.toml
baseURL = "https://your-domain.com"
languageCode = "en-us"
title = "AI Discovery - 智能AI工具发现平台"
theme = "ai-discovery"

paginate = 12
enableRobotsTXT = true
enableGitInfo = true

# 变现配置
[params]
  google_analytics_id = "G-XXXXXXXXX"
  google_adsense_id = "ca-pub-XXXXXXXXX"
  amazon_associate_tag = "yourtag-20"
  
  # SEO配置
  description = "发现最优秀的AI工具，提供专业评测和使用指南"
  keywords = "AI工具, 人工智能, 工具评测, AI应用"
  author = "AI Discovery Team"
  
  # 社交媒体
  twitter = "@aidiscovery"
  
  # 功能开关
  search_enabled = true
  comments_enabled = false
  newsletter_enabled = true

# 菜单配置
[[menu.main]]
  name = "首页"
  url = "/"
  weight = 1

[[menu.main]]
  name = "AI工具"
  url = "/tools/"
  weight = 2

[[menu.main]]
  name = "评测文章"
  url = "/posts/"
  weight = 3

[[menu.main]]
  name = "关于"
  url = "/about/"
  weight = 4

# 输出格式
[outputs]
  home = ["HTML", "RSS", "JSON"]
  page = ["HTML"]
  section = ["HTML", "RSS"]

# Markup配置
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    style = "github"
    lineNos = true

# SEO优化
[sitemap]
  changefreq = "daily"
  priority = 0.8
  filename = "sitemap.xml"
```

### Step 4: Python自动化脚本配置
```python
# config/requirements.txt
pytrends==4.9.2
jinja2==3.1.2
pandas==2.1.0
requests==2.31.0
python-dateutil==2.8.2
pyyaml==6.0.1
beautifulsoup4==4.12.2
lxml==4.9.3
openai==1.3.0
google-api-python-client==2.108.0
python-telegram-bot==20.6
aiohttp==3.9.0
numpy==1.25.2
scikit-learn==1.3.0
matplotlib==3.8.0
python-dotenv==1.0.0
```

```python
# scripts/config_manager.py
import os
from dotenv import load_dotenv

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        load_dotenv('config/secrets.env')
        
        self.config = {
            # API配置
            'google_trends_proxy': os.getenv('GOOGLE_TRENDS_PROXY'),
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
            
            # Google服务配置
            'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID'),
            'google_search_console_key': os.getenv('GOOGLE_SEARCH_CONSOLE_KEY'),
            'google_adsense_id': os.getenv('GOOGLE_ADSENSE_ID'),
            
            # 联盟营销配置
            'amazon_associate_tag': os.getenv('AMAZON_ASSOCIATE_TAG'),
            'amazon_api_key': os.getenv('AMAZON_API_KEY'),
            
            # 网站配置
            'site_url': os.getenv('SITE_URL', 'https://ai-discovery.com'),
            'site_title': os.getenv('SITE_TITLE', 'AI Discovery'),
            
            # 自动化配置
            'daily_content_quota': int(os.getenv('DAILY_CONTENT_QUOTA', '2')),
            'quality_threshold': float(os.getenv('QUALITY_THRESHOLD', '0.8')),
            'anti_ai_threshold': float(os.getenv('ANTI_AI_THRESHOLD', '0.75'))
        }
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def validate_config(self):
        """验证配置完整性"""
        required_keys = [
            'telegram_bot_token', 'telegram_chat_id',
            'google_analytics_id', 'site_url'
        ]
        
        missing_keys = [key for key in required_keys if not self.get(key)]
        
        if missing_keys:
            raise ValueError(f"缺少必需配置: {missing_keys}")
        
        return True
```

## 🔧 阶段二：自动化系统配置

### Step 5: GitHub Actions工作流
```yaml
# .github/workflows/deploy.yml
name: Deploy AI Discovery Site

on:
  push:
    branches: [ main ]
  schedule:
    # 每天UTC 8点执行内容生成
    - cron: '0 8 * * *'
  workflow_dispatch:

env:
  HUGO_VERSION: 0.120.0

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
    
    - name: Setup Hugo
      uses: peaceiris/actions-hugo@v2
      with:
        hugo-version: ${{ env.HUGO_VERSION }}
        extended: true
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache Python dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r config/requirements.txt
    
    - name: Generate Daily Content
      if: github.event_name == 'schedule'
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        GOOGLE_ANALYTICS_ID: ${{ secrets.GOOGLE_ANALYTICS_ID }}
        SITE_URL: ${{ secrets.SITE_URL }}
      run: |
        python scripts/daily_content_generator.py
    
    - name: Build Hugo Site
      run: |
        hugo --minify --environment production
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        vercel-args: '--prod'
        working-directory: ./public
    
    - name: Commit generated content
      if: github.event_name == 'schedule'
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add content/
        git diff --staged --quiet || git commit -m "🤖 Auto-generated daily content $(date +'%Y-%m-%d')"
        git push
    
    - name: Notify Success
      if: success()
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: |
        python scripts/telegram_notifier.py "✅ Site deployed successfully $(date +'%Y-%m-%d %H:%M')"
    
    - name: Notify Failure  
      if: failure()
      env:
        TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
        TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
      run: |
        python scripts/telegram_notifier.py "❌ Deployment failed $(date +'%Y-%m-%d %H:%M'). Check logs."
```

### Step 6: 核心自动化脚本
```python
# scripts/daily_content_generator.py
#!/usr/bin/env python3
"""每日内容生成脚本"""

import sys
import traceback
from datetime import datetime
from config_manager import ConfigManager
from keyword_analyzer import SmartKeywordAnalyzer  
from content_engine import AntiAIContentEngine
from seo_optimizer import SEOOptimizer
from telegram_notifier import TelegramNotifier

def main():
    """主执行函数"""
    
    config = ConfigManager()
    notifier = TelegramNotifier(config)
    
    try:
        print(f"🚀 开始每日内容生成 - {datetime.now()}")
        
        # 验证配置
        config.validate_config()
        print("✅ 配置验证通过")
        
        # 初始化组件
        keyword_analyzer = SmartKeywordAnalyzer(config)
        content_engine = AntiAIContentEngine(config)
        seo_optimizer = SEOOptimizer(config)
        
        # 发现趋势关键词
        print("🔍 发现趋势关键词...")
        trending_keywords = keyword_analyzer.discover_high_value_keywords(
            limit=config.get('daily_content_quota', 2) * 2
        )
        
        if not trending_keywords:
            raise Exception("未发现合适的趋势关键词")
        
        print(f"📊 发现 {len(trending_keywords)} 个候选关键词")
        
        # 生成内容
        successful_articles = 0
        failed_articles = 0
        generated_articles = []
        
        for i, keyword_data in enumerate(trending_keywords[:config.get('daily_content_quota', 2)]):
            try:
                print(f"📝 生成文章 {i+1}: {keyword_data['keyword']}")
                
                # 生成文章
                article = content_engine.generate_ai_tool_article(
                    keyword=keyword_data['keyword'],
                    tool_data=keyword_data.get('tool_data', {}),
                    article_type=keyword_data.get('content_type', 'introduction')
                )
                
                # 质量检查
                if (article['quality_score'] >= config.get('quality_threshold', 0.8) and
                    article['anti_ai_score'] >= config.get('anti_ai_threshold', 0.75)):
                    
                    # SEO优化
                    optimized_article = seo_optimizer.optimize_article(article, keyword_data)
                    
                    # 保存文章
                    article_path = save_hugo_article(optimized_article)
                    
                    generated_articles.append({
                        'title': article['title'],
                        'path': article_path,
                        'keyword': keyword_data['keyword'],
                        'quality_score': article['quality_score'],
                        'anti_ai_score': article['anti_ai_score']
                    })
                    
                    successful_articles += 1
                    print(f"✅ 文章生成成功: {article['title']}")
                    
                else:
                    failed_articles += 1
                    print(f"❌ 文章质量不达标: {keyword_data['keyword']}")
                    
            except Exception as e:
                failed_articles += 1
                print(f"❌ 文章生成失败: {keyword_data['keyword']} - {e}")
        
        # 后续SEO优化
        if generated_articles:
            print("🔍 执行SEO优化...")
            seo_optimizer.build_internal_links([a['keyword'] for a in generated_articles])
            seo_optimizer.update_sitemap()
        
        # 发送成功报告
        report = generate_success_report(successful_articles, failed_articles, generated_articles)
        notifier.send_message(report)
        
        print("🎉 每日内容生成完成!")
        
    except Exception as e:
        error_message = f"❌ 每日内容生成失败:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_message)
        notifier.send_message(f"❌ 每日内容生成失败: {str(e)}")
        sys.exit(1)

def save_hugo_article(article_data):
    """保存Hugo格式文章"""
    
    from datetime import datetime
    import os
    import yaml
    
    # 生成文件名
    slug = article_data['title'].lower().replace(' ', '-').replace(',', '').replace(':', '')
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
    article_path = f"content/posts/{filename}"
    
    # Hugo Front Matter
    front_matter = {
        'title': article_data['title'],
        'description': article_data['metadata']['description'],
        'date': datetime.now().isoformat() + 'Z',
        'categories': article_data['metadata']['categories'],
        'tags': article_data['metadata']['tags'],
        'keywords': article_data['metadata']['keywords'],
        'author': 'AI Discovery Team',
        'featured': True,
        'draft': False,
        'quality_score': article_data['quality_score'],
        'anti_ai_score': article_data['anti_ai_score']
    }
    
    # 创建目录
    os.makedirs(os.path.dirname(article_path), exist_ok=True)
    
    # 写入文件
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write(yaml.dump(front_matter, default_flow_style=False, allow_unicode=True))
        f.write('---\n\n')
        f.write(article_data['content'])
    
    return article_path

def generate_success_report(successful, failed, articles):
    """生成成功报告"""
    
    report = f"""🎯 **每日内容生成报告** - {datetime.now().strftime('%Y-%m-%d')}

📊 **生成统计**
• 成功生成: {successful} 篇
• 生成失败: {failed} 篇  
• 成功率: {(successful/(successful+failed)*100):.1f}%

📝 **生成文章**"""
    
    for article in articles:
        report += f"""
• {article['title']}
  - 关键词: {article['keyword']}
  - 质量分: {article['quality_score']:.2f}
  - AI检测分: {article['anti_ai_score']:.2f}"""
    
    report += f"\n\n✅ 网站已自动更新部署"
    return report

if __name__ == "__main__":
    main()
```

## 🔐 阶段三：安全与配置

### Step 7: 环境变量配置
```bash
# config/secrets.env.example
# 复制为 secrets.env 并填入真实值

# Telegram通知
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Google服务
GOOGLE_ANALYTICS_ID=G-XXXXXXXXX
GOOGLE_ADSENSE_ID=ca-pub-XXXXXXXXX
GOOGLE_SEARCH_CONSOLE_KEY=path/to/service-account.json

# OpenAI API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx

# 联盟营销
AMAZON_ASSOCIATE_TAG=yourtag-20
AMAZON_API_KEY=your_amazon_api_key

# 网站配置
SITE_URL=https://your-domain.com
SITE_TITLE=AI Discovery

# 自动化参数
DAILY_CONTENT_QUOTA=2
QUALITY_THRESHOLD=0.8
ANTI_AI_THRESHOLD=0.75
```

### Step 8: GitHub Secrets配置
```bash
# 在GitHub仓库中配置以下Secrets:

# Vercel部署
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id  
VERCEL_PROJECT_ID=your_project_id

# API密钥
OPENAI_API_KEY=sk-xxxxxxxxx
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Google服务
GOOGLE_ANALYTICS_ID=G-XXXXXXXXX
GOOGLE_ADSENSE_ID=ca-pub-XXXXXXXXX

# 网站配置
SITE_URL=https://your-domain.com
```

## 📊 阶段四：监控与优化

### Step 9: 监控系统部署
```python
# scripts/health_monitor.py
#!/usr/bin/env python3
"""网站健康监控脚本"""

import requests
import time
from datetime import datetime
from config_manager import ConfigManager
from telegram_notifier import TelegramNotifier

class HealthMonitor:
    """健康监控器"""
    
    def __init__(self, config):
        self.config = config
        self.notifier = TelegramNotifier(config)
        
        self.health_checks = [
            self.check_site_accessibility,
            self.check_page_load_speed,
            self.check_content_freshness,
            self.check_error_rates
        ]
    
    def run_health_check(self):
        """执行健康检查"""
        
        health_report = {
            'timestamp': datetime.now(),
            'site_url': self.config.get('site_url'),
            'checks_passed': 0,
            'checks_failed': 0,
            'issues': []
        }
        
        for check in self.health_checks:
            try:
                result = check()
                if result['status'] == 'pass':
                    health_report['checks_passed'] += 1
                else:
                    health_report['checks_failed'] += 1
                    health_report['issues'].append(result)
            
            except Exception as e:
                health_report['checks_failed'] += 1
                health_report['issues'].append({
                    'check': check.__name__,
                    'status': 'error',
                    'message': str(e)
                })
        
        # 发送报告
        self.send_health_report(health_report)
        
        return health_report
    
    def check_site_accessibility(self):
        """检查网站可访问性"""
        
        try:
            response = requests.get(
                self.config.get('site_url'),
                timeout=10,
                headers={'User-Agent': 'HealthMonitor/1.0'}
            )
            
            if response.status_code == 200:
                return {'check': 'site_accessibility', 'status': 'pass'}
            else:
                return {
                    'check': 'site_accessibility',
                    'status': 'fail',
                    'message': f'HTTP {response.status_code}'
                }
        
        except Exception as e:
            return {
                'check': 'site_accessibility',
                'status': 'fail', 
                'message': str(e)
            }
    
    def send_health_report(self, report):
        """发送健康报告"""
        
        total_checks = report['checks_passed'] + report['checks_failed']
        health_percentage = (report['checks_passed'] / total_checks) * 100
        
        if health_percentage < 75:
            emoji = "🚨"
            status = "CRITICAL"
        elif health_percentage < 90:
            emoji = "⚠️"
            status = "WARNING"
        else:
            emoji = "✅"
            status = "HEALTHY"
        
        message = f"""{emoji} **网站健康检查** - {status}

🌐 网站: {report['site_url']}
📊 健康度: {health_percentage:.1f}%
✅ 通过检查: {report['checks_passed']}
❌ 失败检查: {report['checks_failed']}

⏰ 检查时间: {report['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}"""

        if report['issues']:
            message += "\n\n🔍 **发现问题:**"
            for issue in report['issues']:
                message += f"\n• {issue['check']}: {issue.get('message', 'Unknown error')}"
        
        self.notifier.send_message(message)

if __name__ == "__main__":
    config = ConfigManager()
    monitor = HealthMonitor(config)
    monitor.run_health_check()
```

### Step 10: 性能优化脚本
```python
# scripts/performance_optimizer.py
#!/usr/bin/env python3
"""性能优化脚本"""

import os
import subprocess
from pathlib import Path
from config_manager import ConfigManager

class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, config):
        self.config = config
        
    def optimize_images(self):
        """优化图片文件"""
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        optimized_count = 0
        
        for root, dirs, files in os.walk('static/images'):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    file_path = os.path.join(root, file)
                    
                    # 使用imagemin优化图片
                    try:
                        result = subprocess.run([
                            'npx', 'imagemin', file_path,
                            '--out-dir', os.path.dirname(file_path),
                            '--plugin.webp.quality=80'
                        ], capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            optimized_count += 1
                    
                    except Exception as e:
                        print(f"优化图片失败 {file_path}: {e}")
        
        return optimized_count
    
    def minify_css_js(self):
        """压缩CSS和JS文件"""
        
        # Hugo构建时自动处理
        result = subprocess.run([
            'hugo', '--minify', '--environment', 'production'
        ], capture_output=True, text=True)
        
        return result.returncode == 0
    
    def generate_webp_images(self):
        """生成WebP格式图片"""
        
        converted_count = 0
        
        for root, dirs, files in os.walk('static/images'):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    source_path = os.path.join(root, file)
                    webp_path = os.path.splitext(source_path)[0] + '.webp'
                    
                    if not os.path.exists(webp_path):
                        try:
                            subprocess.run([
                                'cwebp', '-q', '80', source_path, '-o', webp_path
                            ], check=True)
                            converted_count += 1
                        
                        except subprocess.CalledProcessError:
                            print(f"转换WebP失败: {source_path}")
        
        return converted_count

if __name__ == "__main__":
    config = ConfigManager()
    optimizer = PerformanceOptimizer(config)
    
    print("🚀 开始性能优化...")
    
    optimized_images = optimizer.optimize_images()
    print(f"✅ 优化图片: {optimized_images} 个")
    
    css_js_success = optimizer.minify_css_js()
    print(f"✅ CSS/JS压缩: {'成功' if css_js_success else '失败'}")
    
    webp_converted = optimizer.generate_webp_images()
    print(f"✅ WebP转换: {webp_converted} 个")
    
    print("🎉 性能优化完成!")
```

## 🚀 阶段五：上线部署

### Step 11: 域名和SSL配置
```bash
# 1. 在Vercel中配置自定义域名
# 登录Vercel Dashboard → 选择项目 → Settings → Domains
# 添加自定义域名: your-domain.com

# 2. 配置DNS记录 (在域名提供商处)
# A记录: @ → 76.76.19.61 (Vercel IP)
# CNAME记录: www → your-project.vercel.app

# 3. 等待DNS生效和SSL证书自动配置
```

### Step 12: Google服务集成
```html
<!-- layouts/partials/head.html -->
<head>
    <!-- 基础Meta标签 -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!-- SEO Meta标签 -->
    <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>
    <meta name="description" content="{{ .Description | default .Site.Params.description }}">
    <meta name="keywords" content="{{ delimit .Keywords ", " }}">
    <meta name="author" content="{{ .Site.Params.author }}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ .Title }}">
    <meta property="og:description" content="{{ .Description }}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{{ .Permalink }}">
    
    <!-- Google Analytics -->
    {{ if .Site.Params.google_analytics_id }}
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ .Site.Params.google_analytics_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ .Site.Params.google_analytics_id }}');
    </script>
    {{ end }}
    
    <!-- Google AdSense -->
    {{ if .Site.Params.google_adsense_id }}
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={{ .Site.Params.google_adsense_id }}" crossorigin="anonymous"></script>
    {{ end }}
    
    <!-- 结构化数据 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{{ .Site.Title }}",
      "url": "{{ .Site.BaseURL }}",
      "description": "{{ .Site.Params.description }}",
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "{{ .Site.BaseURL }}search?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    }
    </script>
</head>
```

### Step 13: 最终部署验证
```bash
# 部署前检查清单
echo "🔍 执行部署前检查..."

# 1. 配置验证
python scripts/config_validator.py

# 2. 内容构建测试
hugo --environment production --destination public-test

# 3. 链接检查
echo "检查内部链接..."
# 可使用工具如 linkchecker

# 4. 性能测试
echo "执行性能测试..."
python scripts/performance_test.py

# 5. SEO检查
echo "SEO基础检查..."
python scripts/seo_validator.py

# 6. 最终部署
echo "🚀 开始部署..."
git add .
git commit -m "🎉 Production deployment $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo "✅ 部署完成!"
echo "🌐 网站地址: https://your-domain.com"
echo "📊 Analytics: https://analytics.google.com"
echo "🔍 Search Console: https://search.google.com/search-console"
```

## 📊 阶段六：运营监控

### Step 14: 建立监控仪表板
```python
# scripts/create_monitoring_dashboard.py
#!/usr/bin/env python3
"""创建监控仪表板"""

import json
from datetime import datetime, timedelta
from config_manager import ConfigManager

def create_dashboard_config():
    """创建仪表板配置"""
    
    dashboard_config = {
        "dashboard_info": {
            "title": "AI Discovery 运营仪表板",
            "description": "网站性能和收入监控",
            "update_frequency": "每小时更新"
        },
        
        "metrics": {
            "traffic": {
                "daily_visitors": {"target": 1000, "current": 0},
                "page_views": {"target": 3000, "current": 0},
                "bounce_rate": {"target": 45, "current": 0},
                "avg_session_duration": {"target": 180, "current": 0}
            },
            
            "content": {
                "total_articles": {"target": 100, "current": 0},
                "daily_content_quota": {"target": 2, "current": 0},
                "avg_quality_score": {"target": 0.85, "current": 0},
                "avg_anti_ai_score": {"target": 0.80, "current": 0}
            },
            
            "revenue": {
                "daily_revenue": {"target": 50, "current": 0},
                "monthly_revenue": {"target": 1500, "current": 0},
                "adsense_rpm": {"target": 3.0, "current": 0},
                "affiliate_conversion": {"target": 0.12, "current": 0}
            },
            
            "seo": {
                "indexed_pages": {"target": 95, "current": 0},
                "avg_position": {"target": 15, "current": 0},
                "click_through_rate": {"target": 0.08, "current": 0},
                "organic_traffic_growth": {"target": 0.15, "current": 0}
            }
        }
    }
    
    # 保存配置
    with open('data/dashboard_config.json', 'w') as f:
        json.dump(dashboard_config, f, indent=2, ensure_ascii=False)
    
    return dashboard_config

if __name__ == "__main__":
    config = create_dashboard_config()
    print("📊 监控仪表板配置创建完成!")
    print(f"配置文件: data/dashboard_config.json")
```

## 🎯 部署后验证清单

### 功能验证
```bash
验证清单:
□ 网站可正常访问
□ HTTPS证书有效
□ 搜索功能工作正常
□ 移动端显示正确
□ Google Analytics追踪正常
□ AdSense广告显示
□ 内部链接无404错误
□ Sitemap生成正确
□ RSS源工作正常
□ 联系表单功能正常(如有)
```

### 性能验证
```bash
性能指标:
□ 页面加载时间 < 3秒
□ 首次内容绘制 < 1.5秒
□ 最大内容绘制 < 2.5秒
□ 累积布局偏移 < 0.1
□ 首次输入延迟 < 100ms
□ Google PageSpeed分数 > 90
□ GTmetrix评级 > A
```

### SEO验证
```bash
SEO检查:
□ 所有页面有唯一标题
□ Meta描述长度适中
□ H1-H6标签层次正确
□ 图片包含Alt属性
□ 结构化数据无错误
□ robots.txt可访问
□ Sitemap提交成功
□ Google Search Console验证
```

## 🚨 故障排除指南

### 常见问题解决
```bash
# 1. Hugo构建失败
hugo --debug --verbose
# 检查模板语法和配置错误

# 2. Python脚本执行失败
python -m pip install -r requirements.txt --upgrade
# 更新依赖包

# 3. Vercel部署失败
vercel --debug
# 检查构建日志

# 4. 内容生成质量低
# 调整 config/secrets.env 中的质量阈值
QUALITY_THRESHOLD=0.75
ANTI_AI_THRESHOLD=0.70

# 5. API调用频率限制
# 增加重试间隔和缓存使用
```

## 🎉 部署完成

恭喜！您已成功部署AI Discovery全自动化AI工具发现平台。

### 下一步行动
1. **监控网站表现** - 关注Analytics和Search Console数据
2. **优化内容质量** - 根据用户反馈调整内容生成参数
3. **扩展关键词库** - 持续发现新的高价值关键词
4. **增强变现效果** - A/B测试不同的广告位置和联盟推荐
5. **建立品牌影响力** - 通过高质量内容建立行业权威性

### 技术支持
- 📚 查看项目文档了解详细配置
- 🐛 遇到问题请检查GitHub Actions日志
- 💬 使用Telegram监控接收实时通知
- 📊 定期查看监控仪表板了解网站健康状况

---

**成功部署是成功运营的第一步！** 🚀🎯