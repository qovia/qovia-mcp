"""Python client for the Qovia public web data API (https://qovia.ai).

    from qovia import Qovia

    client = Qovia()  # reads QOVIA_API_KEY
    notes = client.get("/v1/raw/xiaohongshu/search", keyword="coffee")
    for note in notes.data["items"]:
        print(note["extra"]["url"], note["text"][:60])
    print(notes.charged_usd)
"""

from qovia.client import Qovia, QoviaError, Response

__all__ = ["Qovia", "QoviaError", "Response"]
__version__ = "0.1.1"
