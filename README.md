# WeChat Public Account Data Skill

一个面向 AI Agent 的技能包，用来搜索、抓取和阅读微信公众号文章。

适用场景：

- 搜索某个主题下的微信公众号文章
- 读取公众号文章正文
- 在常规网页抓取失败时，切换到更稳的方式
- 给具备命令执行能力的 Agent 提供稳定的工作流

## 能力范围

当前技能覆盖三类能力：

1. 搜索公众号文章
2. 抓取公众号文章全文
3. 在需要时切换到更强的阅读方案

## 目录结构

```text
wechat-public-account-data-skill/
├── README.md
├── SKILL.md
├── LICENSE
├── NOTICE
├── requirements.txt
├── scripts/
│   └── fetch_wechat_article.py
└── references/
    └── wechat.md
```

## 工作流

### 1. 搜索文章

优先用 Exa 搜索公众号文章：

```bash
mcporter call 'exa.web_search_exa(query: "养老金 延迟退休", numResults: 5, includeDomains: ["mp.weixin.qq.com"])'
```

### 2. 抓取全文

拿到文章链接后，再抓取正文：

```bash
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

### 3. 备用方案

如果 Exa 不够，或者目标文章需要更强的网页兼容能力，可以切到 Camoufox 方案：

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

## 可直接运行的抓取脚本

仓库内置了一个最小可用脚本：

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format json --pretty
```

也支持导出 Markdown：

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format markdown
```

### 输出字段

- `title`
- `author`
- `account_name`
- `publish_time`
- `digest`
- `content_text`
- `content_markdown`
- `image_urls`

### 安装依赖

```bash
pip install -r requirements.txt
```

### 脚本边界

- 适合公开可读的公众号文章
- 对强验证码或更复杂反爬页面，不保证稳定
- 如果抓不到正文，建议切到 `references/wechat.md` 里的浏览器方案

## 适用的 Agent 请求

- 帮我找几篇关于退休生活的公众号文章
- 看一下这篇微信文章讲了什么
- 把这篇公众号文章提取成 Markdown
- 搜一下最近在写“中老年生活”的公众号

## 安装方式

把这个目录放到你的 Agent skills 目录中即可使用。

如果你的 Agent 支持按 `SKILL.md` 自动触发，这个技能在用户提到这些词时会触发：

- 公众号
- 微信文章
- mp.weixin.qq.com
- 微信公众号
- 读一下这篇微信文章

## 作为可安装技能使用

如果你在 Agent 系统里使用技能目录约定，只需要把本目录放进 skills 路径即可。

触发词已经写在 `SKILL.md` 中，Agent 提到这些词时可自动匹配：

- 公众号
- 微信文章
- 微信公众号
- mp.weixin.qq.com

## 来源说明

本仓库中的公众号抓取工作流，整理和改写自公开项目 [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) 中与微信公众号相关的能力说明。

原项目采用 MIT License。  
本仓库保留原始来源说明，并只提取与“公众号数据抓取”直接相关的技能文档。
