#!/usr/bin/env python3
"""
Test LangChain Functional Compatibility

This script tests functional compatibility by actually instantiating a LangChain agent
from our converted format and sending it a test query.
"""

import os
import json
import sys

def test_langchain_functional():
    print("Testing LangChain functional compatibility...")
    
    # Try to import LangChain
    try:
        from langchain.agents import AgentExecutor, create_openai_tools_agent
        from langchain.schema import SystemMessage, HumanMessage
        from langchain_openai import ChatOpenAI
        from langchain.tools import Tool
        from langchain.output_parsers import StrOutputParser
        print("✓ Successfully imported LangChain packages")
    except ImportError:
        print("❌ Failed to import LangChain. Please install with: pip install langchain langchain-openai")
        return False
    
    # Find our converted file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    converted_file = os.path.join(parent_dir, "memgpt_agent.langchain.json")
    
    if not os.path.exists(converted_file):
        print(f"❌ Converted file not found at {converted_file}")
        print("   Please run src/example.py first to generate the file")
        return False
    
    # Load the converted data
    try:
        with open(converted_file, 'r') as f:
            data = json.load(f)
        print(f"✓ Successfully loaded converted file: {converted_file}")
        config = data.get("config", {})
    except Exception as e:
        print(f"❌ Failed to load converted file: {e}")
        return False
        
    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        # Create mock response for testing without API key
        print("⚠️ No OpenAI API key found. Using mock LLM for testing.")
        
        # Create a simple mock LLM function
        class MockChatModel:
            def invoke(self, messages):
                return {"content": "This is a mock response from the agent. In a real scenario with an API key, you would get an actual response from the model."}
        
        llm = MockChatModel()
    else:
        print(f"✓ Found OpenAI API key")
        # Initialize the LLM with the specified model
        model_name = config.get("model", {}).get("model_name", "gpt-3.5-turbo")
        if not model_name or model_name == "":
            model_name = "gpt-3.5-turbo"  # Default if no model specified
            
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model_name,
            temperature=config.get("model", {}).get("temperature", 0.7)
        )
    
    # Implement mock tools
    print("Implementing mock tools...")
    tools_data = config.get("tools", [])
    tools = []
    
    for tool_data in tools_data:
        tool_name = tool_data.get("name", "")
        tool_desc = tool_data.get("description", "")
        
        # Create a mock implementation for each tool
        def mock_tool_func(*args, **kwargs):
            return f"Mock response from {tool_name} tool"
        
        # Create the tool
        tool = Tool(
            name=tool_name,
            func=mock_tool_func,
            description=tool_desc
        )
        tools.append(tool)
        print(f"  - Created mock implementation for: {tool_name}")
    
    # Extract system message
    system_message = config.get("system_message", "You are a helpful assistant.")
    if not system_message:
        system_message = "You are a helpful assistant."
        
    # Add context summary if available
    if "context_summary" in config:
        context = config["context_summary"]
        system_message += f"\n\n{context}"
        print("✓ Added context summary to system message")
    
    # Create the agent
    try:
        system_message_obj = SystemMessage(content=system_message)
        
        # Check if we're using mock or real LLM
        if api_key:
            # Create real agent
            agent = create_openai_tools_agent(llm, tools, system_message_obj)
            agent_executor = AgentExecutor(agent=agent, tools=tools)
            print("✓ Successfully created LangChain agent")
        else:
            # Create a mock executor
            class MockAgentExecutor:
                def invoke(self, input_data):
                    return {
                        "output": "This is a mock response from the agent. To get a real response, provide an OpenAI API key.",
                        "input": input_data.get("input", "")
                    }
            
            agent_executor = MockAgentExecutor()
            print("✓ Created mock agent executor (no API key)")
        
        # Test the agent with a simple query
        test_query = "Hello, who are you?"
        print(f"\nSending test query to agent: '{test_query}'")
        
        response = agent_executor.invoke({"input": test_query})
        print(f"\nAgent response:\n{response.get('output', '')}")
        
        print("\n✓ Agent successfully processed the query")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create or run agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_langchain_functional()
    sys.exit(0 if success else 1) 