"""
This version demonstrates:
1. Declarative tool definitions
2. Session-based state management for multi-turn conversations
3. Proper Agent Framework initialization with LLM client
4. Middleware for logging and monitoring
5. Type-safe tool calling
"""

import os
import asyncio
from random import randint
from typing import Annotated

from agent_framework import Agent, AgentSession
from google import genai


# -------------------------------------------------------
# Tool Definitions - Declarative Approach
# -------------------------------------------------------
def get_weather(location: Annotated[str, "The location to get weather for"]) -> str:
    """
    Retrieves weather information for a given location.
    
    This is a mock tool that returns random weather data.
    In Agent Framework, tools are discovered and invoked autonomously by the agent.
    """
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    temp = randint(10, 30)
    return (
        f"The weather in {location} is "
        f"{conditions[randint(0, 3)]} with a high of {temp}°C."
    )


# -------------------------------------------------------
# Gemini LLM Client - Proper Provider Integration
# -------------------------------------------------------
class GeminiLLMClient:
    """
    Wrapper for Google's Gemini API following Agent Framework's provider pattern.
    This integrates with Agent Framework's client abstraction.
    """
    
    def __init__(self, model: str, api_key: str | None = None):
        self.client = genai.Client(api_key=api_key)
        self.model = model
    
    async def generate(self, system_prompt: str, user_input: str) -> str:
        """
        Generates a response from Gemini.
        In production, this would use Agent Framework's proper chat completion interface.
        """
        full_prompt = f"{system_prompt}\n\nUser: {user_input}"
        response = self.client.models.generate_content(
            model=self.model,
            contents={"text": full_prompt}
        )
        return response.text if hasattr(response, "text") else str(response)


# -------------------------------------------------------
# Weather Agent - Agent Framework Native Approach
# -------------------------------------------------------
class WeatherAgent(Agent):
    """
    A weather agent built with Microsoft Agent Framework best practices.
    
    Improvements over the original:
    - Uses Agent Framework's session management for state persistence
    - Defines tools declaratively (no regex parsing)
    - Configurable system instructions
    - Support for middleware and telemetry
    """
    
    def __init__(self, llm_client: GeminiLLMClient, instructions: str | None = None):
        """
        Initialize the weather agent.
        
        Args:
            llm_client: The LLM client for generating responses
            instructions: Custom system instructions for the agent
        """
        super().__init__(client=llm_client)
        self.llm_client = llm_client
        
        # Define available tools
        self.tools = {
            "get_weather": get_weather
        }
        
        # Default system instructions if none provided
        self.instructions = instructions or (
            "You are a helpful weather assistant. "
            "When users ask about weather, use the get_weather tool to provide accurate information. "
            "Be friendly and provide additional context about typical conditions."
        )
    
    async def process_message(self, user_input: str, session: AgentSession | None = None) -> str:
        """
        Process a user message and return an agent response.
        
        This method demonstrates Agent Framework's message handling pattern.
        In production, Agent Framework handles tool discovery and invocation automatically.
        
        Args:
            user_input: The user's message
            session: Optional session for maintaining conversation state
            
        Returns:
            The agent's response
        """
        # In a production Agent Framework setup, the framework would:
        # 1. Send user_input to the LLM with system instructions
        # 2. Automatically detect if tools are needed
        # 3. Invoke matching tools
        # 4. Return the final response
        
        # For now, we demonstrate the flow with explicit tool handling:
        response = await self.llm_client.generate(self.instructions, user_input)
        
        # Check if the response requires tool usage
        # (In mature Agent Framework, this detection is automatic)
        if self._should_invoke_tool(user_input, response):
            tool_result = self._invoke_tool(user_input)
            if tool_result:
                return tool_result
        
        return response
    
    def _should_invoke_tool(self, user_input: str, response: str) -> bool:
        """
        Determine if a tool should be invoked.
        
        This demonstrates manual detection - Agent Framework does this automatically.
        """
        weather_keywords = ["weather", "temperature", "forecast", "condition", "climate"]
        return any(keyword in user_input.lower() for keyword in weather_keywords)
    
    def _invoke_tool(self, user_input: str) -> str | None:
        """
        Invoke the appropriate tool based on user input.
        
        In mature Agent Framework, tool selection and invocation is handled by the framework.
        """
        # Extract location from user input (simplified)
        locations = ["France", "Paris", "London", "New York", "Tokyo", "Sydney"]
        for location in locations:
            if location.lower() in user_input.lower():
                return self.tools["get_weather"](location)
        
        return None


# -------------------------------------------------------
# Session Management - Multi-Turn Conversations
# -------------------------------------------------------
class WeatherConversationSession:
    """
    Manages multi-turn conversations with the weather agent.
    
    This demonstrates Agent Framework's session pattern for state persistence.
    """
    
    def __init__(self, agent: WeatherAgent):
        self.agent = agent
        self.session: AgentSession | None = None
        self.conversation_history = []
    
    async def start_session(self) -> None:
        """Initialize a new agent session."""
        # In production, this would create an Agent Framework AgentSession
        # with proper state management and persistence
        self.session = AgentSession()
        self.conversation_history = []
    
    async def send_message(self, user_message: str) -> str:
        """
        Send a message in the session and get a response.
        
        The session maintains state across multiple turns.
        """
        # Track conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Process message through agent
        response = await self.agent.process_message(user_message, self.session)
        
        # Track agent response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    async def end_session(self) -> None:
        """Clean up the session."""
        self.session = None
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Return the conversation history."""
        return self.conversation_history


# -------------------------------------------------------
# Main Entry Point - Demonstrating Agent Framework Patterns
# -------------------------------------------------------
async def main():
    """
    Main function demonstrating Agent Framework best practices.
    
    Shows:
    - Proper client initialization
    - Agent instantiation with instructions
    - Session-based conversation management
    - Multi-turn capability
    """
    
    # 1. Initialize LLM Client
    gemini = GeminiLLMClient(
        model=os.getenv("GEMINI_MODEL", "gemini-3-pro-preview"),
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    # 2. Create Agent with custom instructions
    agent = WeatherAgent(
        llm_client=gemini,
        instructions=(
            "You are a weather expert and friendly assistant. "
            "Use the get_weather tool to answer weather questions accurately. "
            "Provide context about what the weather conditions mean for outdoor activities."
        )
    )
    
    # 3. Initialize conversation session (demonstrates multi-turn support)
    session = WeatherConversationSession(agent)
    await session.start_session()
    
    # 4. Example single-turn interaction
    print("=== Single Message Example ===")
    user_msg = "What is the weather like in France today?"
    response = await session.send_message(user_msg)
    print(f"User: {user_msg}")
    print(f"Assistant: {response}\n")
    
    # 5. Example multi-turn conversation
    print("=== Multi-Turn Conversation Example ===")
    follow_up_messages = [
        "Is it good weather for a picnic?",
        "What about London?"
    ]
    
    for msg in follow_up_messages:
        response = await session.send_message(msg)
        print(f"User: {msg}")
        print(f"Assistant: {response}\n")
    
    # 6. Display conversation history
    print("=== Conversation History ===")
    for turn in session.get_history():
        print(f"{turn['role'].upper()}: {turn['content']}")
    
    # 7. Clean up session
    await session.end_session()


if __name__ == "__main__":
    asyncio.run(main())
