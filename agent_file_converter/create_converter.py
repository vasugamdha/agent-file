#!/usr/bin/env python3
"""
Converter Template Generator

This script generates a template for a new framework converter class.
"""

import os
import sys
import textwrap

def create_converter_template(framework_name):
    """Create a template for a new framework converter"""
    class_name = f"{framework_name.title()}Converter"
    
    template = textwrap.dedent(f'''
    class {class_name}(AgentFileConverter):
        """Converts Agent Files to {framework_name} format"""
        
        def convert(self) -> Dict[str, Any]:
            """Convert to {framework_name} format"""
            # Extract system prompt
            system_prompt = self.agent_data.get("system_prompt", "")
            
            # Extract memory blocks
            memory_blocks = self.agent_data.get("memory_blocks", [])
            
            # Extract tools
            tools = self.agent_data.get("tools", [])
            
            # Extract model configuration
            model_config = self.agent_data.get("model_config", {{}})
            
            # Build {framework_name} compatible format
            {framework_name.lower()}_format = {{{{
                "agent_type": "{framework_name.lower()}",
                "config": {{{{
                    "name": self.agent_data.get("name", "Converted Agent"),
                    "system_message": system_prompt,
                    # Add framework-specific configuration here
                    "memory": self._convert_memory(memory_blocks),
                    "tools": self._convert_tools(tools),
                    "model": self._convert_model_config(model_config)
                }}}}
            }}}}
            
            return {framework_name.lower()}_format
        
        def _convert_memory(self, memory_blocks: List[Dict[str, Any]]) -> Dict[str, str]:
            """Convert memory blocks to {framework_name} memory format"""
            memory = {{{{}}}}
            for block in memory_blocks:
                if block.get("label") and block.get("value"):
                    memory[block["label"]] = block["value"]
            return memory
        
        def _convert_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Convert tools to {framework_name} tool format"""
            {framework_name.lower()}_tools = []
            for tool in tools:
                if not tool.get("name"):
                    continue
                    
                {framework_name.lower()}_tool = {{{{
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    # Add framework-specific tool properties here
                }}}}
                
                # If the tool has code, add it in the framework-specific way
                if tool.get("code"):
                    {framework_name.lower()}_tool["function_string"] = tool["code"]
                    
                {framework_name.lower()}_tools.append({framework_name.lower()}_tool)
                
            return {framework_name.lower()}_tools
        
        def _convert_model_config(self, model_config: Dict[str, Any]) -> Dict[str, Any]:
            """Convert model configuration to {framework_name} format"""
            return {{{{
                # Add framework-specific model configuration here
                "model_name": model_config.get("model", "").split("/")[-1],
                "temperature": model_config.get("temperature", 0.7),
                "max_tokens": model_config.get("max_tokens", None)
            }}}}
    ''')
    
    # Create the output file
    output_file = f"{framework_name.lower()}_converter_template.py"
    with open(output_file, 'w') as f:
        f.write(template.strip())
    
    print(f"Created converter template for {framework_name} at {output_file}")
    print("\nTo use this converter:")
    print(f"1. Copy the {class_name} class into af_converter.py")
    print(f"2. Add '{framework_name.lower()}' to the choices in the argparse configuration")
    print(f"3. Add a case for {framework_name.lower()} in the converter selection logic")
    print(f"4. Customize the conversion logic for {framework_name}-specific formats")

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_converter.py <framework_name>")
        sys.exit(1)
    
    framework_name = sys.argv[1]
    create_converter_template(framework_name)

if __name__ == "__main__":
    main() 