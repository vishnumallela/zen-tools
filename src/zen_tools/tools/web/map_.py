from __future__ import annotations

import asyncio
from typing import Annotated

from pydantic import Field

from zen_tools.tools._firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com" }
{ "url": "https://example.com", "filter": "pricing", "limit": 50 }\
"""


async def web_map(
    url: Annotated[str, Field(description="Root URL of the site to map")],
    limit: Annotated[int, Field(description="Max URLs to return (default 5)")] = 5,
    filter: Annotated[  # noqa: A002
        str | None,
        Field(description="Topic keyword to filter returned URLs"),
    ] = None,
) -> str:
    """Discover all URLs on a site without fetching page content.
    Use before web_crawl to scope what to crawl, or when you only need a link inventory."""
    kwargs: dict = {"limit": limit}
    if filter:
        kwargs["search"] = filter
    result = await asyncio.to_thread(client().map_url, url, **kwargs)
    lines: list[str] = []
    for link in result.links or []:
        if isinstance(link, str):
            lines.append(link)
        else:
            title = getattr(link, "title", None)
            link_url = getattr(link, "url", str(link))
            lines.append(f"{link_url} — {title}" if title else link_url)
    return "\n".join(lines) if lines else "No URLs found."
