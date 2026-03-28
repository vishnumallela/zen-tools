from __future__ import annotations

import asyncio
from typing import Annotated

from pydantic import Field

from zen_tools.tools._firecrawl import client

EXAMPLES = '{ "url": "https://docs.example.com", "limit": 20 }'


async def web_crawl(
    url: Annotated[str, Field(description="Root URL to start crawling from")],
    limit: Annotated[int, Field(description="Max pages to crawl (default 5)")] = 5,
) -> str:
    """Crawl an entire site and return every page as markdown.
    Use over web_fetch when you need full site content, not just one page.
    Best for docs sites, wikis, or blogs."""
    result = await asyncio.to_thread(
        client().crawl_url,
        url,
        limit=limit,
        scrape_options={"formats": ["markdown"]},
    )
    parts: list[str] = []
    for page in result.data or []:
        meta = getattr(page, "metadata", {}) or {}
        title = meta.get("title") or meta.get("sourceURL") or url
        content = getattr(page, "markdown", "") or ""
        parts.append(f"## {title}\n\n{content}")
    return "\n\n---\n\n".join(parts)
