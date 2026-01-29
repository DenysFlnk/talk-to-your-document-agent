from typing import Any, Optional

from mcp import ClientSession, ListToolsResult, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    BlobResourceContents,
    CallToolResult,
    ReadResourceResult,
    TextContent,
    TextResourceContents,
)
from pydantic import AnyUrl

from agent.tools.mcp.mcp_tool_model import MCPToolModel


class MCPClient:
    """Handles MCP server connection and tool execution"""

    def __init__(
        self, mcp_server_url: str = None, stdio_params: StdioServerParameters = None
    ) -> None:
        self.server_url = mcp_server_url
        self.stdio_params = stdio_params
        self.session: Optional[ClientSession] = None
        self._streams_context = None
        self._session_context = None

    @classmethod
    async def create_stdio(cls, command: str, args: list[str]) -> "MCPClient":
        """Create stdio-based MCP client (for Docker calculator)"""
        stdio_params = StdioServerParameters(command=command, args=args)
        instance = cls(stdio_params=stdio_params)
        await instance.connect_stdio()
        return instance

    async def connect_stdio(self):
        """Connect to stdio-based MCP server"""
        if self.session:
            return

        self._streams_context = stdio_client(self.stdio_params)
        read_stream, write_stream = await self._streams_context.__aenter__()

        self._session_context = ClientSession(read_stream, write_stream)
        self.session = await self._session_context.__aenter__()

        await self.session.initialize()

    async def get_tools(self) -> list[MCPToolModel]:
        """Get available tools from MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")

        tool_result: ListToolsResult = await self.session.list_tools()

        mcp_models = []

        for tool in tool_result.tools:
            mcp_models.append(
                MCPToolModel(
                    name=tool.name,
                    description=tool.description,
                    parameters=tool.inputSchema,
                )
            )

        return mcp_models

    async def call_tool(self, tool_name: str, tool_args: dict[str, Any]) -> Any:
        """Call a tool on the MCP server"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")

        print(f"    Calling `{tool_name}` with {tool_args}")

        tool_result: CallToolResult = await self.session.call_tool(tool_name, tool_args)

        if not tool_result.content:
            return None

        content = tool_result.content[0]

        if isinstance(content, TextContent):
            return content.text

        return content

    async def get_resource(self, uri: AnyUrl) -> str | bytes:
        """Get specific resource content"""
        if not self.session:
            raise RuntimeError("MCP client not connected.")

        resource: ReadResourceResult = await self.session.read_resource(uri)

        if not resource.contents:
            raise RuntimeError(f"Resource {uri} not found")

        content = resource.contents[0]

        if isinstance(content, TextResourceContents):
            return content.text
        elif isinstance(content, BlobResourceContents):
            return content.blob

        raise RuntimeError(f"Error while fetching resource {uri}")

    async def close(self):
        """Close connection to MCP server"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)

        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        return False
