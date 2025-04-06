#!/usr/bin/env python3
"""
Example usage of the Agent File Converter

This script demonstrates how to use the Agent File Converter programmatically.
"""

from af_converter import LangChainConverter, AutoGenConverter
import os
import json

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def main():
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Example 1: Convert MemGPT agent to LangChain
    memgpt_path = os.path.join(project_dir, "memgpt_agent", "memgpt_agent.af")
    if os.path.exists(memgpt_path):
        print(f"Converting {memgpt_path} to LangChain format...")
        converter = LangChainConverter(memgpt_path)
        langchain_data = converter.convert()
        
        # Save the output to a file
        output_path = os.path.join(script_dir, "memgpt_agent.langchain.json")
        converter.save(output_path, langchain_data)
        print(f"Saved LangChain format to {output_path}")
        
        # Preview some of the converted data
        print("\nLangChain format preview:")
        print("-------------------------")
        print(f"System message length: {len(langchain_data['config']['system_message'])} characters")
        print(f"Memory keys: {list(langchain_data['config']['memory'].keys())}")
        print(f"Number of tools: {len(langchain_data['config']['tools'])}")
        print(f"Model: {langchain_data['config']['model']['provider']}/{langchain_data['config']['model']['model_name']}")
    else:
        print(f"MemGPT agent file not found at {memgpt_path}")
    
    # Example 2: Convert Customer Service agent to AutoGen
    cs_path = os.path.join(project_dir, "customer_service_agent", "customer_service.af")
    if os.path.exists(cs_path):
        print(f"\nConverting {cs_path} to AutoGen format...")
        converter = AutoGenConverter(cs_path)
        autogen_data = converter.convert()
        
        # Save the output to a file
        output_path = os.path.join(script_dir, "customer_service.autogen.json")
        converter.save(output_path, autogen_data)
        print(f"Saved AutoGen format to {output_path}")
        
        # Preview some of the converted data
        print("\nAutoGen format preview:")
        print("----------------------")
        print(f"Agent name: {autogen_data['config']['name']}")
        print(f"System message length: {len(autogen_data['config']['system_message'])} characters")
        print(f"Memory keys: {list(autogen_data['config']['memory'].keys())}")
        print(f"Number of tools: {len(autogen_data['config']['tools'])}")
        print(f"Model: {autogen_data['config']['llm_config']['config_list'][0]['model']}")
    else:
        print(f"Customer Service agent file not found at {cs_path}")
    
    # Example 3: Convert MemGPT agent with conversation history to LangChain
    memgpt_convo_path = os.path.join(project_dir, "memgpt_agent", "memgpt_agent_with_convo.af")
    if os.path.exists(memgpt_convo_path):
        print(f"\nConverting {memgpt_convo_path} to LangChain format with message history...")
        converter = LangChainConverter(memgpt_convo_path)
        langchain_data = converter.convert()
        
        # Save the output to a file
        output_path = os.path.join(script_dir, "memgpt_agent_with_history.langchain.json")
        converter.save(output_path, langchain_data)
        print(f"Saved LangChain format with message history to {output_path}")
        
        # Preview the message history
        message_history = langchain_data['config'].get('message_history', [])
        print("\nLangChain message history preview:")
        print("----------------------------------")
        print(f"Total messages: {len(message_history)}")
        if message_history:
            print(f"First message type: {message_history[0]['type']}")
            print(f"First message content (brief): {message_history[0]['data']['content'][:50]}...")
            
            # Count message types
            message_types = {}
            for msg in message_history:
                msg_type = msg['type']
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
            print(f"Message type distribution: {message_types}")
    else:
        print(f"MemGPT agent with conversation file not found at {memgpt_convo_path}")

if __name__ == "__main__":
    main() 