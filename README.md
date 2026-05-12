# WeChat Public Account Data Skill

一个面向 AI Agent 的微信公众号文章搜索与抓取技能包。

它解决两类问题：

1. 让 Agent 知道什么时候该用“公众号文章工作流”
2. 提供一个最小可用的抓取脚本，直接提取公众号文章正文、摘要、图片和基础元数据

适合这些场景：

- 搜索某个主题下的微信公众号文章
- 阅读、总结、归档公众号文章
- 把公众号文章提取成 JSON / Markdown / 纯文本
- 为具备命令执行能力的 Agent 提供稳定的技能入口

## 特性

- `SKILL.md` 可直接作为 Agent Skill 使用
- 支持公众号文章工作流说明
- 内置可运行脚本 `scripts/fetch_wechat_article.py`
- 支持输出 `json`、`markdown`、`text`
- 提取字段包括标题、作者、公众号名、发布时间、摘要、正文、图片列表

## 目录结构

```text
wechat-public-account-data-skill/
├── README.md
├── SKILL.md
├── LICENSE
├── NOTICE
├── .gitignore
├── requirements.txt
├── scripts/
│   └── fetch_wechat_article.py
└── references/
    └── wechat.md
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 抓取公众号文章

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format json --pretty
```

### 3. 输出 Markdown

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format markdown
```

### 4. 只要纯文本

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format text
```

## 输出字段

脚本会返回这些字段：

- `url`
- `final_url`
- `title`
- `author`
- `account_name`
- `publish_time`
- `digest`
- `content_text`
- `content_markdown`
- `image_urls`

## 作为 Agent Skill 使用

把本目录放进你的 skills 目录即可。

触发词已经写在 `SKILL.md` 中，适合自动匹配这些请求：

- 公众号
- 微信文章
- 微信公众号
- mp.weixin.qq.com
- 读一下这篇微信文章
- 搜一下公众号文章

## 推荐工作流

### 场景一：用户给主题词

先搜索，再抓正文：

```bash
mcporter call 'exa.web_search_exa(query: "养老金 延迟退休", numResults: 5, includeDomains: ["mp.weixin.qq.com"])'
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

### 场景二：用户直接给文章链接

直接抓正文并总结：

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format markdown
```

### 场景三：常规抓取不稳

切换到更强的浏览器方案：

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

## 脚本边界

- 适合公开可读的公众号文章
- 对强验证码或更复杂反爬页面，不保证稳定
- 如果抓不到正文，建议切到 `references/wechat.md` 里的浏览器方案

## 演示示例

### 示例 1：抓成 JSON

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/TSNQKkRpN1qbKsT7BvzqIw" --format json --pretty
```

示例输出结构：

```json
{
  "title": "“老黄骗人”！5070首批评测：说好1/3价格赛4090，实际不如4070Ti",
  "account_name": "gh_114e76fd6e5d",
  "publish_time": "1741148529",
  "digest": "博主：史上最差70系列",
  "content_text": "...",
  "image_urls": ["https://mmbiz.qpic.cn/..."]
}
```

### 示例 2：抓成 Markdown，给 LLM 做总结

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format markdown > article.md
```

### 示例 3：在 Agent 里处理

用户说：

> 帮我读一下这篇微信文章，并给我总结重点

Agent 可以这样做：

1. 检测链接是不是 `mp.weixin.qq.com`
2. 用本仓库脚本或 `references/wechat.md` 里的方案抓正文
3. 提取标题、摘要、正文和图片
4. 再做摘要、翻译或结构化整理

## 仓库发布文案

你可以直接拿下面这段作为仓库首页介绍、朋友圈文案、社群发布文案或产品说明：

> 这是一个给 AI Agent 用的“微信公众号文章抓取技能”。  
> 它包含两部分：一份可安装的 `SKILL.md`，以及一个可直接运行的公众号文章抓取脚本。  
> 适合做公众号文章搜索、正文提取、总结归档、内容分析。  
> 默认支持 JSON / Markdown / Text 输出，便于后续接入总结、RAG、知识库或自动化工作流。  
> 如果你在做 Agent、内容工具、信息抓取、知识归档，这个仓库可以直接拿去用。

## 推荐的 GitHub 仓库描述

可以直接用这句：

> Search and extract WeChat public account articles for AI agents, with a runnable fetch script and installable skill docs.

## 推荐的 GitHub Topics

建议添加这些 topics：

- `wechat`
- `wechat-official-account`
- `weixin`
- `web-scraping`
- `ai-agent`
- `agent-skill`
- `content-extraction`
- `markdown`

## 来源说明

本仓库中的公众号抓取工作流，整理和改写自公开项目 [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) 中与微信公众号相关的能力说明。

原项目采用 MIT License。  
本仓库保留原始来源说明，并只提取与“公众号数据抓取”直接相关的技能文档与最小可用脚本。
