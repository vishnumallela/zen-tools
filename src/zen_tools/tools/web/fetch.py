from typing import Annotated, Literal

from firecrawl.v2.types import Document, PDFParser

from zen_tools.clients.firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com/docs" }
{ "url": "https://example.com/report.pdf", "pdf_mode": "ocr" }\
"""


async def web_fetch(
    url: Annotated[str, "URL to fetch"],
    pdf_mode: Annotated[
        Literal["auto", "fast", "ocr"] | None,
        "PDF parse mode — auto=default, fast=text-only, ocr=force OCR",
    ] = None,
) -> str:
    """Fetch a single URL and return its content as markdown.
    Use when you already have a URL. Supports web pages and documents (PDF, Excel, Word)."""
    parsers = [PDFParser(mode=pdf_mode)] if pdf_mode else None
    result: Document = await client().scrape(url, formats=["markdown"], parsers=parsers)
    return result.markdown or ""
