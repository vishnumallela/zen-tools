from __future__ import annotations

import asyncio
from typing import Annotated, Literal

from pydantic import Field

from zen_tools.tools._firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com/docs" }
{ "url": "https://example.com/report.pdf", "pdf_mode": "ocr" }\
"""


async def web_fetch(
    url: Annotated[str, Field(description="URL to fetch")],
    pdf_mode: Annotated[
        Literal["auto", "fast", "ocr"] | None,
        Field(description="PDF parse mode — auto=default, fast=text-only, ocr=force OCR"),
    ] = None,
) -> str:
    """Fetch a single URL and return its content as markdown.
    Use when you already have a URL. Supports web pages and documents (PDF, Excel, Word)."""
    params: dict = {"formats": ["markdown"]}
    if pdf_mode:
        params["parsers"] = [{"type": "pdf", "mode": pdf_mode}]
    result = await asyncio.to_thread(client().scrape_url, url, **params)
    return getattr(result, "markdown", "") or ""
