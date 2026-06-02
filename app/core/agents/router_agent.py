import json
from langchain_core.messages import HumanMessage


def route_query(llm, query):

    prompt = f"""
You are an intelligent routing agent.

Your job is to decide:
1. Which agents should handle the query
2. Confidence Score (0 to 1) for each agent

Available agents:
- research
- medical
- coding

Return strict json format:

{{
    "agents": ["research", "medical"],
    "confidence": [0.8, 0.6]
}}

Rules:
- Confidence must be between 0 and 1
- If unsure, give lower confidence
- Never return empty agents list

Query:
{query}
"""

    response = llm.invoke([
        HumanMessage(content = prompt)
    ])

    try:
        data = json.loads(response.content)

        agents = data.get("agents", [])
        confidence = data.get("confidence", [])

        if not agents or not isinstance(agents, list):
            return ["research"], [1.0]

        if len(agents) != len(confidence):
            confidence = [0.7] * len(agents)

        return agents, confidence

    except Exception as e:
        return ["research"], [1.0]