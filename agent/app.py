import os

import uvicorn
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response

from agent.agent import TalkToYourDocumentAgent
from agent.prompts import SYSTEM_PROMPT
from agent.tools.base import BaseTool


class TalkToYourDocumentAgentApplication(ChatCompletion):
    def __init__(self):
        self.tools: list[BaseTool] = []

    async def _create_tools(self) -> list[BaseTool]:
        tools: list[BaseTool] = []
        # TODO: add tools
        return tools

    async def chat_completion(self, request: Request, response: Response) -> None:
        if not self.tools:
            self.tools = await self._create_tools()

        with response.create_single_choice() as choice:
            agent = TalkToYourDocumentAgent(
                endpoint=os.getenv("DIAL_ENDPOINT", "http://localhost:8080"),
                system_prompt=SYSTEM_PROMPT,
                tools=self.tools,
            )
            await agent.handle_request(
                deployment_name=os.getenv("DEPLOYMENT_NAME", "mamaylm"),
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
