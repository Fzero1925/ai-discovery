# AI Discovery - GitHub Actions 工作流

这个目录包含了AI Discovery平台的所有自动化工作流配置，实现24/7全自动内容生成和部署。

## 🔄 工作流概览

### 1. Daily Content Generation (`daily-content-generation.yml`)
**用途：** 每日自动生成AI工具评测内容
- **触发时间：** 每天UTC时间2:00（北京时间10:00）
- **功能：**
  - 使用Google Trends分析热门AI工具关键词
  - 生成高质量、反AI检测的评测文章
  - 自动提交到GitHub仓库
  - 部署到GitHub Pages

### 2. Vercel Deployment (`vercel-deployment.yml`)
**用途：** 自动部署到Vercel生产环境
- **触发条件：** 推送到main分支或Pull Request
- **功能：**
  - 构建Hugo静态网站
  - 部署到Vercel（预览/生产环境）
  - 运行健康检查
  - 生成部署报告

### 3. Quality Monitoring (`quality-monitoring.yml`)
**用途：** 网站质量监控和SEO检查
- **触发时间：** 每天6:00和18:00 UTC
- **功能：**
  - HTML结构验证
  - SEO优化检查
  - 性能指标分析
  - 生成质量报告

### 4. Manual Content Update (`manual-content-update.yml`)
**用途：** 手动触发的内容生成和部署
- **触发方式：** GitHub Actions页面手动触发
- **功能：**
  - 指定特定AI工具生成内容
  - 强制重新生成现有内容
  - 立即部署选项

## 🔧 环境变量配置

在GitHub仓库设置中需要配置以下Secrets：

### 必需配置
```bash
# Vercel部署
VERCEL_TOKEN=your_vercel_token
VERCEL_ORG_ID=your_org_id  
VERCEL_PROJECT_ID=your_project_id

# GitHub Token (自动提供)
GITHUB_TOKEN=automatic
```

### 可选配置
```bash
# Telegram通知 (如果需要)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 其他第三方服务API密钥
```

## 🚀 部署流程

### 自动部署流程
1. **内容生成** → 2. **质量检查** → 3. **Hugo构建** → 4. **Vercel部署** → 5. **健康检查**

### 手动部署流程
1. 在GitHub Actions页面选择"Manual Content Update"
2. 填写参数（工具名称、是否强制重新生成等）
3. 点击"Run workflow"
4. 系统自动完成内容生成和部署

## 📊 工作流状态监控

### 状态徽章
可以在README中添加状态徽章来监控工作流状态：

```markdown
[![Daily Content Generation](https://github.com/Fzero1925/ai-discovery/actions/workflows/daily-content-generation.yml/badge.svg)](https://github.com/Fzero1925/ai-discovery/actions/workflows/daily-content-generation.yml)

[![Vercel Deployment](https://github.com/Fzero1925/ai-discovery/actions/workflows/vercel-deployment.yml/badge.svg)](https://github.com/Fzero1925/ai-discovery/actions/workflows/vercel-deployment.yml)

[![Quality Monitoring](https://github.com/Fzero1925/ai-discovery/actions/workflows/quality-monitoring.yml/badge.svg)](https://github.com/Fzero1925/ai-discovery/actions/workflows/quality-monitoring.yml)
```

### 日志和报告
- 每个工作流都会生成详细的执行日志
- 质量监控工作流会生成质量报告artifact
- 部署工作流会在步骤摘要中显示部署URL

## 🛠️ 故障排除

### 常见问题

#### 1. Content Generation失败
```bash
# 检查Python依赖
pip install -r requirements.txt

# 检查Google Trends连接
python test_keyword_analyzer.py

# 检查内容生成器
python test_content_generator.py
```

#### 2. Hugo构建失败
```bash
# 本地测试
hugo server -D

# 检查配置文件
hugo config
```

#### 3. Vercel部署失败
```bash
# 检查Vercel配置
vercel --version

# 验证环境变量
echo $VERCEL_TOKEN
```

### 调试技巧

1. **启用调试模式：** 在工作流中设置 `ACTIONS_STEP_DEBUG: true`
2. **查看artifacts：** 下载质量报告和构建产物
3. **本地复现：** 使用相同的命令在本地环境测试
4. **分步执行：** 使用手动触发工作流逐步测试

## 📈 性能优化

### 缓存策略
- Python包缓存：减少依赖安装时间
- Hugo模块缓存：提升构建速度
- Node.js缓存：加速Vercel部署

### 并发策略
- 工作流之间独立运行，避免相互干扰
- 使用条件执行，避免不必要的步骤

### 资源使用
- 每个工作流都设置了合理的超时时间
- 使用最新的Ubuntu runners确保性能
- 适当的频率设置避免GitHub Actions配额耗尽

## 📋 维护计划

### 定期维护任务
- **每周：** 检查工作流执行状态和失败率
- **每月：** 更新依赖版本（Hugo、Python包等）
- **每季度：** 评估和优化工作流性能
- **年度：** 检查GitHub Actions配额使用情况

### 升级计划
- 根据Hugo新版本更新构建配置
- 根据GitHub Actions新功能优化工作流
- 根据Vercel平台更新调整部署策略

---

**注意：** 所有工作流都经过本地测试验证，确保在生产环境中稳定运行。如有问题，请查看GitHub Actions日志或联系维护人员。