#!/usr/bin/env python3
"""
Test AutoGen Compatibility

This script tests compatibility with the AutoGen framework by:
1. Importing AutoGen packages
2. Loading a converted .autogen.json file
3. Extracting components (tools, memory, etc.)
4. Verifying the structure matches AutoGen expectations
"""

import os
import json
import sys
import importlib.util

def test_autogen_compatibility():
    print("Testing AutoGen compatibility...")
    
    # Try to import AutoGen
    try:
        # Check if the package is already imported
        autogen_spec = importlib.util.find_spec("autogen")
        
        if not autogen_spec:
            print("❌ Failed to import AutoGen. Please install with: pip install pyautogen")
            return False
            
        import autogen
        from autogen import Agent, AssistantAgent, UserProxyAgent, config_list_from_json
        print("✓ Successfully imported AutoGen packages")
    except (ImportError, ModuleNotFoundError) as e:
        print(f"❌ Failed to import AutoGen: {e}")
        print("   Please install with: pip install pyautogen")
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
    
    if not config.get('name'):
        print("❌ Missing agent name")
        return False
    
    # Check for valid model config
    model_config = config.get('model', {})
    if not model_config:
        print("⚠️ No model configuration found. Will use default model settings.")
    else:
        if not model_config.get('model_name'):
            print("⚠️ No model name specified. Will use default model.")
    
    # Verify tool format is compatible with AutoGen
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
    
    # Test creating an agent configuration
    agent_config = {
        "name": config.get('name'),
        "system_message": config.get('system_message', '')
    }
    
    # Add context summary if available
    if config.get('context_summary'):
        agent_config["system_message"] += f"\n\n{config.get('context_summary')}"
        print("✓ Added context summary to system message")
    
    # Extract function/tool definitions
    function_map = {}
    for tool_config in config.get('tools', []):
        # In a real implementation, you would implement actual tool functions
        # Here we just create mock functions for testing compatibility
        tool_name = tool_config['name']
        
        def create_mock_function(name):
            def mock_function(*args, **kwargs):
                return f"Mock response from {name}"
            return mock_function
        
        function_map[tool_name] = create_mock_function(tool_name)
    
    print(f"✓ Successfully extracted {len(function_map)} tools")
    
    # In a real implementation, you would set up the full AutoGen agent
    # For the compatibility test, we just verify we can build the config
    
    print("\n✅ Compatibility test succeeded!")
    print("The converted format should be compatible with AutoGen.")
    print("Note: For full functionality, you'll need to implement the actual tool functions.")
    
    return True

if __name__ == "__main__":
    success = test_autogen_compatibility()
    sys.exit(0 if success else 1) 