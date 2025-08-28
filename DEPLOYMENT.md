# AI Compass 部署指南

## GitHub Pages 部署步骤

### 1. 创建 GitHub 仓库
1. 在 GitHub 上创建新仓库，命名为 `ai-compass`
2. 不要初始化 README、.gitignore 或 license（因为本地已有）

### 2. 推送代码到 GitHub
```bash
# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/ai-compass.git

# 添加所有文件
git add .

# 提交初始版本
git commit -m "Initial commit: AI Compass MVP with complete features

🎉 Features:
- Complete homepage with hero, categories, featured tools
- Tool detail pages with 6-module structure
- Category browsing (tools index, image tools)
- Responsive design with Tailwind CSS
- SEO optimized with meta tags
- TypeScript data management

📊 Pages:
- Homepage: /
- Tools overview: /tools/
- Image tools: /tools/image-tools/  
- Tool detail: /tools/image-tools/nano-banana/

🚀 Tech Stack:
- Astro + Tailwind CSS + TypeScript
- GitHub Pages deployment ready"

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 配置 GitHub Pages
1. 进入仓库的 Settings 标签
2. 在左侧菜单找到 "Pages" 
3. 在 "Source" 部分选择 "GitHub Actions"
4. 保存设置

### 4. 触发部署
- 代码推送后会自动触发部署流程
- 在 Actions 标签可以查看部署进度
- 部署成功后网站地址为: `https://YOUR_USERNAME.github.io/ai-compass/`

### 5. 自定义域名（可选）
如果有自定义域名：
1. 编辑 `public/CNAME` 文件，取消注释并填入域名
2. 在域名管理处添加 CNAME 记录指向 `YOUR_USERNAME.github.io`
3. 在 GitHub Pages 设置中验证域名

## 部署后验证

访问以下页面确认部署成功：
- 首页: `https://YOUR_USERNAME.github.io/ai-compass/`
- 工具大全: `https://YOUR_USERNAME.github.io/ai-compass/tools/`
- 图像工具: `https://YOUR_USERNAME.github.io/ai-compass/tools/image-tools/`
- 工具详情: `https://YOUR_USERNAME.github.io/ai-compass/tools/image-tools/nano-banana/`

## 后续更新

每次代码更新只需：
```bash
git add .
git commit -m "Update: 描述更新内容"
git push
```

GitHub Actions 会自动重新部署网站。

## 注意事项

1. **首次部署可能需要几分钟**：GitHub Pages 需要时间来构建和部署
2. **网站缓存**：更新后如果看不到变化，尝试强制刷新 (Ctrl+F5)
3. **域名配置**：如果使用自定义域名，确保 DNS 记录正确配置
4. **HTTPS**：GitHub Pages 自动提供 HTTPS，建议启用 "Enforce HTTPS"