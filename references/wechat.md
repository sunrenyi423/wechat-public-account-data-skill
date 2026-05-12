# 微信公众号抓取说明

## 推荐方案

### 方案一：Exa 搜索 + Exa 抓取

#### 搜索公众号文章

```bash
mcporter call 'exa.web_search_exa(query: "搜索关键词", numResults: 5, includeDomains: ["mp.weixin.qq.com"])'
```

#### 抓取文章全文

```bash
mcporter call 'exa.crawling_exa(urls: ["https://mp.weixin.qq.com/s/ARTICLE_ID"], maxCharacters: 10000)'
```

这套方案适合：

- 按主题搜索公众号文章
- 抓取公开可读的文章正文
- 让 Agent 先搜索再阅读

## 备用方案

### 方案二：Camoufox

当公众号文章有额外反爬限制时，可以使用：

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

这套方案适合：

- Exa 结果不理想
- 需要更强的浏览器模拟能力
- 目标页面对简单抓取不友好

## 不推荐的方案

### 直接用 Jina Reader 抓公众号文章

```bash
curl -s "https://r.jina.ai/https://mp.weixin.qq.com/s/ARTICLE_ID"
```

这类方式对普通网页常常有效，但对公众号文章经常会被验证码或特殊限制拦截。

所以公众号文章的处理顺序建议始终是：

1. 先搜索
2. 再抓正文
3. 失败时切备用方案

## 面向 Agent 的处理建议

### 用户给主题词

先做搜索，再给出候选文章，必要时抓取其中 1-3 篇正文。

### 用户给文章链接

直接抓正文，再总结。

如果只是需要快速抓结构化数据，也可以直接运行仓库自带脚本：

```bash
python scripts/fetch_wechat_article.py "https://mp.weixin.qq.com/s/ARTICLE_ID" --format json --pretty
```

### 用户让你“找公众号号主/账号”

公众号公开搜索通常以文章为入口，不要假设能稳定拿到完整账号资料。优先返回相关文章和可确认来源。

## 示例请求

- 帮我找几篇写退休生活的公众号文章
- 帮我读一下这篇微信文章
- 搜一下最近在写“中老年生活”的公众号
- 提取这篇公众号文章的正文
