# AutoRequest

定时向大模型发送签到请求的脚本，部署在 GitHub Actions 上自动运行。

## 工作原理

每天 CST 4:00 / 9:00 / 14:00 / 19:00 自动向配置的大模型发送请求，同时支持手动触发。

- 支持多模型，通过 `PROVIDERS` 环境变量配置
- 每个模型可独立开关（`enabled` 字段）
- 采用固定时间点触发，无需维护状态，单次失败不影响后续执行

## 本地运行

```bash
pip install -e .
export PROVIDERS='[{"enabled":true,"name":"智谱GLM","api_key":"your-key","base_url":"https://open.bigmodel.cn/api/anthropic","model":"glm-5"}]'
python -m autorequest.main
```

## 部署到 GitHub Actions

1. 将代码推送到 GitHub 仓库
2. 进入 **Settings → Secrets and variables → Actions**，添加 Secret `PROVIDERS`，值为 JSON 数组：
   ```json
   [
     {"enabled": true, "name": "智谱GLM", "api_key": "your-key", "base_url": "https://open.bigmodel.cn/api/anthropic", "model": "glm-5"},
     {"enabled": false, "name": "DeepSeek", "api_key": "your-key", "base_url": "https://api.deepseek.com", "model": "deepseek-chat"}
   ]
   ```
3. 进入 **Actions → Scheduled Request → Run workflow** 手动触发，或等待定时执行

要增删模型或开关，编辑 `PROVIDERS` 这个 Secret 的值即可。
