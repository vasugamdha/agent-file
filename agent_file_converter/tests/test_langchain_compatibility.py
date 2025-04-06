#!/usr/bin/env python3
"""
Test LangChain Compatibility

This script tests compatibility with the LangChain framework by:
1. Importing LangChain packages
2. Loading a converted .langchain.json file
3. Extracting components (tools, memory, etc.)
4. Verifying the structure matches LangChain expectations
"""

import os
import json
import sys
import importlib.util

def test_langchain_compatibility():
    print("Testing LangChain compatibility...")
    
    # Try to import LangChain
    try:
        # Check if the packages are already imported
        langchain_spec = importlib.util.find_spec("langchain")
        langchain_openai_spec = importlib.util.find_spec("langchain_openai")
        
        if not langchain_spec or not langchain_openai_spec:
            print("❌ Failed to import LangChain. Please install with: pip install langchain langchain-openai")
            return False
            
        import langchain
        from langchain.agents import tool
        from langchain.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
        
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
    
    # Verify the expected structure
    if 'config' not in data:
        print("❌ Invalid format: missing 'config' key")
        return False
    
    config = data['config']
    
    # Check for essential components
    if not config.get('system_message'):
        print("❌ Missing system_message")
        return False
    
    if not isinstance(config.get('tools', []), list):
        print("❌ Tools should be a list")
        return False
    
    if not isinstance(config.get('memory', {}), dict):
        print("❌ Memory should be a dictionary")
        return False
    
    # Check for valid model config
    model_config = config.get('model', {})
    if not model_config:
        print("⚠️ No model configuration found. Will use default model settings.")
    else:
        if not model_config.get('model_name'):
            print("⚠️ No model name specified. Will use default model.")
    
    # Verify tool format is compatible with LangChain
    for tool in config.get('tools', []):
        if not tool.get('name'):
            print("❌ Tool missing name")
            return False
        if not tool.get('description'):
            print("❌ Tool missing description")
            return False
        if 'parameters' not in tool:
            print("❌ Tool missing parameters schema")
            return False
    
    print("✓ All required components validated")
    
    # Test creating tools from the configuration
    tools = []
    for tool_config in config.get('tools', []):
        # In a real implementation, you would implement actual tool functions
        # Here we just create mock functions for testing compatibility
        tool_name = tool_config['name']
        tool_description = tool_config['description']
        
        # Create a simple function without using decorator
        def create_mock_function(name):
            def mock_function(input_str: str) -> str:
                """Mock tool implementation"""
                return f"Mock response from {name}"
            return mock_function
            
        mock_func = create_mock_function(tool_name)
        
        # Create a simple mock tool object
        mock_tool = {
            "name": tool_name,
            "description": tool_description,
            "func": mock_func
        }
        
        tools.append(mock_tool)
    
    print(f"✓ Successfully extracted {len(tools)} tools")
    
    # Test system message with context summary
    system_message = config.get('system_message', '')
    if config.get('context_summary'):
        system_message += f"\n\n{config.get('context_summary')}"
        print("✓ Added context summary to system message")
    
    print("\n✅ Compatibility test succeeded!")
    print("The converted format should be compatible with LangChain.")
    print("Note: For full functionality, you'll need to implement the actual tool functions.")
    
    return True

if __name__ == "__main__":
    success = test_langchain_compatibility()
    sys.exit(0 if success else 1) 