from __future__ import annotations

import json
from typing import Annotated, Literal

import httpx
from pydantic import Field

EXAMPLES = """\
{ "operation": "get", "url": "https://api.example.com/users" }
{ "operation": "post", "url": "https://api.example.com/users", \
"headers": { "Content-Type": "application/json" }, "body": "{\\"name\\": \\"Alice\\"}" }\
"""


async def http_request(
    operation: Annotated[
        Literal["get", "post", "put", "patch", "delete"],
        Field(description="HTTP method"),
    ],
    url: Annotated[str, Field(description="Full URL including protocol")],
    headers: Annotated[
        dict[str, str] | None,
        Field(description="Request headers as key-value pairs"),
    ] = None,
    body: Annotated[
        str | None,
        Field(description="Request body string — use with post, put, patch"),
    ] = None,
    query: Annotated[
        dict[str, str] | None,
        Field(description="URL query params as key-value pairs"),
    ] = None,
) -> str:
    """Call REST APIs. Use this over web_fetch when you need custom headers, auth tokens,
    query params, or a request body. Auto-parses JSON responses."""
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=operation.upper(),
            url=url,
            headers=headers or {},
            content=body.encode() if body else None,
            params=query,
        )
    content_type = resp.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body_text = json.dumps(resp.json(), indent=2)
        except Exception:
            body_text = resp.text
    else:
        body_text = resp.text
    return f"HTTP {resp.status_code} {resp.reason_phrase}\n\n{body_text}"
