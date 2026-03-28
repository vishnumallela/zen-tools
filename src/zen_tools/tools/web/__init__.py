from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools import NamespaceInfo, register_namespace, register_tool
from zen_tools.tools.web import crawl, fetch, map_, search

_NS = "web"
_ann = ToolAnnotations(readOnlyHint=True, openWorldHint=True)

register_namespace(NamespaceInfo(name=_NS, description="Fetch and search web content."))

register_tool(search.web_search, _NS, examples=search.EXAMPLES, annotations=_ann)
register_tool(fetch.web_fetch, _NS, examples=fetch.EXAMPLES, annotations=_ann)
register_tool(crawl.web_crawl, _NS, examples=crawl.EXAMPLES, annotations=_ann)
register_tool(map_.web_map, _NS, examples=map_.EXAMPLES, annotations=_ann)
