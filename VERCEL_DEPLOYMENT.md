# AI Discovery - Vercel 部署指南

本文档指导如何将AI Discovery平台部署到Vercel，实现全球CDN加速和自动部署。

## 🚀 快速部署步骤

### 1. 准备工作

确保你已经：
- ✅ 拥有GitHub账户并且项目代码已推送
- ✅ 注册Vercel账户（推荐使用GitHub登录）
- ✅ 本地Hugo网站可以正常构建

### 2. 连接GitHub仓库

1. 登录 [Vercel控制台](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 选择 "Import Git Repository" 
4. 找到并选择 `ai-discovery` 仓库
5. 点击 "Import"

### 3. 配置项目设置

在Vercel项目配置页面：

#### Framework Preset
```
Framework: Hugo
Build Command: hugo --minify --environment production  
Output Directory: public
Install Command: npm install -g hugo-extended@0.149.0
```

#### Environment Variables
设置以下环境变量：
```bash
HUGO_VERSION=0.149.0
NODE_VERSION=18
HUGO_ENV=production
```

### 4. 高级配置

#### 构建设置
```json
{
  "buildCommand": "hugo --minify --environment production",
  "outputDirectory": "public", 
  "installCommand": "npm install -g hugo-extended@0.149.0",
  "devCommand": "hugo server -D --port 3000"
}
```

#### 域名配置
1. 在项目设置中找到 "Domains"
2. 添加自定义域名（等域名购买后配置）
3. 配置DNS记录指向Vercel

## 🔧 环境变量详解

### 必需环境变量

```bash
# Hugo构建
HUGO_VERSION=0.149.0          # Hugo版本
HUGO_ENV=production           # 生产环境

# Node.js
NODE_VERSION=18               # Node.js版本

# 可选：分析和追踪
GOOGLE_ANALYTICS_ID=          # Google Analytics追踪ID
ADSENSE_PUBLISHER_ID=         # AdSense发布商ID
```

### GitHub Actions集成变量

在GitHub仓库的 Settings > Secrets 中添加：

```bash
# Vercel部署
VERCEL_TOKEN=your_vercel_token          # Vercel API Token
VERCEL_ORG_ID=your_org_id               # 组织ID  
VERCEL_PROJECT_ID=your_project_id       # 项目ID
```

### 获取Vercel Token

1. 访问 [Vercel Account Settings](https://vercel.com/account/tokens)
2. 点击 "Create Token"
3. 命名为 "AI Discovery Deployment"
4. 复制生成的token

### 获取项目ID和组织ID

在Vercel项目设置页面，找到 "General" 标签：
- **Project ID**: 在项目设置中可找到
- **Team/Org ID**: 在团队设置中可找到

## 📊 部署验证

### 1. 自动部署测试

推送代码到main分支后：
```bash
git add .
git commit -m "test: Vercel部署测试"
git push
```

检查：
- Vercel控制台显示构建进度
- GitHub Actions工作流正常运行
- 部署成功后访问预览链接

### 2. 手动部署测试

在GitHub Actions中：
1. 选择 "Vercel Deployment" 工作流
2. 点击 "Run workflow"
3. 观察构建和部署过程

### 3. 功能验证清单

- [ ] 网站可以正常访问
- [ ] 所有页面加载正常
- [ ] CSS/JS资源加载正确
- [ ] 图片和静态资源正常
- [ ] 响应式设计在移动端正常
- [ ] SEO元标签正确显示

## 🌐 域名配置（待域名购买后）

### 1. DNS配置

购买域名后，配置以下DNS记录：

```dns
Type: A
Name: @
Value: 76.76.19.61 (Vercel IP)

Type: CNAME  
Name: www
Value: cname.vercel-dns.com
```

### 2. Vercel域名设置

1. 在Vercel项目中添加域名
2. 选择域名类型（Primary/Redirect）
3. 等待DNS传播（通常需要24-48小时）

### 3. SSL证书

Vercel自动提供：
- 免费SSL证书
- 自动续期
- HTTP到HTTPS自动重定向

## 📈 性能优化

### 1. CDN和缓存

Vercel自动提供：
- 全球CDN网络
- 智能静态资源缓存
- 图片自动优化

### 2. 构建优化

```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.149.0",
      "HUGO_ENABLEGITINFO": "true"
    }
  }
}
```

### 3. 预渲染优化

Hugo静态生成确保：
- 快速页面加载
- 优秀的SEO性能
- 低服务器资源消耗

## 🔍 监控和分析

### 1. Vercel Analytics

启用Vercel Analytics：
```json
{
  "analytics": {
    "enabled": true
  }
}
```

### 2. 性能监控

在Vercel控制台查看：
- 构建时间统计
- 带宽使用情况
- 访问量统计
- 错误日志

### 3. 第三方集成

- **Google Analytics**: 网站流量分析
- **Google Search Console**: SEO监控
- **Cloudflare**: 额外CDN加速（可选）

## 🛠️ 故障排除

### 常见问题

#### 1. Hugo构建失败
```bash
# 检查Hugo版本
hugo version

# 本地测试构建
hugo --minify --environment production
```

#### 2. 静态资源404
检查 `config.toml` 中的 `baseURL` 设置：
```toml
baseURL = "https://your-domain.com"  # 或Vercel提供的URL
```

#### 3. 环境变量不生效
确保在Vercel项目设置中正确配置所有环境变量

#### 4. GitHub Actions部署失败
验证Secrets配置：
- VERCEL_TOKEN是否有效
- PROJECT_ID和ORG_ID是否正确

### 调试技巧

1. **查看构建日志**: 在Vercel控制台查看详细构建日志
2. **本地复现**: 使用相同命令在本地环境测试
3. **分步调试**: 先本地构建成功再推送到远程

## 📋 部署检查清单

### 部署前
- [ ] 代码已推送到main分支
- [ ] 本地Hugo构建成功
- [ ] 所有必需的环境变量已配置
- [ ] GitHub Secrets配置完成

### 部署后
- [ ] Vercel项目构建成功
- [ ] 网站可以正常访问
- [ ] 所有页面和资源加载正常
- [ ] GitHub Actions工作流运行正常
- [ ] 性能指标符合预期

### 长期维护
- [ ] 定期检查构建状态
- [ ] 监控网站性能指标
- [ ] 更新Hugo版本和依赖
- [ ] 备份重要配置文件

## 🎯 下一步计划

1. **域名配置**: 5天后购买并配置域名
2. **SSL证书**: 自动配置HTTPS
3. **CDN优化**: 启用高级缓存策略
4. **监控告警**: 配置性能监控和告警
5. **备份策略**: 设置自动备份机制

---

**注意**: 
- Vercel免费计划提供100GB带宽/月
- Hugo静态网站构建速度快，资源消耗低
- 所有配置文件已针对性能和SEO优化

如有问题，请查看Vercel官方文档或联系技术支持。