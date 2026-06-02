import os
import sys
import uuid
import requests
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

API_URL = "http://127.0.0.1:9999/chat"

st.set_page_config(page_title = "Multi AI Agent", layout = "centered")

st.title("Multi AI Agent System")


## Session Initialization 
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 


## Sidebar Controls
with st.sidebar:

    st.header("Agent Settings")

    system_prompt = st.text_area(
        "Define your AI Agent:", 
        height = 80
    )

    selected_model = st.selectbox(
        "Select Model",
        settings.ALLOWED_MODEL_NAMES
    )

    allow_web_search = st.checkbox("Allow web search")


## Display Chat History
for role, message in st.session_state.chat_history:

    with st.chat_message(role):
        st.markdown(message)


## Chat Input
user_query = st.chat_input("Ask Something...")

if user_query:

    st.session_state.chat_history.append(("user", user_query))

    with st.chat_message("user"):
        st.markdown("user")

    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_query],
        "allow_search": allow_web_search,
        "session_id": st.session_state.session_id
    }

    try:

        logger.info("Sending request to backend.")

        response = requests.post(
            API_URL,
            json = payload,
            stream = True,
            timeout = 300
        )

        full_response = ""

        with st.chat_message("assistant"):

            message_placeholder = st.empty()

            for chunk in response.iter_content(chunk_size = None):

                if chunk:

                    text = chunk.decode("utf-8")

                    full_response += text

                    message_placeholder.markdown(full_response)

        st.session_state.chat_history.append(("assistant", full_response))

        logger.info("Response received sucessfully.")


    except Exception as e:   

        logger.info(f"Frontend communication error: {str(e)}")

        st.error(
            str(
                CustomException(
                    f"Failed to communicate with backend: {str(e)}"
                )
            )
        )