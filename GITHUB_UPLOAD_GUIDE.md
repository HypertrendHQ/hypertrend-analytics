# 📤 上传到 GitHub 指南

## 步骤 1: 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 填写信息：
   - **Repository name**: `hypertrend-analytics`
   - **Description**: `HyperTrend 链上信用分析 OpenClaw Skill`
   - **Visibility**: Public (推荐，方便分享)
   - **Initialize**: 不要勾选 (我们会上传本地文件)
3. 点击 **Create repository**

## 步骤 2: 上传本地文件

### 方法 A: 使用 Git 命令行

```bash
# 1. 进入打包好的目录
cd ~/.openclaw/workspace/hypertrend-analytics-github

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件
git add .

# 4. 提交
git commit -m "Initial release: HyperTrend Analytics v2.0.0"

# 5. 关联远程仓库 (替换 your-username)
git remote add origin https://github.com/your-username/hypertrend-analytics.git

# 6. 推送
git push -u origin main
```

### 方法 B: 直接拖拽上传

1. 在 GitHub 仓库页面点击 **"uploading an existing file"**
2. 拖拽 `hypertrend-analytics-github` 目录下的所有文件
3. 提交消息填写: `Initial release v2.0.0`
4. 点击 **Commit changes**

## 步骤 3: 更新 README 中的链接

上传后，编辑以下文件中的占位符：

### README.md 第 13 行
```diff
- curl -fsSL https://raw.githubusercontent.com/your-username/hypertrend-analytics/main/scripts/install.sh | bash
+ curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/hypertrend-analytics/main/scripts/install.sh | bash
```

### README.md 第 20 行
```diff
- git clone https://github.com/your-username/hypertrend-analytics.git
+ git clone https://github.com/YOUR_USERNAME/hypertrend-analytics.git
```

### package.json 第 9 行
```diff
- "url": "https://github.com/your-username/hypertrend-analytics-skill"
+ "url": "https://github.com/YOUR_USERNAME/hypertrend-analytics"
```

## 步骤 4: 创建 Release (可选但推荐)

1. 在 GitHub 仓库页面点击 **Releases** → **Create a new release**
2. 点击 **Choose a tag** → 输入 `v2.0.0` → **Create new tag**
3. **Release title**: `HyperTrend Analytics v2.0.0`
4. **Description**:
   ```markdown
   ## 🎉 HyperTrend Analytics v2.0.0

   ### ✨ 新功能
   - 完整的六芒星信用模型
   - Hyperliquid 鲸鱼监控
   - 智能地址分析
   - 数据驱动推文生成

   ### 📦 安装
   ```bash
   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/hypertrend-analytics/main/scripts/install.sh | bash
   ```

   ### 📖 文档
   详见 [README.md](README.md)
   ```
5. 点击 **Publish release**

## 步骤 5: 分享您的 Skill

### 分享到 OpenClaw 社区

在 Discord/Telegram 分享：
```
🎉 新 Skill 发布: HyperTrend Analytics v2.0.0

基于 Hyperliquid 的链上信用分析工具

功能:
✅ 六芒星信用评分
✅ 鲸鱼仓位监控
✅ 智能地址分析
✅ 数据推文生成

一键安装:
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/hypertrend-analytics/main/scripts/install.sh | bash

GitHub: https://github.com/YOUR_USERNAME/hypertrend-analytics
```

### 添加到 ClawHub (可选)

如果想让 Skill 显示在 ClawHub 上：
1. Fork https://github.com/openclaw/clawhub
2. 添加您的 skill 到 registry
3. 提交 PR

## 完整的文件清单

确保以下文件都已上传：

```
hypertrend-analytics/
├── ✅ LICENSE
├── ✅ README.md
├── ✅ SKILL.md
├── ✅ CHANGELOG.md
├── ✅ CONTRIBUTING.md
├── ✅ package.json
├── ✅ .gitignore
├── ✅ examples/
│   ├── ✅ address-analysis.md
│   └── ✅ whale-monitoring.md
├── ✅ scripts/
│   └── ✅ install.sh
└── ✅ .github/
    └── ✅ workflows/
        └── ✅ validate.yml
```

## 验证安装

上传后，测试安装命令是否工作：

```bash
# 测试一键安装
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/hypertrend-analytics/main/scripts/install.sh | bash

# 检查技能是否加载
ls ~/.openclaw/skills/hypertrend-analytics/
```

## 🎉 完成！

您的 Skill 现在已经可以在 GitHub 上被其他人发现和使用了！

---

**提示**: 记得定期更新版本号和 CHANGELOG.md！
