# 项目进度与 TODO（News‑First）

最近更新：2025‑09‑12

## 当前进度（已完成）
- 新增新闻一级栏目与模板：`content/news/`、`layouts/news/*`。
- 首页改为新闻优先，兼容旧 `category=news` 回退。
- NewsArticle 结构化数据适配 `section=news` 与 `category=news`。
- 自动化：短新闻采集写入 `content/news/`；新闻站点地图扫描 `news` 类别。
- 工作流：`hourly_news.yml` 增短新闻采集；发布器按 15 分钟节奏运行。
- 目录：`oldfile/` 与 `test/` 已忽略（不推送 GitHub）。

## 工作流概览
- `hourly_news.yml`：每小时 03 分入队 + 生成 News Sitemap + 提交。
- `quarter_hour_publisher.yml`：每 15 分钟发布到点草稿。
- `daily_news_report.yml` / `weekly_news_report.yml`：日报 / 周报。

## TODO（下一步）
1) Telegram 失败降级：Markdown→纯文本自动重试并记录错误 body。
2) Google News 收录优化：列表页元信息与站点地图分片（>100）。
3) 配置中心扩展：相似度阈值、昼夜上限与间隔范围统一放入 `data/scheduler_config.json`。
4) 报表增强：质量均分、相似度拒绝率、产发比、有效点击等指标。
5) 内链增强：新闻指向评测/专题的上下文自动内链。
6) 模板清理：统一 `_default` 残留乱码与中英混排符号。
7) 阈值报警：队列长度/发布失败等指标 Telegram 告警。

## 目录与忽略策略
- 生产：`content/`、`layouts/`、`modules/`、`scripts/`、`static/`。
- 测试：`test/`（pytest），不推送 GitHub。
- 归档：`oldfile/`（历史/过时文档），不推送 GitHub。

更多详情与优先级请参考根目录 `PROJECT_STATUS.md`（单一事实源）。

