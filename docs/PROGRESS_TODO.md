# 项目进度与TODO（生产/测试分离版）

更新时间：2025-09-11

## 当前进度（已上线）
- 新闻自动化全链路：
  - 每小时入队（5–8篇，质量≥85，去重相似度<0.82，按白天/夜间节奏分配发布时间）
  - 每15分钟自动发布（白天/夜间上限可配，默认白天6/小时，夜间2/小时）
  - News Sitemap 生成与 Google Ping；NewsArticle 结构化数据
  - Telegram 通知（入队/发布/日报/周报），通知失败不再阻塞工作流
- 质量与风控：
  - 质量闸门（字数/结构/图片alt/内链/人性化/元数据/可读性）
  - 相似度守门（TF‑IDF 余弦相似度阈值 0.82）
  - 活跃时段与夜间限流（`data/scheduler_config.json`）
- 文档与目录：
  - `oldfile/` 归档历史文档（不再上传）
  - `test/` 测试脚本迁出生产目录（不再上传）

## 工作流（已精简）
- `.github/workflows/hourly_news.yml`：每小时 03 分，入队 + 生成 News Sitemap + Ping + 提交
- `.github/workflows/quarter_hour_publisher.yml`：每 15 分钟发布到点草稿
- `.github/workflows/daily_news_report.yml`：每日 00:05（UTC）日报
- `.github/workflows/weekly_news_report.yml`：每周一 00:10（UTC）周报

说明：可合并日报/周报为一个 workflow，但需在脚本侧分辨时间并控制发送频率；目前分开更直观且易于维护。

## TODO（下一步）
1) Telegram 发送降级：Markdown 失败时自动改为纯文本重试，并打印错误 body，提升送达率
2) Google News 收录优化：新增栏目/导航页，增强新闻聚合与抓取信号
3) 配置中心扩展：将更多节奏/阈值参数开放到 `data/scheduler_config.json`（如相似度阈值、白天/夜间上限、间隔范围）
4) 报表增强：日报/周报加入质量均分、相似度拒绝率、产发比等关键指标
5) 构建节流策略（可选）：如平台构建上限紧张，将发布频率调至 20–30 分钟或启用批量发布策略

## 目录组织与忽略策略
- 生产代码与内容：保留在 `content/`、`scripts/`、`modules/`、`layouts/` 等生产目录
- 测试代码：已迁移至 `test/`，并在 `.gitignore` 中忽略
- 历史/过时文档：已迁移至 `oldfile/`，并在 `.gitignore` 中忽略

## 需要你确认的事项
- 是否同意将 Telegram 发送逻辑升级为“失败降级重试 + 错误 body 打印”？（不影响现有流程，仅提升稳定性）
- 是否需要把日报与周报合并到一个 workflow（脚本内根据日期判断，仅发一次对应报告）？
- 夜间策略是否需要进一步降低产量或延长间隔？（目前夜间 2/小时，20–30 分钟间隔）

