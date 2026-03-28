from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools import NamespaceInfo, register_namespace, register_tool
from zen_tools.tools.agent import research

_NS = "agent"

register_namespace(NamespaceInfo(name=_NS, description="Autonomous AI-powered research tasks."))

register_tool(
    research.agent_research,
    _NS,
    examples=research.EXAMPLES,
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
)
