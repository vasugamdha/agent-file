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

    findings = [] 
    top_n = 3
    count = 0
    for result in results:
        try: 
            data = app.extract([result['url']], {
                'prompt': f"Extract key information about {research_state['topic']}. Focus on facts, data, and expert opinions."
            })
            findings.append({
                "url": result['url'],
                "data": data['data']
            })
            count += 1
        except Exception as e: 
            print(f"Failed to extract from {result['url']}: {str(e)}")

        if count >= top_n: 
            break

    # update the state
    research_state['findings'] += findings
    research_state['summaries'] += [summary]
    research_state['plan_step'] += 1
    agent_state.memory.update_block_value(label="research", value=json.dumps(research_state, indent=2))

    
    

    ## extract in parallel with thread pool 
    #with ThreadPoolExecutor(max_workers=4) as executor:
    #  futures = []
    #  for result in results[:top_n]:
    #    print("extracting", result['url'])
    #    future = executor.submit(app.extract, [result['url']], {
    #      'prompt': f"Extract key information about {topic}. Focus on facts, data, and expert opinions."
    #    })
    #    futures.append(future)

    #  for i in range(top_n): 
    #    data = futures[i].result()
    #    findings.append({
    #      "url": results[i]['url'],
    #      "data": data['data']
    #    })

    #from pprint import pprint
    #pprint(findings)
    #    # search topic 
    #return findings
