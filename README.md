<a href="https://docs.letta.com/">
  <img alt="Agent File (.af): An open standard file format for stateful agents." src="/assets/agentfile.png">
</a>

<p align="center">
    <br /><b>Agent File (.af): An open file format for stateful agents</b>.
</p>

<div align="center">
  
[![Discord](https://img.shields.io/discord/1161736243340640419?label=Discord&logo=discord&logoColor=5865F2&style=flat-square&color=5865F2)](https://discord.gg/letta)
[![GitHub](https://img.shields.io/github/stars/letta-ai/agent-file?style=flat-square&logo=github&label=Stars&color=gold)](https://github.com/letta-ai/agent-file)
[![License](https://img.shields.io/badge/License-Apache%202.0-silver?style=flat-square)](LICENSE)

</div>

<p align="center">
View Schema // Watch Tutorial Video // Download Examples 
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/letta-ai/agent-file/main/assets/agent-file-demo.gif" alt="Agent File Demo" width="700">
</p>

Agent File (.af) is an open standard file format for serializing stateful agents. Originally designed for the [Letta](https://letta.com) framework, Agent File provides a portable, standardized way to share agents with persistent memory and behavior.

Agent Files encapsulate all of the components of a stateful agent:
- Core memory blocks storing agent personality and user information
- Tool configurations for interacting with external systems
- Memory management settings and archival data connections
- LLM provider configurations and model parameters

By standardizing these components in a single file format, Agent File enables seamless transfer of agents between systems, promotes collaboration among developers, and simplifies deployment across environments.

## 👾 Download Example Agents

Browse our collection of ready-to-use agents.

To use one of the agents, simply download the agent file (`.af`) and upload it to Letta (instructions [here]()), or any other framework that supports agent files.

|        Agent Type            | Description | Download |
|------------------------------|------------|----------|
| 🧠 **MemGPT Agent**          | An agent with memory management tools for infinite context, as described in the MemGPT paper | [Download (empty)](https://letta-agent-files.s3.us-east-1.amazonaws.com/memgpt_agent.af) [Download (with pre-fill)](https://letta-agent-files.s3.us-east-1.amazonaws.com/memgpt_agent_with_convo.af) |
| 📚 **Deep Research Agent** | A research agent with planning, search, and memory tools to enable writing deep research reports from iterative research (requires [Tavily](https://tavily.com/) and [Firecrawl](https://www.firecrawl.dev/) keys)| [Download](https://letta-agent-files.s3.us-east-1.amazonaws.com/deep_research_agent.af) |
| 🛒 **Customer Support Agent** | A customer support agent that has dummy tools for handling order cancellations, looking up order status, and also memory | [Download](https://letta-agent-files.s3.us-east-1.amazonaws.com/customer_service.af) |
| ⚙️ **Stateless Workflow Agent** | A stateless graph workflow agent (no memory and deterministic tool calling) that evaluates recruting candidates and drafts emails | [Download](https://letta-agent-files.s3.us-east-1.amazonaws.com/outreach_workflow_agent.af) | 
| 🐙 **Composio Agent** | An example of an agent that uses a Composio tool to star a GitHub repository (requires enabling [Composio](https://composio.dev/)) | [Download](https://letta-agent-files.s3.us-east-1.amazonaws.com/composio_github_star_agent.af) |

## Using .af with Letta 

### Importing Agents 
You can load downloaded `.af` files into your ADE (running with Docker, Desktop, or Letta Cloud) to re-create the agent: 
![Importing Demo](./import_demo.gif)

### Exporting Agents 
You can export your own `.af` files to share (or contribute!) by selecting "Export Agent" in the ADE: 
![Exporting Demo](./export_demo.gif)

## FAQ

### Why Agent File?

The AI ecosystem is witnessing rapid growth in agent development, with each framework implementing its own storage mechanisms. Agent File addresses the need for a standard that enables:

- **Portability**: Move agents between systems or deploy them to new environments
- **Collaboration**: Share your agents with other developers and the community
- **Preservation**: Archive agent configurations to preserve your work
- **Versioning**: Track changes to agents over time through a standardized format

### What state does .af include?

An .af file contains all the state required to re-create the exact same agent:

| Component | Description |
|-----------|-------------|
| Model configuration | Context window limit, model name, embedding model name |
| Message history | Complete chat history with `in_context` field indicating if a message is in the current context window |
| System prompt | Initial instructions that define the agent's behavior |
| Memory blocks | In-context memory segments for personality, user info, etc. |
| Tool rules | Definitions of how tools should be sequenced or constrained |
| Environment variables | Configuration values for tool execution |
| Tools | Complete tool definitions including source code and JSON schema |

We currently do not support Passages (the units of Archival Memory), which have support for them on the roadmap.

You can view the entire schema of .af in the Letta repository [here](https://github.com/letta-ai/letta/blob/main/letta/serialize_schemas/pydantic_agent_schema.py).

### Does .af work with frameworks other than Letta?

Theoretically, other frameworks could also load in .af files if they convert the state into their own representations. Some concepts, such as context window "blocks" which can be edited or shared between agents, are not implemented in other frameworks, so may need to be adapted per-framework.

### How does .af handle secrets?

Agents have associated secrets for tool execution. When you export agents with secrets, the secrets are set to `null`.

## Roadmap 
- [ ] Agent connect to an MCP server
- [ ] Support archival memory passages
- [ ] Support data sources (i.e. files)
- [ ] Migration support between schema changes
- [ ] Multi-agent `.af` files
- [ ] Converters between frameworks 

---

<div align="center">

**[Documentation](https://docs.letta.com/agentfile)** • **[Community](https://discord.gg/letta)** • **[GitHub](https://github.com/letta-ai/letta)**

<small>Agent File is an open project under the Apache 2.0 license. © 2024 Letta Contributors</small>
</div>
