from typing import Annotated

from firecrawl.v2.types import MapData

from zen_tools.clients.firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com" }
{ "url": "https://example.com", "filter": "pricing", "limit": 50 }\
"""


async def web_map(
    url: Annotated[str, "Root URL of the site to map"],
    limit: Annotated[int, "Max URLs to return (default 5)"] = 5,
    filter: Annotated[str | None, "Topic keyword to filter returned URLs"] = None,  # noqa: A002
) -> str:
    """Discover all URLs on a site without fetching page content.
    Use before web_crawl to scope what to crawl, or when you only need a link inventory."""
    result: MapData = await client().map(url, search=filter, limit=limit)
    lines = [
        f"{link.url} — {link.title}" if link.title else link.url for link in (result.links or [])
    ]
    return "\n".join(lines) if lines else "No URLs found."
