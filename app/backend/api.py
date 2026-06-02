from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel 
from typing import List
import asyncio

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.core.llm_factory import get_llm
from app.core.orchestrator import orchestrate_query  

from app.core.memory_store import get_memory, update_memory
from langchain_core.messages import HumanMessage
from langchain_core.messages.ai import AIMessage


logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent System")


class RequestState(BaseModel):
    """
    Pydantic model for the request body.    
    """
    model_name: str
    system_prompt: str
    messages: List[str]  # Expects a list of message strings
    allow_search: bool
    session_id: str


async def stream_response(response_text: str):
    """
    Streams response token-by-token to frontend. 
    """
    words = response_text.split(" ")

    for word in words:
        yield word + " "
        await asyncio.sleep(0.02)       ## small delay for typing effect


@app.post("/chat")
async def chat_endpoint(request: RequestState):
    
    logger.info(f"Received request for model : {request.model_name}")

    ## Validate model
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Invalid model name received: {request.model_name}")
        raise HTTPException(status_code=400, detail="Invalid model name")

    # Validate message input
    if not request.messages:
        logger.warning("Received request with no messages")
        raise HTTPException(status_code=400, detail="No messages provided")

    try:
        
        ## Latest user message 
        latest_query = request.messages[-1]

        ## Create LLM instance
        llm = get_llm(request.model_name)

        memory = get_memory(request.session_id)

        ## add user message to memory
        update_memory(request.session_id, HumanMessage(content=latest_query))

        ## Run orchestrator
        response = await orchestrate_query(
            llm = llm,
            query = latest_query,
            history = memory
        )

        ## add AI response to memory
        update_memory(request.session_id, AIMessage(content = response))

        logger.info("Sucessfully generated response via orchestrator.")

        ## STREAM RESPONSE
        return StreamingResponse(
            stream_response(response),
            media_type = "text/plain"
        )

    except Exception as e:
        logger.error(f"Error occured during response generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(CustomException("Failed to get AI Response", error_detail=e))
            )

