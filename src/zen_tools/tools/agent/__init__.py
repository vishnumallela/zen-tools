from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools._types import ToolDef
from zen_tools.tools.agent import research

DESCRIPTION = "AI agent that browses multiple web sources and returns synthesized answers or structured data."
_ann = ToolAnnotations(readOnlyHint=True, openWorldHint=True)

TOOLS: list[ToolDef] = [
    ToolDef(fn=research.agent_research, namespace="agent", examples=research.EXAMPLES, annotations=_ann),
]
