# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AutoRequest** — 定时向大模型发送签到请求的脚本，部署在 GitHub Actions 上自动运行。使用 OpenAI 兼容 API 格式，支持任意兼容的 LLM 提供商。

## Build & Development Commands

```bash
source .venv/bin/activate
pip install -e .

# 本地运行（需要设置环境变量）
export API_KEY=your-key
python -m autorequest.main
```

## Architecture

- `autorequest/main.py` — 核心逻辑，向 LLM API 发送一条简单的 chat completion 请求，打印响应
- `.github/workflows/schedule.yml` — GitHub Actions 定时触发，每天 CST 4:00/9:00/14:00/19:00 各执行一次（对应 UTC 20:00/1:00/6:00/11:00），同时支持手动触发 (`workflow_dispatch`)
- 环境变量通过 GitHub Secrets 注入：`API_KEY`（必需）、`API_BASE_URL`（可选，默认 OpenAI）、`MODEL`（可选，默认 gpt-4o-mini）

## Schedule Design

采用固定时间点而非倒计时，因为：无状态、失败不影响后续触发、与 GitHub Actions cron 天然匹配。
