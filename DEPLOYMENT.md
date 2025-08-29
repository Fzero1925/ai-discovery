# AI Compass 部署指南

## 🚀 快速部署步骤

### 1. 准备 GitHub 仓库

```bash
# 创建 GitHub 仓库 (通过 GitHub 网页界面)
# 仓库名称: ai-compass
# 用户: Fzero1925
```

### 2. 推送代码到 GitHub

```bash
# 初始化 Git 仓库 (如果还未初始化)
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit: AI Compass 文章平台 - 2025-01-16

🎯 主要功能:
- 完整的文章平台架构
- 8分类文章系统 (image-ai, text-ai, productivity 等)
- 4篇高质量示例文章
- Pagefind 全站搜索
- Google Analytics 集成
- SEO 优化和结构化数据
- 响应式设计

🔧 技术栈:
- Astro + TypeScript
- Tailwind CSS
- Pagefind 搜索
- GitHub Pages 部署

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 设置远程仓库
git branch -M main
git remote add origin https://github.com/Fzero1925/ai-compass.git

# 推送到 GitHub
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入 GitHub 仓库页面
2. 点击 **Settings** 标签
3. 在左侧菜单中找到 **Pages**
4. 在 **Source** 下选择 **GitHub Actions**
5. 系统会自动检测到 Astro 项目并建议工作流程

### 4. GitHub Actions 配置

项目已包含 `.github/workflows/deploy.yml` 配置文件，支持：
- 自动构建和部署
- Pagefind 搜索索引生成
- 静态资源优化

### 5. 环境变量配置

在 GitHub 仓库设置中配置以下环境变量：

**Repository Settings > Secrets and Variables > Actions > Variables**

```
PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX  # 可选，Google Analytics 追踪 ID
PUBLIC_SITE_URL=https://fzero1925.github.io/ai-compass
PUBLIC_SITE_NAME=AI Compass
```

### 6. 验证部署

部署完成后，访问以下 URL 验证功能：

- **主站**: https://fzero1925.github.io/ai-compass
- **文章列表**: https://fzero1925.github.io/ai-compass/articles
- **示例文章**: https://fzero1925.github.io/ai-compass/articles/chatgpt-advanced-guide
- **搜索功能**: 在任意页面按 Ctrl+K 测试搜索
- **Sitemap**: https://fzero1925.github.io/ai-compass/sitemap.xml

## 🔧 本地开发

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/Fzero1925/ai-compass.git
cd ai-compass

# 安装依赖
npm install

# 复制环境变量文件
cp .env.example .env
# 编辑 .env 文件添加你的配置

# 启动开发服务器
npm run dev
```

### 构建和测试

```bash
# 构建生产版本
npm run build

# 预览生产版本
npm run preview

# 验证搜索功能
# 构建后会在 dist/pagefind 目录生成搜索索引
```

## 📊 SEO 和分析设置

### Google Analytics 配置

1. 创建 Google Analytics 账户
2. 获取追踪 ID (格式: G-XXXXXXXXXX)
3. 在 GitHub 仓库变量中设置 `PUBLIC_GOOGLE_ANALYTICS_ID`
4. 重新部署以启用追踪

### Google Search Console

1. 访问 [Google Search Console](https://search.google.com/search-console)
2. 添加网站属性: `https://fzero1925.github.io/ai-compass`
3. 验证网站所有权
4. 提交 Sitemap: `https://fzero1925.github.io/ai-compass/sitemap.xml`

### 搜索引擎提交

手动提交网站到主要搜索引擎：
- **百度**: [百度站长平台](https://ziyuan.baidu.com)
- **搜狗**: [搜狗站长平台](http://zhanzhang.sogou.com)
- **360**: [360搜索站长平台](https://zhanzhang.so.com)

## 📝 内容管理

### 添加新文章

1. 在 `src/data/articles.ts` 中添加文章元数据
2. 在 `src/pages/articles/` 中创建新的 `.astro` 文件
3. 使用 `ArticleLayout` 模板
4. 提交并推送到 GitHub，自动部署

### 图片管理

- 图片存放在 `public/images/articles/` 目录
- 遵循 `IMAGE-GUIDELINES.md` 中的规格标准
- 优先使用 WebP 格式
- 文件大小控制在合理范围内

### 搜索索引更新

搜索索引会在每次构建时自动更新，包含：
- 文章标题和内容
- 分类和标签信息
- 中文搜索支持

## 🛠️ 故障排除

### 常见问题

**Q: 构建失败，提示 CSS 类不存在**
```bash
# 检查 Tailwind 配置是否包含所需的颜色类
# 查看 tailwind.config.mjs 中的 colors 配置
```

**Q: 搜索功能不工作**
```bash
# 确保构建时执行了 Pagefind
npm run build
# 检查 dist/pagefind 目录是否存在
```

**Q: Analytics 数据不显示**
```bash
# 确认环境变量设置正确
# 检查浏览器开发者工具中的网络请求
# 验证 GA 追踪代码是否正确加载
```

### 性能优化

- 启用 GitHub Pages 的 CDN 缓存
- 优化图片大小和格式
- 监控 Google PageSpeed Insights 评分
- 定期清理未使用的 CSS 类

## 📋 部署检查清单

- [ ] GitHub 仓库创建并推送代码
- [ ] GitHub Pages 启用并配置
- [ ] 环境变量设置正确
- [ ] 网站可正常访问
- [ ] 搜索功能工作正常
- [ ] 所有文章页面加载正常
- [ ] 移动端显示正常
- [ ] Google Analytics 追踪正常
- [ ] Sitemap 生成正确
- [ ] SEO 元标签检查通过

---

**部署文档版本**: v1.0  
**最后更新**: 2025年1月16日  
**维护者**: AI Compass Team