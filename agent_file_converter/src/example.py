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
    
    # Example 3: Compare context summary vs. full history (token usage)
    memgpt_convo_path = os.path.join(project_dir, "memgpt_agent", "memgpt_agent_with_convo.af")
    if os.path.exists(memgpt_convo_path):
        print(f"\n=== CONTEXT SUMMARY VS FULL HISTORY COMPARISON ===")
        print(f"Converting {memgpt_convo_path} to LangChain format...")
        
        # CONTEXT SUMMARY ONLY
        converter = LangChainConverter(memgpt_convo_path)
        summary_data = converter.convert()
        
        # Remove message history to only show context summary
        if 'message_history' in summary_data['config']:
            del summary_data['config']['message_history']
            
        summary_path = os.path.join(script_dir, "example_summary_only.json")
        converter.save(summary_path, summary_data)
        print(f"Saved with context summary only to: {summary_path}")
        
        # Preview the context summary (first 3 lines)
        context_summary = summary_data['config'].get('context_summary', "No context summary available")
        preview_lines = context_summary.split('\n')[:4]
        print("\nContext summary preview:")
        print("------------------------")
        for line in preview_lines:
            print(line)
        print("...")
        
        # FULL HISTORY
        full_data = converter.convert()  # Re-convert to get full data
        full_path = os.path.join(script_dir, "example_with_history.json")
        converter.save(full_path, full_data)
        print(f"\nSaved with full message history to: {full_path}")
        
        # Calculate token usage comparison
        summary_chars = len(json.dumps(summary_data))
        full_chars = len(json.dumps(full_data))
        
        # Approximate token count (4 chars ≈ 1 token)
        summary_tokens = summary_chars / 4
        full_tokens = full_chars / 4
        
        # Display comparison
        print("\nToken usage comparison:")
        print(f"Context summary only: ~{int(summary_tokens):,} tokens")
        print(f"With full history: ~{int(full_tokens):,} tokens")
        print(f"Token reduction: ~{int(full_tokens - summary_tokens):,} tokens ({(full_tokens - summary_tokens) / full_tokens * 100:.2f}%)")
        
        # Show cost estimate (GPT-4 price point)
        summary_cost = (summary_tokens / 1000) * 0.01
        full_cost = (full_tokens / 1000) * 0.01
        print(f"\nEstimated cost at $0.01 per 1K tokens:")
        print(f"Context summary only: ${summary_cost:.4f}")
        print(f"With full history: ${full_cost:.4f}")
        print(f"Cost savings: ${full_cost - summary_cost:.4f} ({(full_cost - summary_cost) / full_cost * 100:.2f}%)")
    else:
        print(f"MemGPT agent with conversation file not found at {memgpt_convo_path}")

if __name__ == "__main__":
    main() 