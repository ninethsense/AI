
import asyncio
import os
from random import randint
from typing import Annotated
from pydantic import Field

from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import tool

async def main() -> None:
    client = AzureOpenAIResponsesClient(
        endpoint=os.environ["gpt_5_chat_endpoint"],
        deployment_name=os.environ["gpt_5_chat_deployment"],
        api_key=os.environ["gpt_5_chat_api_key"]    
    )

    agent = client.as_agent(
        name="WeatherAgent",
        instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
        tools=[get_weather]
    )

    result = await agent.run("What is the current weather like in France?")
    print(f"Agent: {result}")

# This is a simple tool that simulates getting the weather for a given location.
@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."

if __name__ == "__main__":
    asyncio.run(main())
