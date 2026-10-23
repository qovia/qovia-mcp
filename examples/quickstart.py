"""Search Xiaohongshu (RedNote) notes with the Qovia API. Standard library only.

    QOVIA_API_KEY=sk-qovia-... python quickstart.py coffee
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.qovia.ai"


def call(path, **params):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {os.environ['QOVIA_API_KEY']}"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        error = json.load(e).get("error", {})
        sys.exit(f"{e.code} {error.get('code')}: {error.get('message')}")


keyword = sys.argv[1] if len(sys.argv) > 1 else "coffee"
body = call("/v1/raw/xiaohongshu/search", keyword=keyword, sort="latest")
for item in body["data"]["items"]:
    print(item["extra"]["url"], "|", item["text"][:60].replace("\n", " "))
print(f"charged ${body['meta']['charged_usd']}")
