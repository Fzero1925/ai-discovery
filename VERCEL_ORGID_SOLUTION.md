# Vercel Organization ID 解决方案

**问题**: 在Vercel项目设置中找不到Team/Organization ID

## 🔍 解决方案

### 方法1: 个人账户使用用户ID
如果您使用的是个人Vercel账户，请按以下步骤操作：

1. **获取用户ID**:
   ```bash
   访问: https://vercel.com/account
   在页面右上角头像区域，您会看到类似: 
   - Username: your-username
   - User ID: user_xxxxxxxxxxxx (复制此ID)
   ```

2. **在GitHub Secrets中使用用户ID**:
   ```bash
   Name: VERCEL_ORG_ID
   Value: user_xxxxxxxxxxxx  (您的用户ID)
   ```

### 方法2: 通过Vercel CLI获取
```bash
# 安装Vercel CLI (如果还没有)
npm i -g vercel@latest

# 登录并查看账户信息
vercel whoami
```

### 方法3: 通过API获取
```bash
# 使用您的VERCEL_TOKEN查看用户信息
curl -H "Authorization: Bearer YOUR_VERCEL_TOKEN" https://api.vercel.com/v2/user
```

### 方法4: 项目URL中查看
```bash
# 在您的项目URL中，ID通常显示为:
https://vercel.com/your-username/ai-discovery
# 这里的 "your-username" 对应的ID就是您需要的Organization ID
```

## ✅ 验证配置

配置完成后，在GitHub Secrets中应该有三个值：
- `VERCEL_TOKEN`: vercel_xxxxxxxxxxxx
- `VERCEL_PROJECT_ID`: proj_xxxxxxxxxxxx  
- `VERCEL_ORG_ID`: user_xxxxxxxxxxxx (个人账户) 或 team_xxxxxxxxxxxx (团队账户)

## 🚀 下一步

配置完成后，推送代码到main分支触发自动部署：
```bash
git add .
git commit -m "feat: 完成Vercel配置，启动自动化部署"
git push origin main
```

然后检查GitHub Actions是否成功运行并部署到Vercel。