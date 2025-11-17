import os
import httpx
import json
from fastmcp import FastMCP
from dotenv import load_dotenv # Recommended for loading secrets

os.environ['FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER'] = 'true'

# --- 1. SETUP: LOAD SECRETS AND CONFIGURATION ---

# NOTE: Ensure you have a .env file with your API key, or export it manually
load_dotenv()

# The URL where your external API's OpenAPI specification is available
OPENAPI_SPEC_URL = "https://dogapi.dog/api-docs/v2/swagger.json"

# The base URL of the actual external API endpoints
API_BASE_URL = "https://dogapi.dog/api/v2"


# The secret key for authenticating with the external API
# API_KEY = os.environ.get("EXTERNAL_API_TOKEN")

# if not API_KEY:
#    raise EnvironmentError("EXTERNAL_API_TOKEN environment variable not set. Cannot authenticate API.")

# --- 2. FETCH SPEC AND CONFIGURE AUTHENTICATED HTTP CLIENT ---

def run_mcp_server_from_openapi_with_auth():
    """Fetches the OpenAPI spec and initializes the authenticated MCP server."""
    
    # 1. Configure the HTTP Client with Authentication Headers
    # This client will be used by FastMCP to make ALL requests to the external API.
    authenticated_client = httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers={
            # This header is sent to the EXTERNAL API with every tool call
#            "Authorization": f"Bearer {API_KEY}", 
            "Content-Type": "application/json"
        },
        timeout=10.0 # Set a request timeout
    )
    
    print("--- ⚙️  Fetching OpenAPI Specification... ---")
    try:
        # Fetch the OpenAPI JSON using the configured client (without credentials, 
        # unless the spec endpoint itself is protected)
        spec_response = httpx.get(OPENAPI_SPEC_URL, timeout=10.0)
        spec_response.raise_for_status()
        openapi_spec = spec_response.json()
        print("Spec Response: ",spec_response)
    except httpx.HTTPError as e:
        print(f"\nFATAL ERROR: Failed to fetch OpenAPI spec from {OPENAPI_SPEC_URL}. {e}")
        return
        
    # --- 3. AUTO-GENERATE MCP SERVER ---
    
    # FastMCP.from_openapi() converts the spec into MCP Tools/Resources.
    # By passing 'authenticated_client', we ensure all subsequent proxied requests 
    # inherit the 'Authorization' header.
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=authenticated_client,
        name="Authenticated API Wrapper"
    )
    
    print("--- ✅ MCP Server Auto-Generated with Authentication! ---")

    # print(dir(mcp))
#    print(f"Generated Tools: {', '.join(mcp.tools.keys())}")

    paths = openapi_spec.get("paths", {}) if isinstance(openapi_spec, dict) else {}
    if paths:
       print("Available API paths exposed via MCP:")
       for p, ops in sorted(paths.items()):
            if isinstance(ops, dict):
                methods = ", ".join(m.upper() for m in ops.keys())
            else:
                methods = repr(ops)
            print(f"  {p} -> {methods}")
    else:
        print("No paths found in OpenAPI spec.")


    print("--- 🚀 Running MCP Server... ---")
    
    # Run the generated MCP server
    #mcp.run(transport='stdio')
    mcp.run(transport='http', host='127.0.0.1', port=8000)

# --- 4. EXECUTE ---

if __name__ == "__main__":
    run_mcp_server_from_openapi_with_auth()