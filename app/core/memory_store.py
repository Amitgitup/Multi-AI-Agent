## Later we can replace this with Redis or any External Database

from langchain_core.messages import HumanMessage, AIMessage

# Simple in-memory storage
memory_store = {}


def get_memory(session_id: str):
    """
    Retrieve conversation history for a session.
    """
    if session_id not in memory_store:
        memory_store[session_id] = []

    return memory_store[session_id]


def update_memory(session_id: str, message):
    """
    Append a message to conversation history.
    """
    if session_id not in memory_store:
        memory_store[session_id] = []

    memory_store[session_id].append(message)


def clear_message(session_id: str):
    """
    Reset conversation memory for a session.
    """
    memory_store[session_id] = []