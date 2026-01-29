from typing import Any, Optional

from pydantic import BaseModel


class MCPToolModel(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: dict[str, Any]
