from __future__ import annotations

import asyncio
import json
from typing import Annotated, Literal

from pydantic import Field

from zen_tools.tools._firecrawl import client

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
        Field(
            description="research=free-form prose answer, extract=structured JSON matching schema"
        ),
    ],
    prompt: Annotated[
        str,
        Field(description="What data to find — describe the target information clearly"),
    ],
    urls: Annotated[
        str | None,
        Field(description="Comma-separated URLs to restrict research to specific pages"),
    ] = None,
    schema: Annotated[
        str | None,
        Field(description="JSON schema string for structured output — required for extract"),
    ] = None,
    model: Annotated[
        Literal["mini", "pro"],
        Field(description="mini=default (faster, cheaper), pro=higher accuracy for complex tasks"),
    ] = "mini",
) -> str:
    """Autonomous AI agent that reasons across the web.
    Use over web_search when the answer requires visiting multiple pages, comparing sources,
    or returning structured data. research=prose answer, extract=JSON matching your schema."""
    url_list = [u.strip() for u in urls.split(",") if u.strip()] if urls else None
    parsed_schema: dict | None = json.loads(schema) if schema else None
    model_id = "spark-1-pro" if model == "pro" else "spark-1-mini"

    kwargs: dict = {"prompt": prompt, "model": model_id}
    if url_list:
        kwargs["urls"] = url_list
    if parsed_schema:
        kwargs["schema"] = parsed_schema

    result = await asyncio.to_thread(client().agent, **kwargs)
    data = getattr(result, "data", None)
    if operation == "extract" or not isinstance(data, str):
        return json.dumps(data, indent=2)
    return data or "No data returned."
