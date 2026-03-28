from fastmcp.tools.tool import ToolAnnotations

from zen_tools.tools._types import ToolDef
from zen_tools.tools.agent import research

DESCRIPTION = "Autonomous AI-powered research tasks."

TOOLS: list[ToolDef] = [
    ToolDef(
        fn=research.agent_research,
        namespace="agent",
        examples=research.EXAMPLES,
        annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True),
    ),
]
