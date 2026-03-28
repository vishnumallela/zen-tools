from typing import Annotated, Literal

from firecrawl.v2.types import PDFParser

from zen_tools.clients.firecrawl import client

EXAMPLES = """\
{ "url": "https://example.com/docs" }
{ "url": "https://example.com/report.pdf" }
{ "url": "https://example.com/scanned.pdf", "pdf_mode": "ocr" }\
"""


async def web_fetch(
    url: Annotated[str, "URL to fetch. Supports web pages and document files (PDF, Word, Excel, PowerPoint)."],
    pdf_mode: Annotated[
        Literal["auto", "fast", "ocr"] | None,
        "PDF parse mode. fast=text-only no OCR, ocr=force OCR for scanned documents. Omit for default.",
    ] = None,
) -> str:
    """Fetch any URL and return its full content as markdown.
    Returns: the full page or document content as a markdown string, with headings, tables, and lists preserved.
    Use when you have a URL for a web page or document file and need its full content.
    Not for API calls that need custom headers or a request body. Use http_request instead."""
    result = await client().scrape(
        url,
        formats=["markdown"],
        parsers=[PDFParser(mode=pdf_mode)] if pdf_mode else None,
    )
    return result.markdown or ""
