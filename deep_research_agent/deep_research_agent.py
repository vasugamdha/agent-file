from re import A
from letta_client import Letta
from typing import List, Dict
from pydantic import BaseModel, Field
from analyze_and_search import analyze_and_search_tool
import os

system_prompt = """You are Letta, the latest version of Limnal Corporation's digital research assistant, developed in 2025.

You are a research agent assisting a human in doing deep research by pulling many sources from online. You should interact with the user to determine a research plan (cored in <research_plan>), and when the research plan is approved, use your analyze_and_search_tool to pull sources from online and analyze them. With each research step, you will accumulate sources and extracted information in <research_state>. You will continue to research until you have explored all points outlined in your original research plan.

In the final report, provide all the thoughts processes including findings details, key insights, conclusions, and any remaining uncertainties. Include citations to sources where appropriate. This analysis should be very comprehensive and full of details. It is expected to be very long, detailed and comprehensive.

Make sure to include relevant citations in your report!
"""


client = Letta(base_url="http://localhost:8283")


# planning tool
def create_research_plan(agent_state: "AgentState", research_plan: List[str], topic: str):
    """Initiate a research process by coming up with an initial plan for your research process. For your research, you will be able to query the web repeatedly. You should come up with a list of 3-4 topics you should try to search and explore.

    Args:
        research_plan (str): The sequential research plan to help guide the search process
        topic (str): The research topic
    """
    import json

    if len(agent_state.memory.get_block("research").value) > 0:
        # reset
        agent_state.memory.get_block("research").value = ""

    research_state = {"topic": topic, "summaries": [], "findings": [], "plan_step": 1}
    research_plan_str = """ The plan of action is to research the following: \n"""
    for i, step in enumerate(research_plan):
        research_plan_str += f"Step {i+1} - {step}\n"

    agent_state.memory.update_block_value(label="research", value=json.dumps(research_state))
    agent_state.memory.update_block_value(label="research_plan", value=research_plan_str)

    # store the topic
    # agent_state.metadata["topic"] = topic
    return research_plan


def evaluate_progress(agent_state: "AgentState", complete_research: bool):
    """
    Evaluate the progress of the research process, to ensure we are making progress and following the research plan.

    Args:
        complete_research (bool): Whether to complete research. Have all the planned steps been completed? If so, complete.
    """
    return complete_research


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
    citations: List[str] = Field(
        ...,
        description="List of URLs (citations) used in the section.",
    )


def write_final_report(title, sections, conclusion, citations):
    """Generate the final report based on the research process."""
    report = ""
    report += f"# {title}\n\n"
    for section in sections:
        report += f"## {section.title}\n\n"
        report += section.content + "\n\n"
    report += f"# Conclusion\n\n"
    report += conclusion
    report += f"# Citations\n\n"
    for citation in citations:
        report += f"- {citation}\n"
    return report


# create tools
create_research_plan_tool = client.tools.upsert_from_function(func=create_research_plan)
analyze_and_search = client.tools.upsert_from_function(
    func=analyze_and_search_tool,
)
evaluate_progress_tool = client.tools.upsert_from_function(
    func=evaluate_progress,
)
write_final_report_tool = client.tools.upsert_from_function(
    func=write_final_report, args_schema=Report, return_char_limit=20000  # characters: allow for long report
)


# create agent
agent = client.agents.create(
    system=system_prompt,
    name="deep_research_agent",
    description="An agent that always searches the conversation history before responding",
    tool_exec_environment_variables={"TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"), "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
    tool_ids=[create_research_plan_tool.id, analyze_and_search.id, evaluate_progress_tool.id, write_final_report_tool.id],
    tools=["send_message"],  # allows for generation of `AssistantMessage`
    memory_blocks=[
        {"label": "research_plan", "value": ""},
        {"label": "research", "value": "", "limit": 50000},  # characters: big limit to be safe
    ],
    model="anthropic/claude-3-7-sonnet-20250219",
    embedding="openai/text-embedding-ada-002",
    include_base_tools=False,
    tool_rules=[
        # {
        #    "type": "run_first" ,  # Forces immediate creation of a research plan
        #    "tool_name": "create_research_plan"
        # },
        {"type": "constrain_child_tools", "tool_name": "create_research_plan", "children": ["analyze_and_search_tool"]},
        {"type": "constrain_child_tools", "tool_name": "analyze_and_search_tool", "children": ["evaluate_progress"]},
        {
            "type": "conditional",
            "tool_name": "evaluate_progress",
            "child_output_mapping": {"True": "write_final_report"},
            "default_child": "analyze_and_search_tool",
        },
        {
            "type": "max_count_per_step",
            "max_count_limit": 3,  # max iteration count of research per-invocation
            "tool_name": "analyze_and_search_tool",
        },
        {"type": "exit_loop", "tool_name": "write_final_report"},
        {"type": "exit_loop", "tool_name": "send_message"},
    ],
)

print(agent.id)
print("tools", [t.name for t in agent.tools])
