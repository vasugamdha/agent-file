# Agent File (.af): A shareable file format for stateful agents 

### What is “Agent File” (.af)? 
Agents files are a file representation of the state of an agent. A fundamental difference between agents and LLMs is that agents are stateful - they have associated message histories, stored memories, and access to specific tools and data sources. Agent files provide a way to represent this state, so that agents can be exported and shared.  

With agent files, you can move agents between different Letta servers, and also between Letta Desktop and Letta Cloud. You can also share agent files with other people so they can recreate your agents with the exact same state and configuration! 

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
