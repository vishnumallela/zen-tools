from typing import Annotated

from firecrawl.v2.types import Document, ScrapeOptions, SearchData

from zen_tools.clients.firecrawl import client

EXAMPLES = '{ "query": "zod v4 migration guide", "limit": 5 }'


async def web_search(
    query: Annotated[str, "Search keywords or phrase"],
    limit: Annotated[int, "Max results (default 5)"] = 5,
) -> str:
    """Keyword search across the web. Returns ranked results with titles, URLs, and page content.
    Use when you need to discover relevant pages, not when you already have a URL."""
    result: SearchData = await client().search(
        query,
        limit=limit,
        scrape_options=ScrapeOptions(formats=["markdown"]),
    )
    parts: list[str] = []
    for i, r in enumerate(result.web or [], 1):
        if isinstance(r, Document):
            meta = r.metadata
            title = (meta.title if meta else "") or ""
            url = ((meta.url or meta.source_url) if meta else "") or ""
            content = r.markdown or ""
        else:
            title = r.title or ""
            url = r.url
            content = r.description or ""
        parts.append(f"{i}. **{title}**\n{url}\n{content}")
    return "\n\n".join(parts)
