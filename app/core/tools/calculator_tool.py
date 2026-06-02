from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Evaluate basic mathematical expressions.
    Example: 2 + 3 * 4
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"