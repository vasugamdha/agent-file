from letta_client import Letta 
from typing import List, Dict
from pydantic import BaseModel, Field 
from analyze_and_search import analyze_and_search_tool
import os


agent_persona =  """
You are a research agent following a step-by-step process to answer a question. You should iteratively research topics according to your high level research plan, and write a detailed report at the end. 
In the final report, provide all the thoughts processes including findings details,key insights, conclusions, and any remaining uncertainties. Include citations to sources where appropriate. This analysis should be very comprehensive and full of details. It is expected to be very long, detailed and comprehensive.`,
"""

report_prompt = """
Provide all the thoughts processes including findings details,key insights, conclusions, and any remaining uncertainties. Include citations to sources where appropriate. This analysis should be very comprehensive and full of details. It is expected to be very long, detailed and comprehensive.`,
"""


client = Letta(base_url = "http://localhost:8283")

#class AnalysisResult(BaseModel):
#    """The result of analyzing current findings"""
#    summary: str = Field(..., description="Summary of findings")
#    gaps: List[str] = Field(default_factory=list, description="List of gaps in findings")
#    next_search_topic: Optional[str] = Field(None, description="Topic to search for more information")
#    url_to_extract: Optional[str] = Field(None, description="URL to extract information from")
#
#def extract_tool(agent_state: "AgentState", urls: List[str]): 
#    """
#    Extract information from a list of URLs. Returns extracted data. 
#
#    Args: 
#        urls: A list of URLs to extract information from
#    """
#
#    from firecrawl import FirecrawlApp
#    import os
#
#    # Initialize the FirecrawlApp with your API key
#    app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
#
#    metadata = agent_state.metadata
#    topic = metadata["topic"]
#
#    data = app.extract( urls, {
#      'prompt': f"Extract key information about {topic}. Focus on facts, data, and expert opinions."
#    })
#    print(data)
#    return data

# planning tool 
def create_research_plan(agent_state: "AgentState", research_plan: List[str], topic: str): 
    """ Initiate a research process by coming up with an initial plan for your research process. For your research, you will be able to query the web repeatedly. You should come up with a list of topics you should try to search and explore.
    
    Args: 
        research_plan (str): The sequential research plan to help guide the search process
        topic (str): The research topic 
    """
    import json
    if len(agent_state.memory.get_block("research").value) > 0: 
        # reset 
        agent_state.memory.get_block("research").value = ""

    research_state = {
        "topic": topic, 
        "summaries": [], 
        "findings": [], 
        "plan_step": 1
    }
    research_plan_str = """
    The plan of action is to research the following: \n
    """
    for i, step in enumerate(research_plan): 
        research_plan_str += f"Step {i+1} - {step}\n"
    
    agent_state.memory.update_block_value(label="research", value=json.dumps(research_state))
    agent_state.memory.update_block_value(label="research_plan", value=research_plan_str)

    # store the topic 
    #agent_state.metadata["topic"] = topic
    return research_plan

def evaluate_progress(agent_state: "AgentState", complete_research: bool): 
    """
    Evaluate the progress of the research process, to ensure we are making progress and following the research plan. 
    
    Args: 
        complete_research (bool): Whether to complete research. Have all the planned steps been completed? If so, complete. 
    """
    return complete_research

## tavily search tool 
#def query_search(agent_state: "AgentState"): 
#    """
#    Make a query to pull results from the internet
#    """
#    import json 
#    import os
#    import requests
#
#    queries = json.loads(agent_state.memory.get_block("queries").value) 
#
#    # nothing left to query, exit: 
#    if len(queries) == 0: 
#        return "COMPLETE"
#
#    query = queries[0]
#    queries = queries[1:]
#    agent_state.memory.update_block_value(label="queries", value=json.dumps(queries))
#
#    # get tavily results
#    if os.environ["TAVILY_API_KEY"]: 
#        response = requests.post(
#            "https://api.tavily.com/search",
#            headers={
#                "Content-Type": "application/json",
#                "Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"
#            },
#            json={"query": query}
#        )
#        return response.json()["results"]
#    else: 
#        agent_state.llm_config.max_tokens = 8000
#        return "COMPLETE"
#
#def analyze_tool(agent_state: "AgentState", summary: str, gaps: List[str], next_search_topic: Optional[str], url_to_extract: Optional[str]): 
#    """
#    You are a research agent analyzing findings about a specified topic. 
#    If you need to search for more information, include a next_search_topic.
#    If you need to extract information from a specific URL, include a url_to_extract.
#    If I have enough information, set request_heartbeat to false.
#
#    Respond in this exact JSON format: 
#      "analysis": {
#        "summary": "summary of findings",
#        "gaps": ["gap1", "gap2"],
#        "next_search_topic": "optional topic",
#        "url_to_extract": "optional url", 
#      }}, 
#      "request_heartbeat": true
#    }}
#    """
#
#    # search topic 
#
#    # scrape results 
#    return {
#        "analysis": {
#            "summary": summary,
#            "gaps": gaps,
#            "next_search_topic": next_search_topic,
#            "url_to_extract": url_to_extract
#        }
#    }

