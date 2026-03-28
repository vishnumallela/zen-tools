from collections.abc import Callable

from fastmcp.tools.tool import ToolAnnotations
from pydantic import BaseModel, ConfigDict


class ToolDef(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    fn: Callable
    namespace: str
    examples: str | None = None
    annotations: ToolAnnotations | None = None

    @property
    def name(self) -> str:
        return self.fn.__name__

    @property
    def description(self) -> str:
        return (self.fn.__doc__ or "").strip()
