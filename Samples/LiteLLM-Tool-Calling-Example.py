import json

from litellm import completion
import os

azure_api_key = os.getenv("gpt_5_chat_api_key")
azure_api_base = os.getenv("gpt_5_chat_endpoint")
azure_deployment = os.getenv("gpt_5_chat_deployment")

def get_random_number():
    import random
    return f"You just hit the custom tool.\nRandom number: {random.randint(1, 100)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_random_number",
            "description": "Return a random number",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
                }
        }
    }
]

try:
    response = completion(
        model="azure/" + azure_deployment,
        api_key=azure_api_key,
        api_base=azure_api_base,
        messages=[{"content": "Give a random number using the tool", "role": "user"}],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_random_number"}}
    )
    #print("Response:\n", json.dumps(response.model_dump(), indent=2))
    
    # Note that LiteLLM do not execute the tool calls for you, you need to do it yourself. This is because LiteLLM is designed to be a lightweight and flexible library that can be used in a variety of environments, including those where executing arbitrary code may not be safe or desirable.
    tool_calls = response.choices[0].message.get("tool_calls")

    if tool_calls:
        for tool_call in tool_calls:
            if tool_call["function"]["name"] == "get_random_number":
                tool_response = get_random_number()
                print("Tool response:\n", tool_response)

except Exception as e:
    print("Error calling completion:\n", repr(e))
    raise
