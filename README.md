# Qovia — public web data API and MCP server

Qovia gives AI agents and developers one API key for public data from Chinese and global platforms: Douyin, Xiaohongshu (RedNote), Weibo, Bilibili, Kuaishou, Zhihu, Tieba, WeChat Official Accounts, Toutiao, Taobao/Tmall and JD.com reviews, Fliggy hotel reviews, the Douyin Xingtu, Xiaohongshu Pugongying, Kuaishou Cili Juxing and Bilibili Huahuo creator marketplaces, TikTok, YouTube, Instagram, X and Reddit.

- **100+ endpoints** for posts, comments, creator profiles, hot lists and search, in one JSON envelope.
- **Remote MCP server** at `https://api.qovia.ai/mcp`, so there is nothing to install.
- **50 trial calls** for every new account, then **pay per successful call** from a prepaid balance. Empty results and errors are never charged. See [pricing](https://qovia.ai/pricing/).

This repository holds setup instructions, examples and a Python client. The service itself is hosted, and its source is not public. Qovia is an unofficial data service, not affiliated with the platforms listed.

## Platforms

| Platform | Chinese name | What you can get |
|---|---|---|
| Douyin | 抖音 | Videos, comments and replies, creators, search, live search, product reviews, hot search |
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

Sign up at [qovia.ai](https://qovia.ai) and create a key at [qovia.ai/console/?tab=keys](https://qovia.ai/console/?tab=keys). Keys look like `sk-qovia-…`. A new account comes with 50 trial calls; top up when they run out.

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

**Gemini CLI**

```bash
gemini extensions install https://github.com/qovia/qovia-mcp
```

Gemini CLI asks for your Qovia API key when it installs the extension. To change it later: `gemini extensions config qovia QOVIA_API_KEY`.

**Claude Code (plugin)**

```
/plugin install qovia --marketplace qovia/qovia-mcp
```

Set your API key when prompted, or later with `/plugin configure qovia@qovia`. Without a key, only the catalog tools work.

### Tools

| Tool | What it does | Key needed |
|---|---|---|
| `search_endpoints` | Find endpoints by keyword (English or Chinese) or platform | No |
| `get_endpoint` | Parameters, price and a response example for one endpoint | No |
| `call_endpoint` | Run an endpoint; returns the data and what the call cost | Yes |
| `get_account` | Balance, plan and rate limit | Yes |

Add `?tools=all` to the URL (`https://api.qovia.ai/mcp?tools=all`) to get one typed tool per live endpoint in addition to these four, or `?tools=douyin,kuaishou` for only some platforms.

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

Every success is HTTP 200 with `{"request_id", "data", "meta"}`. `meta.charged_usd` says what the call cost, and `meta.empty` is true when nothing was found (not charged). Errors are `{"error": {"code", "message", "request_id", "support"}}`.

Examples: [Python](examples/quickstart.py) · [Node.js](examples/quickstart.mjs) · [curl](examples/quickstart.sh)

Python client: `pip install qovia` ([PyPI](https://pypi.org/project/qovia/), source in [python/](python/)).

## How the hosted server works

- **Nothing runs on your machine.** The MCP server is hosted at `https://api.qovia.ai/mcp` (Streamable HTTP, stateless: every request stands alone and is answered with JSON). Cursor, VS Code, Claude Code and Gemini CLI connect to it directly. Only the `mcp-remote` configuration above starts a local process: the open-source `mcp-remote` npm package, which forwards to the same URL.
- **Four tools by default**, listed in the table above. The server advertises tools only, no resources or prompts.
- **What a call sends:** the tool name, its parameters (keywords, IDs, filters) and your API key in the `Authorization` header. The parameters in the [OpenAPI spec](https://qovia.ai/openapi.json) are IDs, keywords, paging and filters; none is a platform login, cookie or password.
- **What comes back:** public data (posts, comments, profiles, hot lists, reviews) as JSON, plus `meta` with what the call cost.
- **Same checks as the HTTP API:** authentication, key scopes, parameter validation, rate limits, billing and the usage log. Create a separate key for your AI tools, limit it to the endpoints it needs, and revoke it in the console at any time.

You can check the tool list yourself, without a key:

```bash
curl -s https://api.qovia.ai/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

[docs/mcp-tools.json](docs/mcp-tools.json) is a copy of what the server returned for `initialize` and `tools/list` on 2026-10-28; the live answer is authoritative. Security reports: [SECURITY.md](SECURITY.md). Privacy summary: [qovia.ai/privacy](https://qovia.ai/privacy/).

## Docs

- [Quickstart](https://qovia.ai/docs/) · [API reference](https://qovia.ai/docs/api-reference/) · [MCP guide](https://qovia.ai/docs/mcp/) · [中文文档](https://qovia.ai/zh/docs/)
- [OpenAPI 3.1 spec](https://qovia.ai/openapi.json) · [llms.txt](https://qovia.ai/llms.txt) · [Coverage](https://qovia.ai/coverage/)

## Support

Email scott@qovia.ai or message [@scott10081](https://t.me/scott10081) on Telegram. News: [@QoviaAI](https://x.com/QoviaAI).

The examples and the Python client in this repository are MIT-licensed.
