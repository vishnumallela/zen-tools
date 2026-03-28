from typing import Annotated

from firecrawl.v2.types import CrawlJob, ScrapeOptions

from zen_tools.clients.firecrawl import client

EXAMPLES = '{ "url": "https://docs.example.com", "limit": 20 }'


async def web_crawl(
    url: Annotated[str, "Root URL to start crawling from"],
    limit: Annotated[int, "Max pages to crawl (default 5)"] = 5,
) -> str:
    """Crawl an entire site and return every page as markdown.
    Use over web_fetch when you need full site content, not just one page.
    Best for docs sites, wikis, or blogs."""
    result: CrawlJob = await client().crawl(
        url,
        limit=limit,
        scrape_options=ScrapeOptions(formats=["markdown"]),
    )
    parts: list[str] = []
    for page in result.data:
        meta = page.metadata
        title = ((meta.title or meta.source_url) if meta else "") or url
        parts.append(f"## {title}\n\n{page.markdown or ''}")
    return "\n\n---\n\n".join(parts)
