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
        print("Breeds List :",result)

asyncio.run(call_tool())


# List breeds api / mcp tool by id
async def call_tool(id: str):
    async with client:
        result = await client.call_tool("get_breed_with_non_existing_id", {"id":"dd9362cc-52e0-462d-b856-fccdcf24b140"})
        print("Breeds by ID :", result)

asyncio.run(call_tool(1))

