import asyncio
from fastmcp import Client

# Initialize the client pointing to your MCP server endpoint
client = Client("http://localhost:8000/mcp")

# Define an asynchronous function to list and call tools

async def list_tools():
    async with client:
        # First, list all available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}")
        
asyncio.run(list_tools())


# List breeds api / mcp tool
async def call_tool():
    async with client:
        result = await client.call_tool("list_breeds" )
        print(result)


asyncio.run(call_tool())

