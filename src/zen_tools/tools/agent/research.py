import json
from typing import Annotated, Literal

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
        "Output mode. research=prose answer, extract=structured JSON matching the provided schema.",
    ],
    prompt: Annotated[str, "What to find or extract. Describe the target information clearly."],
    urls: Annotated[
        str | None, "Comma-separated URLs to restrict the agent to specific pages. Omit to search the open web."
    ] = None,
    schema: Annotated[
        str | None, "JSON schema string describing the output shape. Required when operation is extract."
    ] = None,
    model: Annotated[
        Literal["mini", "pro"], "Model to use. mini=faster and cheaper, pro=higher accuracy. Default is mini."
    ] = "mini",
) -> str:
    """Deploy an AI agent to autonomously browse the web, reason across multiple pages, and return a synthesized answer.
    Returns: prose markdown when operation is research, or a JSON object matching your schema when operation is extract.
    Use when the task requires visiting multiple sources, comparing information, or extracting structured data from the web.
    Not for fetching a single known URL. Use web_fetch instead.
    Not for keyword discovery. Use web_search instead.
    This is slower and more resource-intensive than other tools. Only use when multi-source reasoning is needed."""
    url_list = [u.strip() for u in urls.split(",") if u.strip()] if urls else None
    parsed_schema: dict | None = json.loads(schema) if schema else None

    result = await client().agent(
        urls=url_list,
        prompt=prompt,
        schema=parsed_schema,
        model="spark-1-pro" if model == "pro" else "spark-1-mini",
    )
    if operation == "extract" or not isinstance(result.data, str):
        return json.dumps(result.data, indent=2)
    return result.data or "No data returned."
