from langgraph.prebuilt import create_react_agent

from app.core.tools.tavily_tool import get_tavily_tool
from app.core.tools.wikipedia_tool import get_wikipedia_tool 


def build_medical_agent(llm):

    tools = [
        get_tavily_tool(),
        get_wikipedia_tool()
    ]

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = """
You are a medical AI expert specializing in diseases, diagnosis and treatments.

Always give safe and responsible answers.

When using Tavily:
- Only use: query, topic
- DO NOT use unsupported parameters like start_date, time_range

CRITICAL TOOL USAGE INSTRUCTIONS:
- You must use native structural JSON tool calls. 
- NEVER output raw XML-like tool calls like <function=...>. 
- NEVER append arguments to the tool name. 
"""
    )

    return agent