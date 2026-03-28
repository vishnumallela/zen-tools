from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools import NamespaceInfo, register_namespace, register_tool
from zen_tools.tools.http_ns import request

_NS = "http"

register_namespace(NamespaceInfo(name=_NS, description="Make HTTP requests to external APIs."))

register_tool(
    request.http_request,
    _NS,
    examples=request.EXAMPLES,
    annotations=ToolAnnotations(openWorldHint=True, destructiveHint=True),
)
