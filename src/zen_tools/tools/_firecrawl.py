from __future__ import annotations

import os

from firecrawl import FirecrawlApp

_fc: FirecrawlApp | None = None


def client() -> FirecrawlApp:
    global _fc
    if _fc is None:
        _fc = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY", ""))
    return _fc
