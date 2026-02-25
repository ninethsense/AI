
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent

async def main():
    model_client = OpenAIChatCompletionClient(
        model="mistral-large-3",
        api_key="<your-key>",
        base_url="https://<url>.openai.azure.com/openai/v1/",       
        temperature=0.0,
        model_info={
            
            "response_format": "text",
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "mistral-large-3",
            "structured_output": False,
        }
    )

  

    agent = AssistantAgent("assistant", model_client=model_client)
    result = await agent.run(task="What's the weather like in New Delhi?")
    print(result)
  
asyncio.run(main())
