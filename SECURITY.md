# Security

## Reporting a vulnerability

Email scott@qovia.ai or message [@scott10081](https://t.me/scott10081) on Telegram. Please say what you found and how to reproduce it, and keep the details out of public issues.

This covers the Qovia service (`qovia.ai`, `api.qovia.ai`) and the code in this repository.

## What this repository contains

Setup instructions, example scripts and a small Python client. The Qovia service itself is hosted, and its source is not in this repository.

- No install scripts, no `package.json`, no compiled binaries. Nothing here runs when you clone or open the repository.
- `examples/` has three short scripts (Python, Node.js, curl). `python/` is a client that uses only the Python standard library.
- The examples and the client send your API key only to the API base URL, in the `Authorization` header. The client's default base URL is `https://api.qovia.ai`.
- `llms-install.md` is an install guide for AI coding agents (the optional file Cline's MCP Marketplace reads when it installs a server). It asks the agent to get the user's own Qovia API key from the user, to add the MCP configuration shown in the README and to check the connection with `get_account`, plus notes on the trial and rate limits.
- `mcp.json`, `.cursor-plugin/plugin.json`, `.claude-plugin/` (Claude Code plugin), `gemini-extension.json` and `GEMINI.md` (Gemini CLI extension) describe the same remote MCP server for clients and plugin directories. They hold placeholders, never a key: Claude Code and Gemini CLI ask for your own key.
- `docs/mcp-tools.json` is a copy of what the hosted server returned for `initialize` and `tools/list` on 2026-10-28. The live answer is authoritative.

## How the hosted MCP server works

- It is a remote Streamable HTTP endpoint, `https://api.qovia.ai/mcp`. It is stateless: every request stands alone and is answered with JSON.
- It advertises tools only (no resources or prompts), four by default: `search_endpoints`, `get_endpoint`, `call_endpoint` and `get_account`. `?tools=all` adds one tool per live endpoint.
- `search_endpoints` and `get_endpoint` read the endpoint catalog and need no key. `call_endpoint` and `get_account` need an API key.
- A call sends the tool name, its parameters (keywords, IDs, filters) and the API key in the `Authorization` header. The parameters listed in the [OpenAPI spec](https://qovia.ai/openapi.json) are IDs, keywords, paging and filters; none is a platform login, cookie or password.
- A call returns public data (posts, comments, profiles, hot lists, reviews) as JSON, plus `meta` with what the call cost.
- Every MCP call goes through the same pipeline as the HTTP API: authentication, key scopes, parameter validation, rate limits, billing and the usage log.
- Only a call that returns data is charged. Empty results and failures are not.

You can verify the tool list without a key:

```bash
curl -s https://api.qovia.ai/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Data

Account information (email, company) is used only to deliver the service and to bill. Qovia does not sell personal information and does not resell your requests or the results it returns to you. Details: [qovia.ai/privacy](https://qovia.ai/privacy/).

Qovia is an unofficial data service, not affiliated with the platforms it returns data from.

## API keys

- The full key is shown once when you create it; the server keeps only a hash.
- Use a separate key for AI tools and limit it to the endpoints it needs (scopes). Revoke it in the console at any time.
- Never commit a key. `sk-qovia-...` in this repository is a placeholder.
