#!/usr/bin/env python3
import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from html import unescape
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    )
}


@dataclass
class ArticleData:
    url: str
    final_url: str
    title: str
    author: Optional[str]
    account_name: Optional[str]
    publish_time: Optional[str]
    digest: Optional[str]
    content_text: str
    content_markdown: str
    image_urls: List[str]


def find_first(html: str, patterns: List[str]) -> Optional[str]:
    for pattern in patterns:
        m = re.search(pattern, html, re.S)
        if m:
            return unescape(m.group(1)).strip()
    return None


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def node_to_markdown(node) -> str:
    name = getattr(node, "name", None)
    if name is None:
        return str(node).strip()
    if name in {"script", "style"}:
        return ""
    if name in {"h1", "h2", "h3", "h4"}:
        level = int(name[1])
        text = clean_text(node.get_text("\n", strip=True))
        return f'{"#" * level} {text}\n\n' if text else ""
    if name == "img":
        src = node.get("data-src") or node.get("src")
        return f"![image]({src})\n\n" if src else ""
    if name in {"p", "section", "blockquote"}:
        text = clean_text(node.get_text("\n", strip=True))
        return f"{text}\n\n" if text else ""
    if name in {"ul", "ol"}:
        lines = []
        for li in node.find_all("li", recursive=False):
            item = clean_text(li.get_text("\n", strip=True))
            if item:
                lines.append(f"- {item}")
        return "\n".join(lines) + "\n\n" if lines else ""
    parts = [node_to_markdown(child) for child in node.children]
    return "".join(parts)


def extract_article(html: str, source_url: str, final_url: str) -> ArticleData:
    soup = BeautifulSoup(html, "html.parser")
    title = (
        find_first(
            html,
            [
                r'var\s+msg_title\s*=\s*"([^"]+)"',
                r'<meta\s+property="og:title"\s+content="([^"]+)"',
                r'<title[^>]*>(.*?)</title>',
            ],
        )
        or ""
    )

    digest = find_first(
        html,
        [
            r'var\s+msg_desc\s*=\s*"([^"]*)"',
            r'<meta\s+name="description"\s+content="([^"]*)"',
        ],
    )
    author = find_first(
        html,
        [
            r'var\s+author_nickname\s*=\s*htmlDecode\("([^"]*)"\)',
            r'var\s+author_name\s*=\s*"([^"]*)"',
        ],
    )
    account_name = find_first(
        html,
        [
            r'var\s+user_name\s*=\s*"([^"]*)"',
            r'var\s+nickname\s*=\s*htmlDecode\("([^"]*)"\)',
        ],
    )
    publish_time = find_first(
        html,
        [
            r'var\s+publish_time\s*=\s*"([^"]*)"',
            r'var\s+ct\s*=\s*"([^"]*)"',
        ],
    )

    content_root = soup.select_one("#js_content") or soup.select_one(".rich_media_content")
    if content_root is None:
        raise RuntimeError("Could not locate article body. The page may require a stronger browser-based fetch.")

    text_content = clean_text(content_root.get_text("\n", strip=True))
    markdown_content = clean_text(node_to_markdown(content_root))

    image_urls: List[str] = []
    for img in content_root.find_all("img"):
        src = img.get("data-src") or img.get("src")
        if src and src not in image_urls:
            image_urls.append(src)

    return ArticleData(
        url=source_url,
        final_url=final_url,
        title=title,
        author=author,
        account_name=account_name,
        publish_time=publish_time,
        digest=digest,
        content_text=text_content,
        content_markdown=markdown_content,
        image_urls=image_urls,
    )


def fetch(url: str, timeout: int = 30) -> requests.Response:
    session = requests.Session()
    response = session.get(url, headers=DEFAULT_HEADERS, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    return response


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and extract data from a WeChat public account article.")
    parser.add_argument("url", help="mp.weixin.qq.com article URL")
    parser.add_argument("--format", choices=["json", "markdown", "text"], default="json")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    try:
        response = fetch(args.url)
        article = extract_article(response.text, args.url, response.url)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        payload = asdict(article)
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    elif args.format == "markdown":
        lines = [
            f"# {article.title}",
            "",
            f"- 原始链接: {article.url}",
            f"- 最终链接: {article.final_url}",
        ]
        if article.account_name:
            lines.append(f"- 公众号: {article.account_name}")
        if article.author:
            lines.append(f"- 作者: {article.author}")
        if article.publish_time:
            lines.append(f"- 发布时间: {article.publish_time}")
        if article.digest:
            lines += ["", "## 摘要", "", article.digest]
        lines += ["", "## 正文", "", article.content_markdown]
        if article.image_urls:
            lines += ["", "## 图片", ""]
            lines.extend(f"- {url}" for url in article.image_urls)
        print("\n".join(lines))
    else:
        print(article.content_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
