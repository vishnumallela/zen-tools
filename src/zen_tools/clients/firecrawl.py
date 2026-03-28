import os

from firecrawl import AsyncFirecrawlApp

_fc: AsyncFirecrawlApp | None = None


def client() -> AsyncFirecrawlApp:
    global _fc
    if _fc is None:
        _fc = AsyncFirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY", ""))
    return _fc
