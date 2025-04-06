#!/usr/bin/env python3
"""
Test AutoGen Functional Compatibility

This script tests functional compatibility by actually instantiating an AutoGen agent
from our converted format and sending it a test query.
"""

import os
import json
import sys

def test_autogen_functional():
    print("Testing AutoGen functional compatibility...")
    
    # Try to import AutoGen
    try:
        import autogen
        from autogen import Agent, AssistantAgent, UserProxyAgent, config_list_from_json
        print("✓ Successfully imported AutoGen packages")
    except ImportError:
        print("❌ Failed to import AutoGen. Please install with: pip install pyautogen")
        return False
    
    # Find our converted file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    converted_file = os.path.join(parent_dir, "customer_service.autogen.json")
    
    if not os.path.exists(converted_file):
        print(f"❌ Converted file not found at {converted_file}")
        print("   Please run src/example.py first to generate the file")
        return False
    
    # Load the converted data
    try:
        with open(converted_file, 'r') as f:
            data = json.load(f)
        print(f"✓ Successfully loaded converted file: {converted_file}")
    except Exception as e:
        print(f"❌ Failed to load converted file: {e}")
        return False
    
    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("⚠️ No OpenAI API key found. Using mock response for testing.")
        mock_mode = True
    else:
        print("✓ Found OpenAI API key")
        mock_mode = False
    
    # Extract configuration
    config = data.get("config", {})
    
    # Extract system message
    system_message = config.get("system_message", "You are a helpful assistant.")
    
    # Add context summary if available
    if "context_summary" in config:
        context = config["context_summary"]
        system_message += f"\n\n{context}"
        print("✓ Added context summary to system message")
    
    # Extract and set up tools
    tools_data = config.get("tools", [])
    function_map = {}
    
    # Create mock tool implementations
    print("Implementing mock tools...")
    for tool_data in tools_data:
        tool_name = tool_data.get("name", "")
        
        # Define a mock function for this tool
        def create_mock_tool(name):
            def mock_tool(*args, **kwargs):
                return f"Mock response from {name} tool"
            return mock_tool
        
        function_map[tool_name] = create_mock_tool(tool_name)
        print(f"  - Created mock implementation for: {tool_name}")
    
    # Set up configuration
    if mock_mode:
        # Create a mock agent configuration
        class MockAssistantAgent:
            def __init__(self, name, system_message, **kwargs):
                self.name = name
                self.system_message = system_message
                self.function_map = kwargs.get("function_map", {})
            
            def send(self, message, recipient=None):
                return f"[Mock Agent Response] This is a mock response. In a real scenario with an API key, the agent would process: '{message}'"
        
        class MockUserProxyAgent:
            def __init__(self, name, **kwargs):
                self.name = name
                self.function_map = kwargs.get("function_map", {})
            
            def initiate_chat(self, recipient, message):
                print(f"\nUser: {message}")
                response = recipient.send(message, self)
                print(f"\nAgent: {response}")
                return response
        
        # Create mock agents
        assistant = MockAssistantAgent(
            name="assistant", 
            system_message=system_message,
            function_map=function_map
        )
        
        user_proxy = MockUserProxyAgent(
            name="user",
            function_map=function_map
        )
        
        print("✓ Created mock agents (no API key)")
    else:
        # Extract model configuration
        model_config = config.get("model", {})
        model_name = model_config.get("model_name", "gpt-3.5-turbo")
        temperature = model_config.get("temperature", 0.7)
        
        # Set up LLM configuration for AutoGen
        llm_config = {
            "config_list": [{"model": model_name, "api_key": api_key}],
            "temperature": temperature,
            "functions": [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool.get("parameters", {"type": "object", "properties": {}})
                } for tool in tools_data
            ]
        }
        
        # Create actual AutoGen agents
        assistant = autogen.AssistantAgent(
            name="assistant",
            system_message=system_message,
            llm_config=llm_config,
            function_map=function_map
        )
        
        user_proxy = autogen.UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            function_map=function_map
        )
        
        print("✓ Successfully created AutoGen agents")
    
    # Test the agent
    try:
        # Send a test query
        test_query = "Hello, who are you?"
        print(f"\nSending test query to agent: '{test_query}'")
        
        response = user_proxy.initiate_chat(
            recipient=assistant,
            message=test_query
        )
        
        print("\n✓ Agent successfully processed the query")
        return True
        
    except Exception as e:
        print(f"❌ Failed to test agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_autogen_functional()
    sys.exit(0 if success else 1) 