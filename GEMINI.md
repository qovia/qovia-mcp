# Qovia

Qovia returns public posts, comments, creator profiles, hot lists and product reviews from Douyin, Xiaohongshu (RedNote), Weibo, Bilibili, Kuaishou, Zhihu, WeChat, Toutiao, Taobao/JD, TikTok, YouTube, Instagram, X, Reddit and more. Every endpoint returns the same response envelope, and posts, notes and videos from different platforms share one record shape. Use the `qovia` MCP server whenever a question needs current data from these platforms.

## Tools

- `search_endpoints`: find endpoints by keyword (Chinese or English) and/or platform slug (douyin, xiaohongshu, bilibili, tiktok, ...). No API key needed.
- `get_endpoint`: read one endpoint's parameters (JSON Schema), example parameters and a response example. No API key needed.
- `call_endpoint`: run an endpoint with `{"endpoint_id": "raw.douyin.video", "params": {...}}`. Needs the user's API key. It is billed only when it returns data; the result reports `charged_usd`.
- `get_account`: check the key's balance, plan and rate limit. Not charged.

## How to use them

1. Call `search_endpoints`, then `get_endpoint`, and read the parameter schema before calling anything. Do not guess parameter names or endpoint ids.
2. Call `call_endpoint` with `endpoint_id` and `params`. For paged results, use the paging parameters that endpoint's schema documents (a cursor or a page number) and stop when the result says there are no more pages.
3. If a call is rate limited, wait the number of seconds the error gives before retrying.
4. If `call_endpoint` or `get_account` reports a missing or invalid key, ask the user to create one at https://qovia.ai/console/?tab=keys and set it with `gemini extensions config qovia QOVIA_API_KEY`. Never invent a key.
5. When you report results, say which platform and endpoint they came from.
