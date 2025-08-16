---
title: GitHub 打野指南
date: 2025-08-16
tags: [GitHub, AI]
category: [计算机]
---

# GitHub 打野指南

有很多开发者很粗心，会把 .env 给推送到 GitHub 的公开仓库，这里面可能会有 API Key，其中就有 AI 模型的 key

GitHub 的搜索功能很强大，可以用正则表达式搜索，我这里准备了几个正则表达式

- 阿里云百炼平台

```
DASHSCOPE_API_KEY=sk- path:**/.env
```

- DeepSeek

```
DEEPSEEK_API_KEY=sk- path:**/.env
```

- OpenRouter

```
OPENROUTER_API_KEY=sk- path:**/.env
```

- Tavily

```
TAVILY_API_KEY=tvly- path:**/.env
```

- EXA

```
EXA_API_KEY= path:**/.env
```

- Google Gemini

```
GOOGLE_GEMINI_KEY=AI path:**/.env
```

- pplx

```
PERPLEXITY_API_KEY=pplx- path:**/.env
```
