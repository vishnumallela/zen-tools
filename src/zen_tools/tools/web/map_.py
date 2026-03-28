from typing import Annotated

from zen_tools.clients.firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com" }
{ "url": "https://example.com", "filter": "pricing", "limit": 50 }\
"""


async def web_map(
    url: Annotated[str, "Root URL of the site to map."],
    limit: Annotated[int, "Max number of URLs to return. Default is 5."] = 5,
    filter: Annotated[str | None, "Keyword to filter URLs by topic. Omit to return all."] = None,  # noqa: A002
) -> str:
    """Discover all URLs on a site without fetching any page content.
    Returns: plain list of URLs with titles, one per line. No page content is fetched.
    Use when you need to find which pages exist on a site before deciding what to fetch.
    Not for getting page content directly. Use web_fetch or web_search instead."""
    result = await client().map(url, search=filter, limit=limit)
    lines = [
        f"{link.url} | {link.title}" if link.title else link.url for link in (result.links or [])
    ]
    return "\n".join(lines) if lines else "No URLs found."
