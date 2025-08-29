# GitHub 仓库创建步骤

## 步骤1: 创建GitHub仓库

1. 访问 https://github.com/new
2. 仓库名设置为: `ai-compass`
3. 描述: `AI工具目录与点评平台 - 发现最优质的AI工具，获得专业点评与对比分析`
4. 设置为 **Public**（GitHub Pages免费版需要公开仓库）
5. **不要**勾选 "Add a README file"
6. **不要**勾选 "Add .gitignore" 
7. **不要**选择 "Choose a license"
8. 点击 "Create repository"

## 步骤2: 推送本地代码

创建仓库后，在本地运行以下命令：

```bash
# 进入项目目录
cd "D:\Users\claude\ai-compass"

# 添加远程仓库
git remote add origin https://github.com/Fzero1925/ai-compass.git

# 推送代码到GitHub
git push -u origin main
```

## 步骤3: 配置GitHub Pages

1. 进入仓库页面 https://github.com/Fzero1925/ai-compass
2. 点击 "Settings" 标签
3. 在左侧菜单中找到 "Pages"
4. 在 "Source" 部分选择 "GitHub Actions"
5. 保存设置

## 步骤4: 等待部署完成

- 推送代码后会自动触发部署
- 在 "Actions" 标签可以查看部署进度
- 首次部署大约需要 2-5 分钟
- 部署完成后访问: https://fzero1925.github.io/ai-compass/

## 验证部署成功

访问以下页面确认网站正常运行：
- 首页: https://fzero1925.github.io/ai-compass/
- 工具大全: https://fzero1925.github.io/ai-compass/tools/
- 图像工具: https://fzero1925.github.io/ai-compass/tools/image-tools/
- 工具详情: https://fzero1925.github.io/ai-compass/tools/image-tools/nano-banana/

## 如果遇到问题

1. **404 错误**: 检查 astro.config.mjs 中的 base 路径配置
2. **样式异常**: 清除浏览器缓存，等待CDN更新
3. **Actions失败**: 查看Actions日志，可能需要在仓库设置中启用Actions权限

需要帮助的话随时联系！