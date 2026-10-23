# Qovia — public web data API and MCP server

Qovia gives AI agents and developers one API key for public data from Chinese and global platforms: Douyin, Xiaohongshu (RedNote), Weibo, Bilibili, Kuaishou, Zhihu, Tieba, WeChat Official Accounts, Toutiao, Taobao/Tmall and JD.com reviews, the Douyin Xingtu and Xiaohongshu Pugongying creator marketplaces, TikTok, YouTube, Instagram, X and Reddit.

- **140+ endpoints** for posts, comments, creator profiles, hot lists and search, in one JSON envelope.
- **Remote MCP server** at `https://api.qovia.ai/mcp`, so there is nothing to install.
- **Pay per successful call** from a prepaid balance. Empty results and errors are never charged. See [pricing](https://qovia.ai/pricing/).

This repository holds setup instructions and examples. The service itself is hosted, and its source is not public.

## Platforms

| Platform | Chinese name | What you can get |
|---|---|---|
| Douyin | 抖音 | Videos, comments and replies, creators, search, live rooms, product reviews, hot search |
| Xiaohongshu (RedNote) | 小红书 | Notes, search, comments and replies, user profiles and notes |
| Weibo | 微博 | Posts, comments and replies, user profiles and posts, search, hot search |
| Kuaishou | 快手 | Videos, comments and replies, creators' hot videos, hot board |
| Bilibili | 哔哩哔哩 | Videos, search, comments and replies, danmaku, creators, popular videos |
| Zhihu | 知乎 | Questions, answers, comments, users, hot list, search |
| Tieba | 百度贴吧 | Threads, floor replies, users |
| WeChat | 微信公众号、视频号 | Official account search and articles, article metrics, Channels search |
| Toutiao | 今日头条 | Articles, videos, comments |
| Taobao / Tmall | 淘宝、天猫 | Product reviews |
| JD.com | 京东 | Product reviews |
| Fliggy | 飞猪 | Hotel ratings and reviews |
| Douyin Xingtu | 抖音星图 | Creator rate cards, audience, performance |
| Xiaohongshu Pugongying | 小红书蒲公英 | Creator data, fans, notes |
| Kuaishou Cili Juxing | 快手磁力聚星 | Creator data |
| Bilibili Huahuo | B 站花火 | Creator data |
| TikTok | — | Videos, comments, creators, search, hashtags |
| YouTube | — | Videos, comments, channels, search |
| Instagram | — | Posts, comments, profiles, hashtags |
| X (Twitter) | — | Posts, replies, users, search, trending |
| Reddit | — | Posts, comments, subreddits, users, search |

Plus **cross-platform search** (跨域检索): one query across Weibo, Douyin, Toutiao, Xiaohongshu, WeChat articles, news sites, forums and Bilibili, filtered by date, platform and sentiment. The full, current endpoint list is at [qovia.ai/coverage](https://qovia.ai/coverage/).

## 1. Get an API key

Sign up at [qovia.ai](https://qovia.ai), top up your balance, and create a key at [qovia.ai/console/?tab=keys](https://qovia.ai/console/?tab=keys). Keys look like `sk-qovia-…`.

## 2. Connect your MCP client

**Claude Code**

```bash
claude mcp add --transport http qovia https://api.qovia.ai/mcp --header "Authorization: Bearer $QOVIA_API_KEY"
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "qovia": {
      "url": "https://api.qovia.ai/mcp",
      "headers": { "Authorization": "Bearer sk-qovia-..." }
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`)

```json
{
  "servers": {
    "qovia": {
      "type": "http",
      "url": "https://api.qovia.ai/mcp",
      "headers": { "Authorization": "Bearer ${input:qovia-key}" }
    }
  },
  "inputs": [
    { "type": "promptString", "id": "qovia-key", "description": "Qovia API key", "password": true }
  ]
}
```

**Cline, Claude Desktop and other clients that run local commands** (via `mcp-remote`)

```json
{
  "mcpServers": {
    "qovia": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.qovia.ai/mcp", "--header", "Authorization:${QOVIA_AUTH}"],
      "env": { "QOVIA_AUTH": "Bearer sk-qovia-..." }
    }
  }
}
```

### Tools

| Tool | What it does | Key needed |
|---|---|---|
| `search_endpoints` | Find endpoints by keyword (English or Chinese) or platform | No |
| `get_endpoint` | Parameters, price and a response example for one endpoint | No |
| `call_endpoint` | Run an endpoint; returns the data and what the call cost | Yes |
| `get_account` | Balance, plan and rate limit | Yes |

Connect to `https://api.qovia.ai/mcp?tools=all` to get one typed tool per endpoint instead.

### Things to ask

- "Search Xiaohongshu for notes about [product] from the last week and summarise what people like and complain about."
- "What is on the Weibo and Douyin hot lists right now? Group the topics by theme."
- "Pull the JD.com reviews for [product link] and list the most common complaints."
- "Search Chinese social media and news for [brand] in the last 7 days and break the mentions down by platform and sentiment."

## 3. Or call the HTTP API

```bash
curl -s "https://api.qovia.ai/v1/raw/xiaohongshu/search?keyword=coffee" \
  -H "Authorization: Bearer $QOVIA_API_KEY"
```

Every success is HTTP 200 with `{"request_id", "data", "meta"}`. `meta.charged_usd` says what the call cost, and `meta.empty` is true when nothing was found (not charged). Errors are `{"error": {"code", "message", "request_id"}}`.

Examples: [Python](examples/quickstart.py) · [Node.js](examples/quickstart.mjs) · [curl](examples/quickstart.sh)

## Docs

- [Quickstart](https://qovia.ai/docs/) · [API reference](https://qovia.ai/docs/api-reference/) · [MCP guide](https://qovia.ai/docs/mcp/) · [中文文档](https://qovia.ai/zh/docs/)
- [OpenAPI 3.1 spec](https://qovia.ai/openapi.json) · [llms.txt](https://qovia.ai/llms.txt) · [Coverage](https://qovia.ai/coverage/)

## Support

Email scott@qovia.ai or message [@wodaemn](https://t.me/wodaemn) on Telegram. News: [@QoviaAI](https://x.com/QoviaAI).

The examples in this repository are MIT-licensed.
