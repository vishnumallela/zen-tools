from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fastmcp.tools.tool import ToolAnnotations


@dataclass
class NamespaceInfo:
    name: str
    description: str


@dataclass
class ToolDef:
    name: str
    fn: Callable
    namespace: str
    examples: str | None = None
    annotations: ToolAnnotations | None = None

    @property
    def description(self) -> str:
        return (self.fn.__doc__ or "").strip()


ALL_TOOLS: dict[str, ToolDef] = {}
NAMESPACES: list[NamespaceInfo] = []


def register_namespace(info: NamespaceInfo) -> None:
    NAMESPACES.append(info)


def register_tool(
    fn: Callable,
    namespace: str,
    *,
    name: str | None = None,
    examples: str | None = None,
    annotations: ToolAnnotations | None = None,
) -> ToolDef:
    tool_name = name or fn.__name__
    td = ToolDef(
        name=tool_name, fn=fn, namespace=namespace, examples=examples, annotations=annotations
    )
    ALL_TOOLS[tool_name] = td
    return td


from zen_tools.tools.agent import *  # noqa: E402, F401, F403
from zen_tools.tools.http_ns import *  # noqa: E402, F401, F403
from zen_tools.tools.web import *  # noqa: E402, F401, F403
