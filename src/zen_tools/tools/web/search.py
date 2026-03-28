from __future__ import annotations

import asyncio
from typing import Annotated

from pydantic import Field

from zen_tools.tools._firecrawl import client

EXAMPLES = '{ "query": "zod v4 migration guide", "limit": 5 }'


async def web_search(
    query: Annotated[str, Field(description="Search keywords or phrase")],
    limit: Annotated[int, Field(description="Max results (default 5)")] = 5,
) -> str:
    """Keyword search across the web. Returns ranked results with titles, URLs, and page content.
    Use when you need to discover relevant pages, not when you already have a URL."""
    result = await asyncio.to_thread(
        client().search,
        query,
        limit=limit,
        scrape_options={"formats": ["markdown"]},
    )
    parts: list[str] = []
    for i, r in enumerate(result.data or [], 1):
        title = getattr(r, "title", "") or ""
        url = getattr(r, "url", "") or ""
        content = getattr(r, "markdown", "") or getattr(r, "description", "") or ""
        parts.append(f"{i}. **{title}**\n{url}\n{content}")
    return "\n\n".join(parts)
