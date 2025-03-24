# Agent File (.af): A file format for stateful agents 

Agent File (.af) is an open standard file format for serializing stateful agents. Originally designed for the [Letta](https://letta.com) framework, Agent File provides a portable, standardized way to share agents with persistent memory and behavior.

Agent Files encapsulate all of the components of a stateful agent:
- Core memory blocks storing agent personality and user information
- Tool configurations for interacting with external systems
- Memory management settings and archival data connections
- LLM provider configurations and model parameters

By standardizing these components in a single file format, Agent File enables seamless transfer of agents between systems, promotes collaboration among developers, and simplifies deployment across environments.

## Download agents

|      Agent Type      | Description | Download (.af) | Source Code |
|----------------------|-------------|----------------|-------------|
| MemGPT Agent       | An agent with memory management tools for infinite context, as described in the MemGPT paper | [Download](https://example.com/item1.af) | [link](github.com) |
| MemGPT Agent with chat history     | A MemGPT agent that is pre-populated with an extended chat history and memories | [Download](https://example.com/item1.af) | [link](github.com) |
| Deep Research Agent| A agent with planning, search, and memory tools to enable writing deep research reports | [Download](https://example.com/item2.af) | [link](github.com) |
| Customer Support Agent | A customer support agent that has dummy tools for handling order cancellations, looking up order status, and also memory | [Download](https://example.com/item3.af) | [link](github.com) |
| Composio Agent | An example of an agent that uses a Composio tool to star a GitHub repository | [Download](https://example.com/item3.af) | [link](github.com) |
| Workflow Agent | A stateless workflow agent with no memory and deterministic tool calling workflows | [Download](https://example.com/item4.af) | [link](github.com) |

## FAQ

### Why Agent File?

The AI ecosystem is witnessing rapid growth in agent development, with each framework implementing its own storage mechanisms. Agent File addresses the need for a standard that enables:

- **Portability**: Move agents between systems or deploy them to new environments
- **Collaboration**: Share your agents with other developers and the community
- **Preservation**: Archive agent configurations to preserve your work
- **Versioning**: Track changes to agents over time through a standardized format

### What state does .af include? 

An .af files contains all the state required to re-create the exact same agent: 
* Model configuration (context window limit, model name, embedding model name)
* Full message history 
* Field `in_context` denotes whether the message is still in the context window 
* System prompt 
* In-context memory blocks 
* Tool rules 
* Tool environment variables 
* Tools (source code, json schema) 
We currently do not support Passages (the units of Archival Memory), which have support for them on the roadmap.

You can view the entire schema of .af in the Letta repository [here](https://github.com/letta-ai/letta/blob/main/letta/serialize_schemas/pydantic_agent_schema.py). 

### Does .af work with frameworks other than Letta? 
Theoretically, other framework could also load in .af files if they convert the state into their own representations. Some concepts, such as context window “blocks” which can be edited or shared between agents, are not implemented in other frameworks, so may need to be adapted per-framework. 

### How does .af handle secrets? 
Agents have associated secrets for tool execution. When you export agents with secrets, the secrets are set to `null`. 