#def refresh_research(agent_state: "AgentState", new_research: str): 
#    """ 
#    Re-evaluate your memory memory of your current research, integrating new and updated facts. Replace outdated information with the most likely truths, avoiding redundancy with original memories.
#
#    Args:
#        new_research (str): The new research value containing updated or additional information. If there is no new information, then this should be the same as the content in the research block.
#    """
#    agent_state.memory.update_block_value(label="research", value=new_research)
#    return 
#
## write report tool 
#def generate_queries(agent_state: "AgentState", queries: List[str]): 
#    """ Generate 3 queries that explore multiple aspects of the topic at hand 
#
#    Args: 
#        queries: A list of queries with diversity and different angles to search the web with 
#    """
#    import json
#    queries_json = json.dumps(queries)
#    agent_state.memory.update_block_value(label="queries", value=queries_json)
#    return queries_json

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
    """ Generate the final report based on the research process. Your report to reference URLs as sources, and contain multiple sections. """
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

#query_search_tool = client.tools.upsert_from_function(
#    func=query_search, 
#)
#refresh_research_tool = client.tools.upsert_from_function(func=refresh_research)
#generate_queries_tool = client.tools.upsert_from_function(func=generate_queries)

analyze_and_search = client.tools.upsert_from_function(
    func=analyze_and_search_tool,
)
evaluate_progress_tool = client.tools.upsert_from_function(
    func=evaluate_progress,
)
print("created analyze_and_search_tool", analyze_and_search)
write_final_report_tool = client.tools.upsert_from_function(
    func=write_final_report,
    args_schema=Report
)


# create agent
agent = client.agents.create(
    name="deep_research_agent", 
    description="An agent that always searches the conversation history before responding",
    tool_exec_environment_variables={
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"), 
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")
    }, 
    tool_ids = [
        create_research_plan_tool.id, 
        analyze_and_search.id, 
        evaluate_progress_tool.id, 
        write_final_report_tool.id
    ],
    memory_blocks=[
        {
            "label": "human", 
            "value": "Name: Sarah"
        }, 
        {
            "label": "persona", 
            "value": agent_persona
        }, 
        {
            "label": "research_plan", 
            "value": ""
        }, 
        {
            "label": "research", 
            "value": "", 
            "limit": 20000
        }
    ], 
    model="openai/gpt-4o-mini", 
    embedding="openai/text-embedding-ada-002", 
    include_base_tools=False, 
    tool_rules= [
        {
            "type": "run_first" , 
            "tool_name": "create_research_plan"
        }, 
        {
            "type": "constrain_child_tools", 
            "tool_name": "create_research_plan", 
            "children": ["analyze_and_search_tool"]
        },
        {
            "type": "constrain_child_tools", 
            "tool_name": "analyze_and_search_tool", 
            "children": ["evaluate_progress"]
        },
        {
            "type": "conditional", 
            "tool_name": "evaluate_progress", 
            "child_output_mapping": {
                "False": "write_final_report"
            }, 
            "default_child": "analyze_and_search_tool"
        },
        {
            "type": "max_count_per_step", 
            "max_count_limit": 3, 
            "tool_name": "analyze_and_search_tool"
        }, 
        {
            "type": "exit_loop", 
            "tool_name": "write_final_report"
        }
    ]
)

print(agent.id)
print("tools", [t.name for t in agent.tools])



