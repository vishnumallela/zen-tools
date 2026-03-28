from typing import Annotated

from zen_tools.clients.firecrawl import client

EXAMPLES = '{ "query": "zod v4 migration guide", "limit": 5 }'


async def web_search(
    query: Annotated[str, "Search keywords or phrase."],
    limit: Annotated[int, "Max number of results to return. Default is 5."] = 5,
) -> str:
    """Search the web by keyword and return a ranked list of matching pages.
    Returns: numbered list where each result has the page title, URL, and a short content preview. Not full page content.
    Use when you have keywords but no URL yet and need to discover relevant pages.
    Not for fetching a known URL. Use web_fetch instead.
    Not for research that requires reasoning across sources. Use agent_research instead."""
    result = await client().search(query, limit=limit)
    parts: list[str] = []
    for i, r in enumerate(result.web or [], 1):
        parts.append(f"{i}. **{r.title or ''}**\n{r.url}\n{r.description or ''}")
    return "\n\n".join(parts)
