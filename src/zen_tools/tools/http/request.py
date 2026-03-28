import json
from typing import Annotated, Literal

import httpx

EXAMPLES = """\
{ "operation": "get", "url": "https://api.example.com/users" }
{ "operation": "post", "url": "https://api.example.com/users", \
"headers": { "Content-Type": "application/json" }, "body": "{\\"name\\": \\"Alice\\"}" }\
"""


async def http_request(
    operation: Annotated[Literal["get", "post", "put", "patch", "delete"], "HTTP method."],
    url: Annotated[str, "Full URL including protocol."],
    headers: Annotated[dict[str, str] | None, "Request headers as key-value pairs."] = None,
    body: Annotated[str | None, "Request body string. Use with post, put, and patch."] = None,
    query: Annotated[dict[str, str] | None, "URL query parameters as key-value pairs."] = None,
) -> str:
    """Make an HTTP request to a REST API endpoint and return the response.
    Returns: status line followed by the response body. JSON responses are pretty-printed, all others as plain text.
    Use when the target requires a specific HTTP method, custom headers, auth tokens, or a request body.
    Not for reading web pages or documents. Use web_fetch instead."""
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
