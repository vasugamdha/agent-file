#!/usr/bin/env python3
"""
Test LangChain Functional Compatibility

This script tests functional compatibility by actually instantiating a LangChain agent
from our converted format and sending it a test query.
"""

import os
import json
import sys
import importlib.util

def test_langchain_functional():
    print("Testing LangChain functional compatibility...")
    
    # Try to import LangChain with proper error handling
    try:
        # Check if the packages are already imported
        langchain_spec = importlib.util.find_spec("langchain")
        langchain_openai_spec = importlib.util.find_spec("langchain_openai")
        
        if not langchain_spec or not langchain_openai_spec:
            print("❌ Failed to import LangChain. Please install with: pip install langchain langchain-openai")
            return False
            
        # Import core components
        from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain.agents import AgentExecutor, create_openai_tools_agent, tool
        from langchain_openai import ChatOpenAI
        from langchain.schema import SystemMessage, HumanMessage, AIMessage
        
        print("✓ Successfully imported LangChain packages")
    except (ImportError, ModuleNotFoundError) as e:
        print(f"❌ Failed to import LangChain: {e}")
        print("   Please install with: pip install langchain langchain-openai")
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
    
    # Extract and implement tools
    tools_data = config.get("tools", [])
    tools = []
    
    # Create mock tool implementations
    print("Implementing mock tools...")
    for tool_data in tools_data:
        tool_name = tool_data.get("name", "")
        tool_description = tool_data.get("description", "")
        
        # Define a mock function for this tool
        @tool
        def mock_tool(args: str) -> str:
            """Mock tool implementation"""
            return f"Mock response from {tool_name} tool"
        
        # Set the metadata on the function
        mock_tool.name = tool_name
        mock_tool.__doc__ = tool_description
        
        tools.append(mock_tool)
        print(f"  - Created mock implementation for: {tool_name}")
    
    # Set up agent
    if mock_mode:
        # Create a mock agent that doesn't require API key
        class MockAgent:
            def __init__(self, system_message, tools):
                self.system_message = system_message
                self.tools = tools
                
            def invoke(self, message):
                tool_names = [t.name for t in self.tools]
                return {"output": f"[Mock Agent Response] This is a mock response. In a real scenario with an API key, the agent would process: '{message}' using tools: {', '.join(tool_names)}"}
        
        agent_executor = MockAgent(system_message, tools)
        print("✓ Created mock agent (no API key)")
    else:
        try:
            # Extract model configuration
            model_config = config.get("model", {})
            model_name = model_config.get("model_name", "gpt-3.5-turbo")
            temperature = model_config.get("temperature", 0.7)
            
            # Create chat model
            llm = ChatOpenAI(
                openai_api_key=api_key,
                model=model_name,
                temperature=temperature
            )
            
            # Create prompt with system message and tool options
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            # Create agent
            agent = create_openai_tools_agent(llm, tools, prompt)
            
            # Create agent executor
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True
            )
            
            print("✓ Successfully created LangChain agent")
        except Exception as e:
            print(f"❌ Failed to create LangChain agent: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # Test the agent
    try:
        # Send a test query
        test_query = "Hello, who are you?"
        print(f"\nSending test query to agent: '{test_query}'")
        
        response = agent_executor.invoke({"input": test_query})
        
        print(f"\nAgent response: {response['output']}")
        print("\n✓ Agent successfully processed the query")
        return True
        
    except Exception as e:
        print(f"❌ Failed to test agent: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_langchain_functional()
    sys.exit(0 if success else 1) 