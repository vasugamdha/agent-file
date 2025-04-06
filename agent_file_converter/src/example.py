#!/usr/bin/env python3
"""
Example usage of the Agent File Converter

This script demonstrates how to use the Agent File Converter programmatically.
"""

import os
import sys
import json

# Add the parent directory to path if necessary to find the module
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Import converters
try:
    from src.af_converter import LangChainConverter, AutoGenConverter
except ImportError:
    try:
        from af_converter import LangChainConverter, AutoGenConverter
    except ImportError:
        print("Error: Could not import converters. Make sure you're running from the right directory.")
        sys.exit(1)

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def create_test_agent_file(path, content):
    """Create a test agent file if it doesn't exist"""
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    
    if not os.path.exists(path):
        print(f"Creating test agent file: {path}")
        with open(path, 'w') as f:
            f.write(content)
    return path

def main():
    """Convert agent files to LangChain and AutoGen formats."""
    
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Input files
    memgpt_agent_path = os.path.join(parent_dir, "memgpt_agent", "memgpt_agent.af")
    customer_service_path = os.path.join(parent_dir, "customer_service_agent", "customer_service.af")
    
    # Create test agent files if they don't exist
    if not os.path.exists(memgpt_agent_path):
        memgpt_content = """
{
    "agent_name": "MemGPT Test Agent",
    "system_message": "You are MemGPT, an experimental AI assistant with a persistent memory.",
    "tools": [
        {
            "name": "memory_search",
            "description": "Search the agent's memory for specific information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "memory_store",
            "description": "Store information in the agent's memory",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "The memory key"
                    },
                    "value": {
                        "type": "string",
                        "description": "The information to store"
                    }
                },
                "required": ["key", "value"]
            }
        }
    ],
    "conversation_history": [
        {"role": "system", "content": "You are MemGPT, an experimental AI assistant with a persistent memory."},
        {"role": "user", "content": "Hello, can you introduce yourself?"},
        {"role": "assistant", "content": "I am MemGPT, an AI assistant with the ability to maintain persistent memory. I can recall our past conversations and store information for future reference. How can I assist you today?"}
    ]
}
"""
        create_test_agent_file(memgpt_agent_path, memgpt_content)
    
    if not os.path.exists(customer_service_path):
        customer_service_content = """
{
    "agent_name": "Customer Service Agent",
    "system_message": "You are a helpful customer service agent for a tech company.",
    "tools": [
        {
            "name": "lookup_order",
            "description": "Look up a customer's order by order ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID to look up"
                    }
                },
                "required": ["order_id"]
            }
        },
        {
            "name": "process_return",
            "description": "Process a return for a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID for the return"
                    },
                    "reason": {
                        "type": "string",
                        "description": "The reason for the return"
                    }
                },
                "required": ["order_id", "reason"]
            }
        }
    ],
    "conversation_history": [
        {"role": "system", "content": "You are a helpful customer service agent for a tech company."},
        {"role": "user", "content": "I need help with my order."},
        {"role": "assistant", "content": "I'd be happy to help with your order. Could you please provide your order ID so I can look up the details?"}
    ]
}
"""
        create_test_agent_file(customer_service_path, customer_service_content)
    
    # Output files
    output_dir = parent_dir
    langchain_output = os.path.join(output_dir, "memgpt_agent.langchain.json")
    autogen_output = os.path.join(output_dir, "customer_service.autogen.json")
    
    print(f"Converting {memgpt_agent_path} to LangChain format...")
    langchain_converter = LangChainConverter(memgpt_agent_path)
    langchain_json = langchain_converter.convert()
    
    with open(langchain_output, 'w') as f:
        json.dump(langchain_json, f, indent=2)
    print(f"Saved to {langchain_output}")
    
    print(f"Converting {customer_service_path} to AutoGen format...")
    autogen_converter = AutoGenConverter(customer_service_path)
    autogen_json = autogen_converter.convert()
    
    with open(autogen_output, 'w') as f:
        json.dump(autogen_json, f, indent=2)
    print(f"Saved to {autogen_output}")
    
    print("Conversion complete!")

if __name__ == "__main__":
    main() 