# API to MCP Server

This repo demonstrates how to convert any OpenAI compatible APIs to MCP Servers.

## Why MCP Servers over APIs?
For many scenarios an API can serve the same purpose as an MCP server, but they are not functionally identical and they solve slightly different problems.

Here is the practical comparison:

### When an API alone is enough

- You are only exposing data or services over the network
- You do not need streaming, tool discovery, or session based context
- Integration is straightforward and predefined
- APIs are great for direct request/response interactions.

### When MCP is a better fit

MCP servers are designed for tool integration with AI models in a structured and discoverable way. They offer:

- Tool discovery and schema based actions
- Live streaming or incremental results
- Session wide shared context
- A standard protocol for multiple AI clients


## Tech Stack
- Python
- FastMCP - https://gofastmcp.com/

## Example
For this example purpose, I have used openly available DogAPI - https://dogapi.dog/api-docs/v2/swagger.json

- **api-to-mcpserver.py** - An MCP Server which wraps all the dodapi. When the server is up, you can access using any MCP Client code to access the tools

- **mcpclient-example.py** - Using the same FastMCP, the client call demonstrates listing of all the available tools (useful to know the newly generated tool names by MCP Server) and calls one tool.

## How to execute the sample scripts

* Step 1: Start Server and keep it running
    * python api-to-mcpserver.py

* Step 2: Run client script
    * python mcpclient-example.py
