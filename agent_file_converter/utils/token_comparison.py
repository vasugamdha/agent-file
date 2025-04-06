#!/usr/bin/env python3
"""
Token Comparison Script

This script compares the token usage between context summary and full message history.
"""

import os
import json
from af_converter import LangChainConverter

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Path to the agent file with conversation
    agent_path = os.path.join(project_dir, "memgpt_agent", "memgpt_agent_with_convo.af")
    
    if not os.path.exists(agent_path):
        print(f"Error: Agent file not found at {agent_path}")
        return
    
    print("=" * 80)
    print("CONTEXT SUMMARY VS FULL HISTORY: TOKEN COMPARISON")
    print("=" * 80)
    
    # Convert with context summary only
    converter = LangChainConverter(agent_path)
    summary_data = converter.convert()
    
    # Remove message history
    if 'message_history' in summary_data['config']:
        del summary_data['config']['message_history']
    
    summary_path = os.path.join(script_dir, "token_test_summary.json")
    converter.save(summary_path, summary_data)
    
    # Convert with full history
    history_data = converter.convert()  # Re-convert to get full data
    history_path = os.path.join(script_dir, "token_test_history.json") 
    converter.save(history_path, history_data)
    
    # Calculate sizes
    summary_size = os.path.getsize(summary_path)
    history_size = os.path.getsize(history_path)
    
    # Character counts in JSON
    summary_chars = len(json.dumps(summary_data))
    history_chars = len(json.dumps(history_data))
    
    # Approximate token counts (4 chars ≈ 1 token)
    summary_tokens = summary_chars / 4
    history_tokens = history_chars / 4
    
    # Display results
    print("\nFile Size Comparison:")
    print(f"Context Summary: {summary_size / 1024:.2f} KB")
    print(f"Full History:    {history_size / 1024:.2f} KB")
    print(f"Reduction:       {(history_size - summary_size) / 1024:.2f} KB ({(history_size - summary_size) / history_size * 100:.2f}%)")
    
    print("\nCharacter Count Comparison:")
    print(f"Context Summary: {summary_chars:,} characters")
    print(f"Full History:    {history_chars:,} characters")
    print(f"Reduction:       {history_chars - summary_chars:,} characters ({(history_chars - summary_chars) / history_chars * 100:.2f}%)")
    
    print("\nToken Usage Comparison (Estimated):")
    print(f"Context Summary: ~{int(summary_tokens):,} tokens")
    print(f"Full History:    ~{int(history_tokens):,} tokens")
    print(f"Token Savings:   ~{int(history_tokens - summary_tokens):,} tokens ({(history_tokens - summary_tokens) / history_tokens * 100:.2f}%)")
    
    print("\nWith an LLM cost of $0.01 per 1K tokens (like GPT-4):")
    summary_cost = (summary_tokens / 1000) * 0.01
    history_cost = (history_tokens / 1000) * 0.01
    print(f"Context Summary: ${summary_cost:.4f}")
    print(f"Full History:    ${history_cost:.4f}")
    print(f"Cost Savings:    ${history_cost - summary_cost:.4f} ({(history_cost - summary_cost) / history_cost * 100:.2f}%)")

if __name__ == "__main__":
    main() 