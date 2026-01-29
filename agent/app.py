import os

import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from agent.agent import TalkToYourDocumentAgent
from agent.prompts import SYSTEM_PROMPT
from agent.tools.base import BaseTool
from agent.tools.mcp.mcp_client import MCPClient
from agent.tools.mcp.mcp_tool import MCPTool
from agent.tools.py_interpreter.python_code_interpreter_tool import (
    PythonCodeInterpreterTool,
)

DIAL_ENDPOINT = os.getenv("DIAL_ENDPOINT", "http://localhost:8080")
AGENT_DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME", "qwen/qwen3-8b")


class TalkToYourDocumentAgentApplication(ChatCompletion):
    def __init__(self):
        self.tools: list[BaseTool] = []

    async def _create_tools(self) -> list[BaseTool]:
        tools: list[BaseTool] = []

        interpreter_tool = await PythonCodeInterpreterTool.create(
            mcp_url="http://localhost:8050/mcp",
            tool_name="execute_code",
            dial_endpoint=DIAL_ENDPOINT,
        )
        tools.append(interpreter_tool)

        calc_client = await MCPClient.create_stdio(
            command="docker", args=["run", "--rm", "-i", "calculator-mcp"]
        )

        mcp_tools = await calc_client.get_tools()

        for tool in mcp_tools:
            tools.append(MCPTool(client=calc_client, mcp_tool_model=tool))

        return tools

    async def chat_completion(self, request: Request, response: Response) -> None:
        if not self.tools:
            self.tools = await self._create_tools()

        with response.create_single_choice() as choice:
            agent = TalkToYourDocumentAgent(
                endpoint=DIAL_ENDPOINT,
                system_prompt=SYSTEM_PROMPT,
                tools=self.tools,
            )

            await agent.handle_request(
                deployment_name=AGENT_DEPLOYMENT_NAME,
                choice=choice,
                request=request,
                response=response,
            )


dial_app = DIALApp()
talk_to_your_document_agent_app = TalkToYourDocumentAgentApplication()
dial_app.add_chat_completion(
    deployment_name="talk-to-your-document-agent", impl=talk_to_your_document_agent_app
)

if __name__ == "__main__":
    uvicorn.run(dial_app, port=5030, host="0.0.0.0")
