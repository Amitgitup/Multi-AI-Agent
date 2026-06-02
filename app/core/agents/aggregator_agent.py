from langchain_core.messages import HumanMessage


def aggregate_responses(llm, responses):

    combined_text = "\n\n".join(responses)

    prompt = f"""
You are an AI aggregator.

Combine the following responses from different expert agents into one clear and structured final answer.

Responses:
{combined_text}
"""

    result = llm.invoke([
        HumanMessage(content = prompt)
    ])

    return result.content