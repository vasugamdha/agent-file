# Workflow (or Graph) Agent
Letta agents are by default designed to be stateful and have advanced memory capabilities. However, you can still use Letta to design agentic workflows that combined LLMs and tool execution in deterministic ways. To do this, we can configure the agent to disable the memory functionality to essentially create a *stateless* workflow agent. 

## Configuration
The workflow agent is configured to:
* Have no memory blocks
* Clear the in-context messages on every agent invocation
* Have no default tools

## Workflow Graph 
We can define the workflow graph by using tool rules on the tools. The agent in this example is a email drafting workflow for recruiting candidates that has the following tools:
- `retrieve_candidate`: Retrieve a candidate based on their name
- `evaluate_candidate`: Evaluate a candidate based on their name
- `send_email`: Send an email to a candidate
- `reject`: Reject a candidate
We can define the rules for the workflow graph by specifying tool rules, which define the order in which tools are executed and the conditions under which a tool is called. For this agent, we define the following tool rules:
- `retrieve_candidate` is run first
- `evaluate_candidate` is run after `retrieve_candidate`
- if `evaluate_candidate` returns `True`, `send_email` is called, otherwise `reject` is called
- The agent terminates after calling `reject` or `send_email`



