#!/usr/bin/env python3
"""
Agent File (.af) Converter

This script converts Letta Agent Files (.af) to other popular agent frameworks.
Currently supports conversion to:
- LangChain
- AutoGen

Usage:
    python af_converter.py --input agent.af --output-format langchain
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Any, Optional, Union

class AgentFileConverter:
    """Base class for converting Agent Files to other formats"""
    
    def __init__(self, input_file: str):
        """Initialize the converter with an input .af file"""
        self.input_file = input_file
        self.agent_data = self._load_agent_file()
    
    def _load_agent_file(self) -> Dict[str, Any]:
        """Load and parse the .af file"""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {self.input_file} is not a valid JSON file")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: {self.input_file} not found")
            sys.exit(1)
    
    def convert(self) -> Dict[str, Any]:
        """Convert the .af file to the target format (abstract method)"""
        raise NotImplementedError("Subclasses must implement this method")
    
    def save(self, output_file: str, data: Dict[str, Any]) -> None:
        """Save the converted data to a file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Converted file saved to: {output_file}")
    
    def _extract_message_history(self) -> List[Dict[str, Any]]:
        """Extract message history from the .af file"""
        messages = self.agent_data.get("messages", [])
        # Filter out system messages if needed
        return [msg for msg in messages if msg.get("role") != "system"]
    
    def _get_message_content(self, message: Dict[str, Any]) -> str:
        """Extract text content from a message"""
        content = message.get("content", [])
        if not content:
            return ""
        
        # Handle both string content and structured content
        if isinstance(content, str):
            return content
        
        # Handle array of content parts
        if isinstance(content, list):
            text_parts = []
            for part in content:
                # Handle text content parts
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                # Handle string content parts directly
                elif isinstance(part, str):
                    text_parts.append(part)
            
            return "\n".join(text_parts)
        
        # Fallback for unexpected content structure
        try:
            return str(content)
        except:
            return "Content could not be extracted"

class LangChainConverter(AgentFileConverter):
    """Converts Agent Files to LangChain format"""
    
    def convert(self) -> Dict[str, Any]:
        """Convert to LangChain format"""
        # Extract system prompt
        system_prompt = self.agent_data.get("system_prompt", "")
        
        # Extract memory blocks
        memory_blocks = self.agent_data.get("memory_blocks", [])
        
        # Extract tools
        tools = self.agent_data.get("tools", [])
        
        # Extract model configuration
        model_config = self.agent_data.get("model_config", {})
        
        # Extract message history
        message_history = self._convert_message_history()
        
        # Build LangChain compatible format
        langchain_format = {
            "agent_type": "langchain",
            "config": {
                "system_message": system_prompt,
                "memory": self._convert_memory(memory_blocks),
                "tools": self._convert_tools(tools),
                "model": self._convert_model_config(model_config),
                "message_history": message_history
            }
        }
        
        return langchain_format
    
    def _convert_memory(self, memory_blocks: List[Dict[str, Any]]) -> Dict[str, str]:
        """Convert memory blocks to LangChain memory format"""
        memory = {}
        for block in memory_blocks:
            if block.get("label") and block.get("value"):
                memory[block["label"]] = block["value"]
        return memory
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tools to LangChain tool format"""
        langchain_tools = []
        for tool in tools:
            if not tool.get("name"):
                continue
                
            langchain_tool = {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "schema": tool.get("schema", {})
            }
            
            # If the tool has code, add it as a function string
            if tool.get("code"):
                langchain_tool["function_string"] = tool["code"]
                
            langchain_tools.append(langchain_tool)
            
        return langchain_tools
    
    def _convert_model_config(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert model configuration to LangChain format"""
        return {
            "provider": "openai" if "openai" in model_config.get("model", "") else "default",
            "model_name": model_config.get("model", "").split("/")[-1],
            "temperature": model_config.get("temperature", 0.7),
            "max_tokens": model_config.get("max_tokens", None)
        }
    
    def _convert_message_history(self) -> List[Dict[str, Any]]:
        """Convert message history to LangChain format"""
        messages = self._extract_message_history()
        langchain_messages = []
        
        for msg in messages:
            role = msg.get("role", "")
            if role not in ["user", "assistant"]:
                continue
                
            content = self._get_message_content(msg)
            
            # Map roles to LangChain format
            lc_role = "human" if role == "user" else "ai"
            
            langchain_message = {
                "type": lc_role,
                "data": {
                    "content": content,
                    "additional_kwargs": {}
                }
            }
            
            # If tool calls are present in assistant messages, add them
            if role == "assistant" and msg.get("tool_calls"):
                tool_calls = []
                for tool_call in msg.get("tool_calls", []):
                    if tool_call.get("function"):
                        tool_calls.append({
                            "name": tool_call["function"].get("name", ""),
                            "arguments": json.loads(tool_call["function"].get("arguments", "{}"))
                        })
                
                if tool_calls:
                    langchain_message["data"]["additional_kwargs"]["tool_calls"] = tool_calls
            
            # Add tool returns if present
            if msg.get("tool_returns"):
                tool_returns = []
                for tool_return in msg.get("tool_returns", []):
                    tool_returns.append({
                        "tool_call_id": tool_return.get("tool_call_id", ""),
                        "content": tool_return.get("content", "")
                    })
                
                if tool_returns:
                    langchain_message["data"]["additional_kwargs"]["tool_returns"] = tool_returns
            
            langchain_messages.append(langchain_message)
        
        return langchain_messages

