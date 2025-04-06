# Agent File Converter

A utility tool for converting Letta Agent Files (.af) to other popular agent frameworks.

## Currently Supported Conversions

- **Letta .af → LangChain**: Converts .af files to LangChain-compatible format
- **Letta .af → AutoGen**: Converts .af files to AutoGen-compatible format

## Key Features

- **Context Summary**: Automatically extracts and includes a concise summary of relevant context from the agent's memory (enabled by default)
- **Message History**: Option to include full conversation history (disabled by default to maintain token efficiency)
- **Tool Conversion**: Maps Letta tools to framework-specific tool formats
- **Memory Conversion**: Preserves persona and user information from memory blocks

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

This will generate a converted file with a context summary but without full message history.

### Including Message History

By default, message history is not included in the conversion to maintain token efficiency. To include it:

```bash
python af_converter.py --input /path/to/agent.af --output-format langchain --include-history
```

### Excluding Context Summary

By default, a context summary is included. To exclude it:

```bash
python af_converter.py --input /path/to/agent.af --output-format langchain --no-context-summary
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

Convert a Customer Service agent to AutoGen format with both context summary and message history:
```bash
python af_converter.py --input ../customer_service_agent/customer_service.af --output-format autogen --include-history
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
    "context_summary": "CONTEXT SUMMARY:\n- User: message content...\n- Assistant: response...",
    "message_history": [
      {
        "type": "human",
        "data": {
          "content": "...",
          "additional_kwargs": {}
        }
      },
      {
        "type": "ai",
        "data": {
          "content": "...",
          "additional_kwargs": {
            "tool_calls": [...]
          }
        }
      }
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
    "context_summary": "CONTEXT SUMMARY:\n- User: message content...\n- Assistant: response...",
    "chat_history": [
      {
        "role": "human",
        "content": "..."
      },
      {
        "role": "assistant",
        "content": "...",
        "function_call": {...}
      },
      {
        "role": "function",
        "name": "...",
        "content": "..."
      }
    ]
  }
}
```

## Context Summary vs. Full Message History

The converter provides two approaches to handling conversation context:

1. **Context Summary (Default)**: Extracts only the most relevant messages that would be in the agent's immediate context window, providing a concise summary that maintains the essential context with minimal token usage.

2. **Full Message History (Optional)**: Includes all messages exchanged between the user and agent, preserving the complete conversation history but potentially using more tokens.

This design aligns with MemGPT's token-efficient memory management philosophy, allowing you to choose the approach that best fits your needs.

## Programmatic Usage

You can also use the converter in your own Python scripts:

```python
from af_converter import LangChainConverter, AutoGenConverter

# Convert a Letta .af file to LangChain format
converter = LangChainConverter("path/to/agent.af")
langchain_data = converter.convert()

# Remove message history to maintain token efficiency (if needed)
if "message_history" in langchain_data["config"]:
    del langchain_data["config"]["message_history"]

# Save the converted data to a file
converter.save("output.langchain.json", langchain_data)
```

## Limitations

- This converter focuses on the core components (system prompts, memory blocks, tools, and model configurations)
- Some framework-specific features might require additional manual configuration
- Environment variables and tool rules might need manual adjustment after conversion

## Contributing

Feel free to contribute by adding support for additional frameworks or improving existing conversions!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-framework-support`)
3. Commit your changes (`git commit -am 'Add support for new framework'`)
4. Push to the branch (`git push origin feature/new-framework-support`)
5. Create a new Pull Request 