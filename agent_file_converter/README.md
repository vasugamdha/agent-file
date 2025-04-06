# Agent File Converter

A utility tool for converting Letta Agent Files (.af) to other popular agent frameworks.

## Currently Supported Conversions

- **Letta .af → LangChain**: Converts .af files to LangChain-compatible format
- **Letta .af → AutoGen**: Converts .af files to AutoGen-compatible format

## Key Features

- **Context Summary:** Automatically extracts and summarizes the most important context from message history, reducing token usage by ~90% compared to full conversation history.
- **Message History:** Optionally include the full message history for complete conversation context.
- **Tool Conversion:** Maps Letta tools to framework-specific formats.
- **Memory Preservation:** Maintains core memory blocks (persona, human info).

## Installation

```bash
# Clone this repository (if you haven't already)
git clone https://github.com/letta-ai/agent-file.git
cd agent-file/agent_file_converter

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python af_converter.py --input /path/to/agent.af --output-format langchain
```

This will generate a converted file with context summary (but without full message history) and saves it with appropriate extension.

### Including Message History

By default, the converter only includes a concise context summary. To include the full message history:

```bash
python af_converter.py --input /path/to/agent.af --output-format langchain --include-history
```

### Disabling Context Summary

If you don't want to include the context summary:

```bash
python af_converter.py --input /path/to/agent.af --output-format autogen --no-context-summary
```

### Specifying Output File

```bash
python af_converter.py --input /path/to/agent.af --output-format autogen --output my_converted_agent.json
```

### Examples

Convert a MemGPT agent to LangChain format with context summary:
```bash
python af_converter.py --input ../memgpt_agent/memgpt_agent.af --output-format langchain
```

Convert a Customer Service agent to AutoGen format with full message history:
```bash
python af_converter.py --input ../customer_service_agent/customer_service.af --output-format autogen --include-history
```

## Context Summary vs. Full History

The context summary feature is inspired by MemGPT's approach to memory management. Instead of including the entire conversation history (which can be token-heavy), the converter extracts only the most relevant messages based on the agent's context window indices.

Benefits:
- **Token Efficiency:** Reduces token usage by ~90% compared to full history
- **Preserved Context:** Maintains the most relevant parts of the conversation
- **Framework Compatibility:** Makes Letta agents more compatible with other frameworks that don't have the same sophisticated memory management

Example of token usage comparison:
```
File size comparison:
Context summary only: 2.5 KB (~621 tokens)
With full history: 31.9 KB (~7979 tokens)
Token reduction: ~7358 tokens (92%)
```

## Output Format

### LangChain Output

The LangChain output is structured as follows:

```json
{
  "agent_type": "langchain",
  "config": {
    "system_message": "...",
    "memory": {
      "persona": "...",
      "human": "..."
    },
    "tools": [...],
    "model": {
      "provider": "openai",
      "model_name": "gpt-4-0613",
      "temperature": 0.7,
      "max_tokens": null
    },
    "context_summary": "Context summary:\n- User: ...\n- Assistant: ...",
    "message_history": [
      // Optional, included with --include-history flag
    ]
  }
}
```

### AutoGen Output

The AutoGen output is structured as follows:

```json
{
  "agent_type": "autogen",
  "config": {
    "name": "...",
    "system_message": "...",
    "human_input_mode": "NEVER",
    "max_consecutive_auto_reply": 10,
    "memory": {
      "persona": "...",
      "human": "..."
    },
    "tools": [...],
    "llm_config": {
      "config_list": [{
        "model": "gpt-4-0613",
        "temperature": 0.7,
        "max_tokens": null
      }]
    },
    "context_summary": "Context summary:\n- User: ...\n- Assistant: ...",
    "chat_history": [
      // Optional, included with --include-history flag
    ]
  }
}
```

## Programmatic Usage

You can also use the converter in your own Python scripts:

```python
from af_converter import LangChainConverter, AutoGenConverter

# Convert a Letta .af file to LangChain format with context summary only
converter = LangChainConverter("path/to/agent.af")
langchain_data = converter.convert()

# Remove full message history if you only want context summary
if 'message_history' in langchain_data['config']:
    del langchain_data['config']['message_history']

# Save the converted data to a file
converter.save("output.json", langchain_data)

# For full message history, just use the data as-is
converter = AutoGenConverter("path/to/agent.af")
autogen_data = converter.convert()
converter.save("output_with_history.json", autogen_data)
```

## Advantages Over the Original .af Format

- **Token Efficiency:** Context summaries capture essential conversation context with minimal token usage
- **Framework Compatibility:** Makes Letta agents usable with popular frameworks
- **Flexibility:** Choose between concise summaries or full conversation history

## Limitations

- The context summary is based on the in-context message indices in the original .af file
- Some framework-specific features might require additional manual configuration
- Environment variables and tool rules might need manual adjustment after conversion

## Contributing

Feel free to contribute by adding support for additional frameworks or improving existing conversions!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-framework-support`)
3. Commit your changes (`git commit -am 'Add support for new framework'`)
4. Push to the branch (`git push origin feature/new-framework-support`)
5. Create a new Pull Request 