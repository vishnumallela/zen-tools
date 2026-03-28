import json
from typing import Annotated, Literal

from firecrawl.v2.types import AgentResponse

from zen_tools.clients.firecrawl import client

EXAMPLES = """\
{ "operation": "research", "prompt": "Find the top 5 AI startups and their funding amounts" }
{ "operation": "extract", "prompt": "Get pricing plans from example.com", \
"schema": "{\\"type\\":\\"object\\",\\"properties\\":{\\"plans\\":{\\"type\\":\\"array\\"}}}" }
{ "operation": "research", "prompt": "Compare features", \
"urls": "https://example.com,https://example2.com", "model": "pro" }\
"""


async def agent_research(
    operation: Annotated[
        Literal["research", "extract"],
        "research=free-form prose answer, extract=structured JSON matching schema",
    ],
    prompt: Annotated[str, "What data to find — describe the target information clearly"],
    urls: Annotated[
        str | None, "Comma-separated URLs to restrict research to specific pages"
    ] = None,
    schema: Annotated[
        str | None, "JSON schema string for structured output — required for extract"
    ] = None,
    model: Annotated[
        Literal["mini", "pro"], "mini=default (faster, cheaper), pro=higher accuracy"
    ] = "mini",
) -> str:
    """Autonomous AI agent that reasons across the web.
    Use over web_search when the answer requires visiting multiple pages, comparing sources,
    or returning structured data. research=prose answer, extract=JSON matching your schema."""
    url_list = [u.strip() for u in urls.split(",") if u.strip()] if urls else None
    parsed_schema: dict | None = json.loads(schema) if schema else None

    result: AgentResponse = await client().agent(
        urls=url_list,
        prompt=prompt,
        schema=parsed_schema,
        model="spark-1-pro" if model == "pro" else "spark-1-mini",
    )
    if operation == "extract" or not isinstance(result.data, str):
        return json.dumps(result.data, indent=2)
    return result.data or "No data returned."
