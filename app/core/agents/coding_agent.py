from langgraph.prebuilt import create_react_agent

from app.core.tools.python_tool import get_python_tool
from app.core.tools.calculator_tool import calculator


def build_coding_agent(llm):

    tools = [
        get_python_tool(),
        calculator
    ]

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = """ 
You are a senior software engineer.

Use:
- Python tool for computation and debugging
- Calculator for simple math

You help users write, debug and optimize code.
"""
    )

    return agent 
