# qovia

Python client for [Qovia](https://qovia.ai): public data from Douyin, Xiaohongshu (RedNote), Weibo, Bilibili, Kuaishou, Zhihu, WeChat Official Accounts, Taobao/JD reviews, the Xingtu and Pugongying creator marketplaces, TikTok, YouTube, Instagram, X and Reddit, as structured JSON. No dependencies.

```bash
pip install qovia
```

```python
from qovia import Qovia, QoviaError

client = Qovia()  # reads QOVIA_API_KEY; create a key at https://qovia.ai/console/?tab=keys

notes = client.get("/v1/raw/xiaohongshu/search", keyword="coffee", sort="latest")
for note in notes.data["items"]:
    print(note["extra"]["url"], note["text"][:60])
print("charged", notes.charged_usd)

hot = client.get("/v1/raw/weibo/hot_search")
results = client.search("electric vehicles", platforms=["weibo", "douyin"])

try:
    client.get("/v1/raw/douyin/video", item_id="not-a-real-id")
except QoviaError as error:
    print(error.code, error.request_id)
```

- `get(path, **params)` and `post(path, body)` call any endpoint; the [API reference](https://qovia.ai/docs/api-reference/) lists them all.
- A `Response` has `data`, `meta`, `charged_usd`, `balance_usd` and `empty`. Empty results and errors are never charged.
- `pages(path, ...)` walks page-numbered endpoints until `has_more` is false.
- 429 and 503 answers are retried (honouring `Retry-After`); other errors raise `QoviaError` with `code`, `message` and `request_id`.

New accounts get 50 trial calls. Questions: [Telegram @scott10081](https://t.me/scott10081) or scott@qovia.ai.
