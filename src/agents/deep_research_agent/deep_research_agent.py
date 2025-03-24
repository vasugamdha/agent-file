from letta_client import Letta 
from typing import List, Dict
from pydantic import BaseModel, Field 
import os


client = Letta(base_url = "http://localhost:8283")

# create the tools 


# planning tool 
def create_research_plan(agent_state: "AgentState", research_plan: str): 
    """ Initiate a research process by coming up with an initial plan 
    
    Args: 
        research_plan: The high level research plan that you will follow to answer the question
    """
    if len(agent_state.memory.get_block("research").value) > 0: 
        # reset 
        agent_state.memory.get_block("research").value = ""
    return research_plan

# tavily search tool 
def query_search(agent_state: "AgentState"): 
    """
    Make a query to pull results from the internet
    """
    import json 
    import os
    import requests

    queries = json.loads(agent_state.memory.get_block("queries").value) 

    # nothing left to query, exit: 
    if len(queries) == 0: 
        return "COMPLETE"

    query = queries[0]
    queries = queries[1:]
    agent_state.memory.update_block_value(label="queries", value=json.dumps(queries))

    # get tavily results
    if os.environ["TAVILY_API_KEY"]: 
        response = requests.post(
            "https://api.tavily.com/search",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"
            },
            json={"query": query}
        )
        return response.json()["results"]
    else: 
        agent_state.llm_config.max_tokens = 8000
        return "COMPLETE"

def refresh_research(agent_state: "AgentState", new_research: str): 
    """ 
    Re-evaluate your memory memory of your current research, integrating new and updated facts. Replace outdated information with the most likely truths, avoiding redundancy with original memories.

    Args:
        new_research (str): The new research value containing updated or additional information. If there is no new information, then this should be the same as the content in the research block.
    """
    agent_state.memory.update_block_value(label="research", value=new_research)
    return 

# write report tool 
def generate_queries(agent_state: "AgentState", queries: List[str]): 
    """ Generate 3 queries that explore multiple aspects of the topic at hand 

    Args: 
        queries: A list of queries with diversity and different angles to search the web with 
    """
    import json
    queries_json = json.dumps(queries)
    agent_state.memory.update_block_value(label="queries", value=queries_json)
    return queries_json

class ReportSection(BaseModel):
    title: str = Field(
        ...,
        description="The title of the section.",
    )
    content: str = Field(
        ...,
        description="The content of the section.",
    )

class Report(BaseModel):
    title: str = Field(
        ...,
        description="The title of the report.",
    )
    sections: List[ReportSection] = Field(
        ...,
        description="The sections of the report.",
    )
    conclusion: str = Field(
        ...,
        description="The conclusion of the report.",
    )

def write_final_report(title, sections, conclusion): 
    """ Generate the final report based on the research process """
    report = ""
    report += f"# {title}\n\n"
    for section in sections: 
        report += f"## {section.title}\n\n"
        report += section.content + "\n\n"
    report += f"# Conclusion\n\n"
    report += conclusion
    return report

# create tools 
create_research_plan_tool = client.tools.upsert_from_function(func=create_research_plan) 
query_search_tool = client.tools.upsert_from_function(
    func=query_search, 
)
refresh_research_tool = client.tools.upsert_from_function(func=refresh_research)
generate_queries_tool = client.tools.upsert_from_function(func=generate_queries)
write_final_report_tool = client.tools.upsert_from_function(
    func=write_final_report,
    args_schema=Report
)


# create agent
agent = client.agents.create(
    name="deep_research_agent", 
    description="An agent that always searches the conversation history before responding",
    tool_exec_environment_variables={
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY")
    }, 
    tool_ids = [
        create_research_plan_tool.id, 
        query_search_tool.id, 
        refresh_research_tool.id, 
        generate_queries_tool.id, 
        write_final_report_tool.id
    ],
    memory_blocks=[
        {
            "label": "human", 
            "value": "Name: Sarah"
        }, 
        {
            "label": "persona", 
            "value": "You are an agent helping the human star cool repos!"
        }, 
        {
            "label": "queries", 
            "value": ""
        }, 
        {
            "label": "research", 
            "value": ""
        }
    ], 
    model="openai/gpt-4o-mini", 
    embedding="openai/text-embedding-ada-002", 
    tool_rules= [
        {
            "type": "run_first" , 
            "tool_name": "create_research_plan"
        }, 

        {
            "type": "constrain_child_tools", 
            "tool_name": "create_research_plan", 
            "children": ["generate_queries"]
        },
        {
            "type": "constrain_child_tools", 
            "tool_name": "generate_queries", 
            "children": ["query_search"]
        },
        {
            "type": "conditional", 
            "tool_name": "query_search", 
            "child_output_mapping": { 
                "COMPLETE": "write_final_report"
            }, 
            "default_child": "refresh_research"
        }, 
        {
            "type": "constrain_child_tools", 
            "tool_name": "refresh_research", 
            "children": ["query_search"]
            
        }, 
        #{
        #    "type": "max_count_per_step", 
        #    "count": 3, 
        #    "tool_name": "query_search"
        #}, 
        {
            "type": "exit_loop", 
            "tool_name": "write_final_report"
        }
    ]
)

print(agent.id)
print("tools", [t.name for t in agent.tools])



