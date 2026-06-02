from langgraph.prebuilt import create_react_agent

from app.core.tools.wikipedia_tool import get_wikipedia_tool
from app.core.tools.tavily_tool import get_tavily_tool
from app.core.tools.arxiv_tool import get_arxiv_tool


def build_research_agent(llm):

    tools = [
        get_tavily_tool(),
        get_wikipedia_tool(),
        get_arxiv_tool()
    ]

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = """ 
You are a research assistant.

Available tools:
- arxiv_search → ONLY for deep scientific/ML research queries
- tavily_search → for general web search
- wikipedia → for general knowledge

STRICT RULES:
- Use arxiv_search ONLY if query is about research papers, ML, AI, or academic topics
- For general queries, use tavily_search instead
- Do NOT overuse arxiv_search

CRITICAL TOOL USAGE INSTRUCTIONS:
- You must use native structural JSON tool calls. 
- NEVER output raw XML-like tool calls like <function=...>. 
- NEVER append arguments to the tool name. 
"""
    )

    return agent 
