# Installing the Qovia MCP server (for AI agents)

Qovia is a remote MCP server over Streamable HTTP. Nothing needs to be downloaded or built.

1. Ask the user for their Qovia API key. It starts with `sk-qovia-`. If they don't have one, they create it at https://qovia.ai/console/?tab=keys after signing up and topping up. Never invent a key.
2. Add the server to the client's MCP settings.
   - Clients that support remote HTTP servers with headers:
     ```json
     {
       "mcpServers": {
         "qovia": {
           "url": "https://api.qovia.ai/mcp",
           "headers": { "Authorization": "Bearer <API key>" }
         }
       }
     }
     ```
   - Clients that only run local commands (Cline, Claude Desktop):
     ```json
     {
       "mcpServers": {
         "qovia": {
           "command": "npx",
           "args": ["-y", "mcp-remote", "https://api.qovia.ai/mcp", "--header", "Authorization:${QOVIA_AUTH}"],
           "env": { "QOVIA_AUTH": "Bearer <API key>" }
         }
       }
     }
     ```
     This needs Node.js 18 or newer.
3. Check the connection: call `get_account`. It returns the balance, plan and rate limit and is not charged. `search_endpoints` works even without a key.

Notes:
- Calls are billed per successful, non-empty result from the user's prepaid balance; every `call_endpoint` result reports `charged_usd`.
- On HTTP 429, wait for the `Retry-After` seconds before retrying.
- Docs: https://qovia.ai/docs/mcp/
