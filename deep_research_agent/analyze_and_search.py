from typing import List, Optional

def analyze_and_search_tool(agent_state: "AgentState", summary: str, gaps: List[str], next_search_topic: str): 
    """
    You are a research agent analyzing findings about a specified topic. If you need to search for more information, include a next_search_topic. If you need to extract information from a specific URL, include a url_to_extract. If I have enough information, set request_heartbeat to false.

    Args: 
        summary (str): A summary of the findings
        gaps (List[str]): A list of gaps in the findings
        next_search_topic (str): A topic to search for more information
    """
    from firecrawl import FirecrawlApp
    import requests
    import json
    import os
    from concurrent.futures import ThreadPoolExecutor
    from typing import Dict, Any

    assert len(next_search_topic) > 0, "next_search_topic must be a non-empty string"

    query = next_search_topic

    # get tavily results
    response = requests.post(
        "https://api.tavily.com/search",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"
        },
        json={"query": query}
    )
    results = response.json()["results"]

    # Initialize the FirecrawlApp with your API key
    api_key = os.environ["FIRECRAWL_API_KEY"]
    app = FirecrawlApp(api_key=api_key)

    # Extract and gather findings
    current_findings = agent_state.memory.get_block("research").value
    research_state = json.loads(current_findings)
    
    top_n = 3
    urls_to_extract = [result['url'] for result in results[:top_n]]
    
    def extract_from_url(url: str) -> Dict[str, Any]:
        """Helper function to extract data from a single URL"""
        try:
            data = app.extract([url], {
                'prompt': f"Extract key information about {research_state['topic']}. Focus on facts, data, and expert opinions."
            })
            return {
                "url": url,
                "data": data['data']
            }
        except Exception as e:
            print(f"Failed to extract from {url}: {str(e)}")
            return None
    
    # Use ThreadPoolExecutor to make concurrent requests
    findings = []
    with ThreadPoolExecutor(max_workers=min(len(urls_to_extract), 5)) as executor:
        # Submit all extraction tasks
        future_to_url = {executor.submit(extract_from_url, url): url for url in urls_to_extract}
        
        # Collect results as they complete
        for future in future_to_url:
            result = future.result()
            if result:
                findings.append(result)
    
    # update the state
    research_state['findings'] += findings
    research_state['summaries'] += [summary]
    research_state['plan_step'] += 1
    agent_state.memory.update_block_value(label="research", value=json.dumps(research_state, indent=2))

#def analyze_and_search_tool(agent_state: "AgentState", summary: str, gaps: List[str], next_search_topic: str): 
#    """
#    You are a research agent analyzing findings about a specified topic. If you need to search for more information, include a next_search_topic. If you need to extract information from a specific URL, include a url_to_extract. If I have enough information, set request_heartbeat to false.
#
#    Args: 
#        summary (str): A summary of the findings
#        gaps (List[str]): A list of gaps in the findings
#        next_search_topic (str): A topic to search for more information
#    """
#    from firecrawl import FirecrawlApp
#    import requests
#    import json
#    import os
#    from concurrent.futures import ThreadPoolExecutor
#
#    assert len(next_search_topic) > 0, "next_search_topic must be a non-empty string"
#
#    query = next_search_topic
#
#    # get tavily results
#    response = requests.post(
#        "https://api.tavily.com/search",
#        headers={
#            "Content-Type": "application/json",
#            "Authorization": f"Bearer {os.environ['TAVILY_API_KEY']}"
#        },
#        json={"query": query}
#    )
#    results = response.json()["results"]
#
#
#    # Initialize the FirecrawlApp with your API key
#    api_key = os.environ["FIRECRAWL_API_KEY"]
#    app = FirecrawlApp(api_key=api_key)
#
#    # Extract and gather findings
#    current_findings = agent_state.memory.get_block("research").value
#    research_state = json.loads(current_findings)
#
#    findings = [] 
#    top_n = 3
#    count = 0
#    for result in results:
#        try: 
#            data = app.extract([result['url']], {
#                'prompt': f"Extract key information about {research_state['topic']}. Focus on facts, data, and expert opinions."
#            })
#            findings.append({
#                "url": result['url'],
#                "data": data['data']
#            })
#            count += 1
#        except Exception as e: 
#            print(f"Failed to extract from {result['url']}: {str(e)}")
#
#        if count >= top_n: 
#            break
#
#    # update the state
#    research_state['findings'] += findings
#    research_state['summaries'] += [summary]
#    research_state['plan_step'] += 1
#    agent_state.memory.update_block_value(label="research", value=json.dumps(research_state, indent=2))
#
#    
# 
#    #return findings
#
