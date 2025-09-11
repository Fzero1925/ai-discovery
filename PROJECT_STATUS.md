# 项目状态与待办（News‑First 架构）

更新时间：2025-09-12

## 概览
- 定位：以“科技新闻”为核心的自动化网站（News‑First）。
- 现状：新闻一级栏目已建立，首页已改为新闻优先，自动化采集/入队/发布与新闻站点地图已对齐。

## 已完成（Done）
- 新增新闻栏目与模板：`content/news/`、`layouts/news/list.html`、`layouts/news/single.html`。
- 首页聚焦新闻：`layouts/index.html` 以 `section=news` 为主，兼容 `category=news` 回退。
- NewsArticle 结构化数据：`layouts/partials/news-structured-data.html` 支持 `section=news` 与 `category=news`。
- 自动化对齐：
  - 短新闻采集：`scripts/ingest_news.py` 写入 `content/news/`。
  - 新闻站点地图：`scripts/generate_news_sitemap.py` 扫描所有 `news` 类别文章。
  - 工作流：`.github/workflows/hourly_news.yml` 增加短新闻采集步骤。
- 导航与文档：`config.toml` 菜单指向 `/news/`；`README.md` 增补 News‑First 说明。
- 目录与忽略：`.gitignore` 已忽略 `oldfile/` 与 `test/`（不推送 GitHub）。

## 进行中（In Progress）
- 质量/相似度阈值逐步调优（`data/scheduler_config.json`）。
- 评测/长文的发布节奏与短新闻配比策略观察期。

## 待办（Next / TODO）
1) Telegram 发送降级：失败时从 Markdown 自动降级纯文本，并记录错误 body（提升送达率）。
2) Google News 收录优化：完善 `/news/` 列表页元信息与分页站点地图分片策略（>100条时）。
3) 配置中心扩展：将相似度阈值、昼夜节奏、每小时上限、间隔范围开放到 `data/scheduler_config.json`（已部分支持）。
4) 报表增强：在日报/周报中加入质量均分、相似度拒绝率、产发比、有效点击等关键指标。
5) 内链增强：为新闻正文自动生成指向评测/专题的上下文内链（基于关键词/实体）。
6) 模板清理：逐步清理 `_default` 模板中残留乱码与中英混排符号，统一文案与样式。
7) 监控与报警：为发布器与队列长度设置阈值报警（Telegram）。

## 建议（Recommendations）
- 架构：保持“短新闻（广覆盖） + 长评测（深价值）”双轨，短新闻优先索引，长文支持变现。
- SEO：新闻卡片补充三段式摘要（what’s new / why it matters / context），提升点击与收录质量。
- 发布节奏：夜间建议进一步限流（2/小时→1/小时或延长间隔至 25–35 分钟），减轻低峰期构建压力。
- 代码卫生：中期移除未使用的 Astro 残留与无用脚本，降低维护成本（待确认影响面后执行）。

## 风险与依赖（Risks/Deps）
- 外部 API 配额（NewsAPI、图片源）可能限制吞吐量；已具本地/多源降级策略，仍需观察。
- GitHub Actions 构建配额与频率限制；若触顶需上调发布间隔或做合批。

## 目录与提交策略（Folders & VCS）
- 生产：`content/`、`layouts/`、`modules/`、`scripts/`、`static/`。
- 测试：`test/`（已在 `.gitignore`，不推送 GitHub）。
- 归档：`oldfile/`（过时/历史文档，已在 `.gitignore`，不推送 GitHub）。

## 快速命令（Local）
- 本地预览：`hugo serve --disableFastRender`
- 采集短新闻：`python scripts/ingest_news.py`
- 生成新闻站点地图：`SITE_BASE_URL=http://localhost:3000 python scripts/generate_news_sitemap.py`

— 本文件为当前状态与执行指引的“单一事实源（SoT）”，与 `README.md`、`docs/PROGRESS_TODO.md` 保持一致。

