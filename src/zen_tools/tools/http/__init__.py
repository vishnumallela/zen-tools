from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools._types import ToolDef
from zen_tools.tools.http import request

DESCRIPTION = "Make HTTP requests to external APIs."

TOOLS: list[ToolDef] = [
    ToolDef(
        fn=request.http_request,
        namespace="http",
        examples=request.EXAMPLES,
        annotations=ToolAnnotations(openWorldHint=True, destructiveHint=True),
    ),
]
