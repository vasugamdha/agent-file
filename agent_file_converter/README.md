# Agent File Converter

A utility tool for converting Letta Agent Files (.af) to other popular agent frameworks.

## Currently Supported Conversions

- **Letta .af → LangChain**: Converts .af files to LangChain-compatible format
- **Letta .af → AutoGen**: Converts .af files to AutoGen-compatible format

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

This will generate a converted file with the same name as your input but with a `.langchain.json` extension.

### Specifying Output File

```bash
python af_converter.py --input /path/to/agent.af --output-format autogen --output my_converted_agent.json
```

### Examples

Convert a MemGPT agent to LangChain format:
```bash
python af_converter.py --input ../memgpt_agent/memgpt_agent.af --output-format langchain
```

Convert a Customer Service agent to AutoGen format:
```bash
python af_converter.py --input ../customer_service_agent/customer_service.af --output-format autogen
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
    }
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
    }
  }
}
```

## Limitations

- This converter focuses on the core components (system prompts, memory blocks, tools, and model configurations)
- Some framework-specific features might require additional manual configuration
- Environment variables and tool rules might need manual adjustment after conversion
- Message history is not converted due to framework-specific implementation differences

## Contributing

Feel free to contribute by adding support for additional frameworks or improving existing conversions!

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-framework-support`)
3. Commit your changes (`git commit -am 'Add support for new framework'`)
4. Push to the branch (`git push origin feature/new-framework-support`)
5. Create a new Pull Request 