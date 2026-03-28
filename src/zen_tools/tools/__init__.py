from zen_tools.tools import agent, http, web
from zen_tools.tools._types import ToolDef

NAMESPACE_DESCRIPTIONS: dict[str, str] = {
    "web": web.DESCRIPTION,
    "agent": agent.DESCRIPTION,
    "http": http.DESCRIPTION,
}

ALL_TOOLS: list[ToolDef] = [*web.TOOLS, *agent.TOOLS, *http.TOOLS]
