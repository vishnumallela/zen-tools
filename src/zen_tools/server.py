from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_request
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.function_tool import FunctionTool
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

from zen_tools.docs import generate_docs_html
from zen_tools.tools import ALL_TOOLS


class ToolScopingMiddleware(Middleware):
    """Limits each request to only the tools specified via ?tools= on the HTTP request."""

    def _allowed(self) -> set[str]:
        raw = get_http_request().query_params.get("tools", "")
        if not raw:
            return set(ALL_TOOLS.keys())
        return {t.strip() for t in raw.split(",") if t.strip() in ALL_TOOLS}

    async def on_list_tools(self, context: MiddlewareContext, call_next):
        tools = await call_next(context)
        allowed = self._allowed()
        return [t for t in tools if t.name in allowed]

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        allowed = self._allowed()
        if len(allowed) < len(ALL_TOOLS) and context.message.name not in allowed:
            raise ToolError(f"Tool '{context.message.name}' is not available in this session")
        return await call_next(context)


mcp = FastMCP("zen-tools", middleware=[ToolScopingMiddleware()])

for tool_def in ALL_TOOLS.values():
    tool = FunctionTool.from_function(tool_def.fn, annotations=tool_def.annotations)
    mcp.add_tool(tool)

_docs_html = generate_docs_html()


@mcp.custom_route("/health", methods=["GET"])
async def _health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "tools": list(ALL_TOOLS.keys())})


@mcp.custom_route("/", methods=["GET"])
@mcp.custom_route("/docs", methods=["GET"])
async def _docs(_: Request) -> HTMLResponse:
    return HTMLResponse(_docs_html)
