# Deep Research Agent 
> ⚠️ **Warning:** You will need a `TAVILITY_API_KEY` and `FIRECRAWL_API_KEY` to run this agent. 

This is an agent inspired by OpenAI's [Deep Research Agent](https://github.com/openai/deep-research-agent). The agent has a set of tools for performing deep research: 

- `create_research_plan`: Create a research plan for a given topic. 
- `analyze_and_search`: Analyze the current findings and search for more information (uses Tavily for search and FireCrawl for extracting information from web pages)
- `evaluate_progress`: Evaluate the progress of the research process, to determine if `analyze_and_search` should be called again. 
- `write_final_report`: Write a final report based on the final research state

The deep research agent also uses core memory blocks to maintain the research *state*. This allows the agent to accumulate state between calls to `analyze_and_search` and `evaluate_progress`, and also to remember the research plan. The agent therefore has the following core memory blocks: 

- `research_plan`: The research plan for the current topic
- `research`: The current state of the research process (updated by `analyze_and_search`)
- `human`: The name of the human (in this case, Sarah)
- `persona`: The persona of the agent 

Although it is possible to have the agent be fully autonomous and always choose what tools to call when, we can improve reliability by also adding tool rules to constrain the agent's behavior. We add tool rules to enforce that: 
- `create_research_plan` is run first
- `analyze_and_search` is run after `create_research_plan`
- `evaluate_progress` is run after `analyze_and_search`
- `analyze_and_search` is run a maximum of 3 times
- if `evaluate_progress` returns `True`, `write_final_report` is called, otherwise `analyze_and_search` is called again
- the agent terminates after calling `write_final_report`

