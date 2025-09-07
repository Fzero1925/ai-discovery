# AI Discovery 域名注册配置指南

**准备时间**: 2025-09-07  
**计划执行**: 2025-09-09 (2天后)  
**预计用时**: 30-60分钟

---

## 📋 **域名注册前准备清单**

### ✅ **当前网站状态确认**
- [x] 网站正常运行: https://ai-discovery-nu.vercel.app/
- [x] 108个英文页面完整
- [x] Vercel部署系统稳定
- [x] 内容质量达到专业标准
- [x] SEO优化完成

### 🎯 **推荐域名选项 (按优先级)**

#### 首选域名 (.com 后缀)
1. **ai-discovery.com** - 最直接，品牌匹配度最高
2. **aidiscovery.com** - 简洁，易记
3. **aitooldiscovery.com** - 更明确的定位

#### 备选域名 (.io/.ai/.tech 后缀)
4. **ai-discovery.io** - 科技感强，适合AI领域
5. **discover-ai.com** - 简洁动感
6. **aidiscovery.ai** - AI专用域名，高端但较贵

### 💰 **预算估算**
- **.com域名**: $12-15/年
- **.io域名**: $35-50/年  
- **.ai域名**: $80-200/年
- **DNS管理**: 通常免费（Vercel提供）
- **SSL证书**: 免费（Let's Encrypt）

---

## 🛠️ **详细配置步骤**

### 第1步: 域名注册 (5-10分钟)
```bash
推荐注册商:
1. Namecheap - 价格实惠，界面友好
2. GoDaddy - 知名品牌，服务完善
3. Cloudflare Registrar - 成本价域名，无额外费用
4. Google Domains - Google生态集成

注册流程:
1. 搜索可用域名
2. 添加到购物车
3. 完成支付
4. 保存域名管理信息
```

### 第2步: DNS配置 (10-15分钟)
```bash
在域名注册商控制台:
1. 找到DNS管理 / Name Servers设置
2. 配置以下记录:

A记录:
@ (root domain) → 76.76.21.21 (Vercel IP)
www → 76.76.21.21

CNAME记录:
www → ai-discovery-nu.vercel.app

或者使用Vercel DNS:
Name Servers设置为:
ns1.vercel-dns.com
ns2.vercel-dns.com
```

### 第3步: Vercel域名绑定 (5-10分钟)
```bash
在Vercel控制台:
1. 进入ai-discovery项目
2. Settings → Domains
3. 添加自定义域名:
   - 主域名: ai-discovery.com
   - www别名: www.ai-discovery.com
4. 等待DNS验证通过
5. 启用HTTPS自动证书
```

### 第4步: 更新项目配置 (5分钟)
```bash
更新文件:
1. config.toml - 修改baseURL
2. vercel.json - 添加域名重定向
3. robots.txt - 更新站点地址
4. sitemap.xml - 更新域名引用
```

### 第5步: 搜索引擎配置 (10-15分钟)
```bash
Google Search Console:
1. 添加新域名属性
2. 验证域名所有权
3. 提交新sitemap
4. 设置域名偏好 (www vs non-www)

Google Analytics:
1. 更新跟踪域名设置
2. 测试数据收集
```

---

## 🎯 **配置文件更新模板**

### config.toml 更新
```toml
# 原配置 (当前)
baseURL = 'https://ai-discovery-nu.vercel.app/'

# 新配置 (域名后)
baseURL = 'https://ai-discovery.com/'
```

### vercel.json 域名重定向
```json
{
  "routes": [
    {
      "src": "/(.*)",
      "headers": {
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff"
      }
    }
  ],
  "redirects": [
    {
      "source": "https://ai-discovery-nu.vercel.app/(.*)",
      "destination": "https://ai-discovery.com/$1",
      "permanent": true
    }
  ]
}
```

---

## ⚠️ **重要注意事项**

### DNS传播时间
- **预计等待**: 4-24小时
- **全球生效**: 最多48小时
- **建议**: 在低流量时段执行

### SSL证书
- **Vercel自动**: Let's Encrypt免费证书
- **激活时间**: 域名验证后5-15分钟
- **续期**: 自动续期，无需手动操作

### 流量影响
- **SEO过渡**: 使用301重定向最小化影响
- **Analytics**: 短期数据可能受影响
- **用户体验**: 透明切换，用户无感知

---

## 📊 **验收测试清单**

### 域名访问测试
- [ ] 主域名可正常访问
- [ ] www子域名正确重定向
- [ ] HTTPS证书正常加载
- [ ] 所有页面链接正常

### SEO检查
- [ ] 搜索引擎可以抓取新域名
- [ ] robots.txt正确配置
- [ ] sitemap.xml更新完成
- [ ] 301重定向设置正确

### 功能测试  
- [ ] 图片加载正常
- [ ] CSS/JS资源加载正常
- [ ] 表单功能正常
- [ ] 内链跳转正常

---

## 🚀 **后续优化建议**

### 品牌一致性
- 更新社交媒体链接
- 修改邮件签名
- 更新商业文档

### SEO提升
- 监控排名变化
- 更新外链指向
- 优化社交分享卡片

### 性能监控
- 设置新域名监控
- 更新Telegram通知配置
- 配置错误日志收集

---

## 📞 **问题排查指南**

### 常见问题
1. **DNS未生效**: 等待24-48小时传播
2. **SSL证书错误**: 检查域名验证状态
3. **重定向循环**: 检查DNS CNAME设置
4. **404错误**: 确认Vercel项目绑定正确

### 紧急联系
- **Vercel支持**: 在线文档 + 社区论坛
- **域名注册商**: 客服热线（保存注册信息）
- **DNS检查工具**: whatsmydns.net

---

**执行时间表**:
- **2025-09-09 上午**: 域名注册和基础配置
- **2025-09-09 下午**: DNS配置和Vercel绑定  
- **2025-09-10**: 验证和优化
- **2025-09-11**: 搜索引擎更新

**预期结果**: 从ai-discovery-nu.vercel.app成功迁移到专业自定义域名，提升品牌形象和SEO效果。