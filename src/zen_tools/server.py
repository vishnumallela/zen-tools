from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_request
from fastmcp.server.middleware import Middleware, MiddlewareContext
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from zen_tools.docs import generate_docs_html
from zen_tools.tools import ALL_TOOLS

_TOOL_NAMES = {td.name for td in ALL_TOOLS}


class ToolScopingMiddleware(Middleware):
    """Limits each request to only the tools specified via ?tools= on the HTTP request."""

    def _allowed(self) -> set[str]:
        raw = get_http_request().query_params.get("tools", "")
        if not raw:
            return _TOOL_NAMES
        return {t.strip() for t in raw.split(",") if t.strip() in _TOOL_NAMES}

    async def on_list_tools(self, context: MiddlewareContext, call_next):
        allowed = self._allowed()
        return [t for t in await call_next(context) if t.name in allowed]

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        allowed = self._allowed()
        if len(allowed) < len(_TOOL_NAMES) and context.message.name not in allowed:
            raise ToolError(f"Tool '{context.message.name}' is not available in this session")
        return await call_next(context)


mcp = FastMCP("zen-tools", middleware=[ToolScopingMiddleware()])

for _td in ALL_TOOLS:
    mcp.tool(annotations=_td.annotations)(_td.fn)

_docs_html = generate_docs_html()


@mcp.custom_route("/health", methods=["GET"])
async def _health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "tools": sorted(_TOOL_NAMES)})


@mcp.custom_route("/", methods=["GET"])
@mcp.custom_route("/docs", methods=["GET"])
async def _docs(_: Request) -> HTMLResponse:
    return HTMLResponse(_docs_html)