class AutoGenConverter(AgentFileConverter):
    """Converts Agent Files to AutoGen format"""
    
    def convert(self) -> Dict[str, Any]:
        """Convert to AutoGen format"""
        # Extract system prompt
        system_prompt = self.agent_data.get("system_prompt", "")
        
        # Extract memory blocks
        memory_blocks = self.agent_data.get("memory_blocks", [])
        
        # Extract tools
        tools = self.agent_data.get("tools", [])
        
        # Extract model configuration
        model_config = self.agent_data.get("model_config", {})
        
        # Extract message history
        message_history = self._convert_message_history()
        
        # Build AutoGen compatible format
        autogen_format = {
            "agent_type": "autogen",
            "config": {
                "name": self.agent_data.get("name", "Converted Agent"),
                "system_message": system_prompt,
                "human_input_mode": "NEVER",
                "max_consecutive_auto_reply": 10,
                "memory": self._convert_memory(memory_blocks),
                "tools": self._convert_tools(tools),
                "llm_config": self._convert_model_config(model_config),
                "chat_history": message_history
            }
        }
        
        return autogen_format
    
    def _convert_memory(self, memory_blocks: List[Dict[str, Any]]) -> Dict[str, str]:
        """Convert memory blocks to AutoGen memory format"""
        memory = {}
        for block in memory_blocks:
            if block.get("label") and block.get("value"):
                memory[block["label"]] = block["value"]
        return memory
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert tools to AutoGen tool format"""
        autogen_tools = []
        for tool in tools:
            if not tool.get("name"):
                continue
                
            autogen_tool = {
                "name": tool.get("name", ""),
                "description": tool.get("description", ""),
                "parameters": tool.get("schema", {}).get("properties", {})
            }
            
            # If the tool has code, add it as a function string
            if tool.get("code"):
                autogen_tool["implementation"] = tool["code"]
                
            autogen_tools.append(autogen_tool)
            
        return autogen_tools
    
    def _convert_model_config(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert model configuration to AutoGen format"""
        return {
            "config_list": [{
                "model": model_config.get("model", "").split("/")[-1],
                "temperature": model_config.get("temperature", 0.7),
                "max_tokens": model_config.get("max_tokens", None)
            }]
        }
    
    def _convert_message_history(self) -> List[Dict[str, Any]]:
        """Convert message history to AutoGen format"""
        messages = self._extract_message_history()
        autogen_messages = []
        
        for msg in messages:
            role = msg.get("role", "")
            if role not in ["user", "assistant"]:
                continue
                
            content = self._get_message_content(msg)
            
            # Map roles to AutoGen format
            ag_role = "human" if role == "user" else "assistant"
            
            autogen_message = {
                "role": ag_role,
                "content": content
            }
            
            # If tool calls are present in assistant messages, add them
            if role == "assistant" and msg.get("tool_calls"):
                function_calls = []
                for tool_call in msg.get("tool_calls", []):
                    if tool_call.get("function"):
                        function_calls.append({
                            "name": tool_call["function"].get("name", ""),
                            "arguments": tool_call["function"].get("arguments", "{}")
                        })
                
                if function_calls:
                    autogen_message["function_call"] = function_calls[0]  # AutoGen typically uses the first function call
            
            # Add tool returns if present
            if msg.get("tool_returns"):
                # In AutoGen, function responses are separate messages
                for tool_return in msg.get("tool_returns", []):
                    tool_return_msg = {
                        "role": "function",
                        "name": tool_return.get("name", "unknown_function"),
                        "content": tool_return.get("content", "")
                    }
                    autogen_messages.append(tool_return_msg)
                    
            autogen_messages.append(autogen_message)
        
        return autogen_messages

def main():
    parser = argparse.ArgumentParser(description="Convert Agent Files (.af) to other frameworks")
    parser.add_argument("--input", required=True, help="Input .af file path")
    parser.add_argument("--output-format", required=True, choices=["langchain", "autogen"], 
                        help="Target framework format")
    parser.add_argument("--output", help="Output file path (default: input filename with new extension)")
    parser.add_argument("--include-history", action="store_true", default=False,
                       help="Include message history in the conversion (default: False)")
    
    args = parser.parse_args()
    
    # Determine output file if not specified
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}.{args.output_format}.json"
    
    # Select the appropriate converter based on the target format
    converter_class = None
    if args.output_format == "langchain":
        converter_class = LangChainConverter
    elif args.output_format == "autogen":
        converter_class = AutoGenConverter
    
    if converter_class:
        converter = converter_class(args.input)
        converted_data = converter.convert()
        
        # Remove message history if not requested
        if not args.include_history:
            if args.output_format == "langchain" and "message_history" in converted_data["config"]:
                del converted_data["config"]["message_history"]
            elif args.output_format == "autogen" and "chat_history" in converted_data["config"]:
                del converted_data["config"]["chat_history"]
        
        converter.save(args.output, converted_data)
        print(f"Conversion completed with{'' if args.include_history else 'out'} message history")
    else:
        print(f"Error: Unsupported output format: {args.output_format}")
        sys.exit(1)

if __name__ == "__main__":
    main() 