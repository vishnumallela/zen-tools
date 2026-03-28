from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools._types import ToolDef
from zen_tools.tools.web import fetch, map_, search

DESCRIPTION = "Search the web and fetch content from any URL as markdown."
_ann = ToolAnnotations(readOnlyHint=True, openWorldHint=True)

TOOLS: list[ToolDef] = [
    ToolDef(fn=search.web_search, namespace="web", examples=search.EXAMPLES, annotations=_ann),
    ToolDef(fn=fetch.web_fetch, namespace="web", examples=fetch.EXAMPLES, annotations=_ann),
    ToolDef(fn=map_.web_map, namespace="web", examples=map_.EXAMPLES, annotations=_ann),
]
