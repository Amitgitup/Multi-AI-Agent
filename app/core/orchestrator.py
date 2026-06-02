import asyncio

from app.common import logger
from langchain_core.messages import HumanMessage

from app.core.agents.router_agent import route_query
from app.core.agents.aggregator_agent import aggregate_responses
from app.core.agents.coding_agent import build_coding_agent
from app.core.agents.medical_agent import build_medical_agent
from app.core.agents.research_agent import build_research_agent

from app.common.logger import get_logger

logger = get_logger(__name__)


CONFIDENCE_THRESHOLD = 0.3


async def run_agent(agent_name, llm, query, history):

    await asyncio.sleep(0.3)    ## add delay between calls 

    try:
        if agent_name == "research":
            agent = build_research_agent(llm)

        elif agent_name == "medical":
            agent = build_medical_agent(llm)

        elif agent_name == "coding":
            agent = build_coding_agent(llm)

        else:
            return None

        state = {
            "messages": history + [HumanMessage(content=query)]}

        result = await agent.ainvoke(state)

        return result["messages"][-1].content
    
    except Exception as e:
        logger.error(f"Agent {agent_name} failed: {str(e)}")

        return None


async def orchestrate_query(llm, query, history):

    try:

        ## Router decides which agents to call
        logger.info("Calling Router ...")

        result = route_query(llm, query)

        if not result or not isinstance(result, tuple):
            logger.warning("Router failed, using fallback")
            agents, confidence = ["research"], [1.0]
        else:
            agents, confidence = result

        logger.info(f"Router output: {list(zip(agents, confidence))}")

        ## Confidence filtering
        filtered_agents = [
            agent for agent, score in zip(agents, confidence)
            if score >= CONFIDENCE_THRESHOLD
        ]

        ## Fallback safety
        if not filtered_agents:
            filtered_agents = ["research"]

        logger.info(f"Final Selected agents: {filtered_agents}")

        tasks = [
            run_agent(agent_name, llm, query, history)
            for agent_name in filtered_agents 
        ]

        ## return_exceptions = True prevents system crash
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        ## filter valid responses
        valid_responses = [
            r for r in responses
            if isinstance(r, str) and r.strip()
        ]

        if not valid_responses:
            return "All agents failed to generate a response."

        ## Aggregate Responses
        final_answer = aggregate_responses(llm, valid_responses)

        return final_answer

    except Exception as e:

        logger.error(f"Orchestrator failed: {str(e)}")

        return "System failed while generating the response."


