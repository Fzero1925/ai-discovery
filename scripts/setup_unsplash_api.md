# Unsplash API 配置指南

## 🆓 Unsplash API 免费额度说明

✅ **完全免费使用**  
- 每小时：50次请求  
- 每月：5000次请求  
- 无需付费，注册即可使用  
- 对AI Discovery网站需求完全够用  

## 📋 配置步骤

### 1. 注册Unsplash开发者账号
1. 访问：https://unsplash.com/developers
2. 点击"Register as a developer"
3. 使用你的邮箱注册或GitHub登录

### 2. 创建应用获取API密钥
1. 登录后访问：https://unsplash.com/oauth/applications
2. 点击"New Application"
3. 同意开发者条款
4. 填写应用信息：
   - **Application name**: AI Discovery
   - **Description**: AI tools review website for fetching related images
   - **Website**: https://ai-discovery.vercel.app

### 3. 获取Access Key
创建应用后，你会看到：
- **Access Key** (这就是我们需要的API密钥)
- **Secret Key** (暂时不需要)

### 4. 配置环境变量
复制Access Key，然后运行以下命令：

```bash
# Windows (临时设置)
set UNSPLASH_ACCESS_KEY=你的Access Key

# 或者添加到 .env 文件中
echo UNSPLASH_ACCESS_KEY=你的Access Key >> .env
```

## 🎯 测试配置

配置完成后，运行测试脚本：
```bash
python scripts/test_unsplash_api.py
```

## ✅ 配置完成后的效果

- 每篇文章将获得与AI工具相关的真实图片
- 自动缓存图片，避免重复请求
- 支持批量处理所有文章
- 图片质量和相关性大幅提升

请按照以上步骤操作，获取Access Key后告诉我，我将继续配置真实图片获取系统。