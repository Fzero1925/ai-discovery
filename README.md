# AI Discovery 静态站点

AI Discovery 是聚焦 “AI 新闻 + AI 工具指南 + 机器人专题” 的英文内容站，目标是通过 Google AdSense 实现长期变现。生产仓库仅保留 Hugo 静态站点必需文件，后期维护只需上传符合模板的 Markdown 内容即可。

- **核心栏目**：`News`（新闻快讯与深度解读）、`Tools`（AI 工具评测与榜单）、`Robot`（工业/服务机器人专题）、`About`（品牌信息）。
- **运营策略**：保持高质量英文内容、合法合规的图片与结构化数据支持，提升 CPC 与收录效果。
- **导航配置**：见 `config.toml`，菜单顺序为 News → Tools → Robot → About。

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-discovery.git
cd ai-discovery

# 安装依赖（仅需 Hugo，如果需要 Tailwind 自定义则安装 Node）
npm install

# 本地预览
hugo server -D
```

> 备注：所有自动化脚本、数据处理、监控工具已迁移至仓库外的 `../ai-discovery-automation/` 目录，如需批量生成内容，可在本地或私有环境中运行，再将生成的 Markdown 拷贝回本仓库 `content/`。

## 内容发布流程（零维护）

1. 准备 Markdown 文件，补充 front matter：
   ```yaml
   ---
   title: "示例标题"
   description: "150 字以内摘要"
   date: 2025-09-20
   categories: ["news"]
   tags: ["ai", "robotics"]
   featured_image: "/images/sample.jpg"
   image_alt: "描述图片内容"
   draft: false
   ---
   ```
2. 根据栏目放入对应目录：
   - 新闻 → `content/news/`
   - 工具评测 → `content/reviews/`
   - 机器人专题 → `content/robot/`（可按 `industrial/`、`service/`、`research/` 建子目录）
3. 提交并推送，Vercel 自动构建发布。

## 目录结构

```
ai-discovery/
├── content/            # News / Tools / Robot / About 等 Markdown 内容
├── layouts/            # Hugo 模板（首页、列表、单页、partials 等）
├── static/             # 静态资源（CSS/JS/图片）
├── config/             # 站点配置补充文件
├── dev-docs/           # 内部规划文档（已加入 .gitignore，不推送 GitHub）
├── config.toml         # Hugo 主配置
├── README.md           # 本文档
└── vercel.json         # 部署配置
```

## 机器人栏目说明

- 访问 `/robot/` 即可查看机器人专题页，页面提供了 `Industrial`, `Service`, `Research` 三个锚点，便于定位内容。
- 上传内容时将 Markdown 放入对应子目录，Hugo 会基于 front matter 自动归档并生成页面。

## SEO 与合规

- 模板内置结构化数据、面包屑、站点地图、Lazy Load 等 SEO 能力，无需额外脚本。
- 上传图片时请确认版权与来源，并补充 `image_alt` 文本。
- `About` 页面建议提供品牌描述、联系方式、隐私/条款链接，满足 AdSense 审核要求。

## 常见命令

```bash
hugo server -D          # 本地预览
hugo --minify           # 生成生产环境静态文件（输出到 public/）
```

更多内部计划、路线图与待办事项详见 `dev-docs/` 目录中的 Markdown 文件（仅供团队参考）。
