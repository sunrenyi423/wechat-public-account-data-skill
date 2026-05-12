---
name: wechat-public-account-data
description: >
  Search, fetch, and read WeChat public account articles for AI agents.
  Use when the user asks to find公众号文章, read微信文章, extract微信公众号正文,
  or handle mp.weixin.qq.com links.
triggers:
  - 公众号
  - 微信文章
  - 微信公众号
  - mp.weixin.qq.com
  - 读一下这篇微信文章
  - 搜一下公众号文章
metadata:
  source:
    adapted_from: https://github.com/Panniantong/Agent-Reach
---

# WeChat Public Account Data Skill

用于搜索、抓取、阅读微信公众号文章。

## 什么时候用

当用户：

- 提到“公众号”“微信文章”“微信公众号”
- 给出 `mp.weixin.qq.com` 链接
- 想搜索某个主题下的公众号文章
- 想把公众号文章正文提取出来

## 核心工作流

### 1. 搜索公众号文章

优先用 Exa：

```bash
mcporter call 'exa.web_search_exa(query: "关键词", numResults: 5, includeDomains: ["mp.weixin.qq.com"])'
```

### 2. 抓取公众号正文

```bash
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

### 3. 如果常规抓取不稳

切换到更强的浏览器方案：

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

## 注意事项

- 不要优先用 Jina Reader 直接抓公众号文章，容易被验证码拦截。
- 搜索和抓取分两步做：先搜链接，再读正文。
- 如果用户只给了主题词，不要直接猜文章，先搜索。
- 如果用户给了具体链接，优先抓正文，再做总结。

## 详细说明

见 [references/wechat.md](references/wechat.md)
