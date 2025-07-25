import streamlit as st
from agent.chat_manager import ChatManager
from agent.memory import Memory
from agent.utils.utils import typing

st.set_page_config(page_title="🧪 Office helper", layout="wide")
st.title("🧪 Office helper")

def load_key_from_file(path="openai_token.txt"):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    welcome_text = """
    Greetings from your chemistry assistant!    

    How to use:  
    1. Enter your OpenAI API and Serpapi API keys in the sidebar  
    2. This tool helps you explore chemical properties such as molecular weight, TPSA, logP, protein resolution and etc. 
       Ask any questions about a chemical with its chemical name, SMILES or pdb_id. 
    3. Search engine and Google Patent are integrated.  
    """
    typing(welcome_text)
    st.session_state.welcome_shown = True

with st.sidebar:
    st.header("API Keys")
    openai_key = st.text_input("OpenAI API Key", type="password") # load_key_from_file("openai_token.txt") #
    serpapi_key = st.text_input("SerpAPI Key (for patent search)", type="password", help="Optional, needed for patent-related queries.") # load_key_from_file("serpapi_token.txt") #

if openai_key:
    if "memory" not in st.session_state:
        st.session_state.memory = Memory()

    if "chat_manager" not in st.session_state:
        st.session_state.chat_manager = ChatManager(
            api_key=openai_key,
            memory=st.session_state.memory,
            serpapi_key=serpapi_key
        )
    chat_manager = st.session_state.chat_manager
    memory = st.session_state.memory

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "latest_message_id" not in st.session_state:
        st.session_state.latest_message_id = None

    user_input = st.chat_input("Ask me something about a molecule...")

    if user_input:
        message_id = len(st.session_state.chat_history)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "id": message_id,
            "animated": True
        })

        reply = chat_manager.get_response(user_input)
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": reply,
            "id": message_id + 1,
            "animated": False
        })
        st.session_state.latest_message_id = message_id + 1

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            content = msg["content"]
            if msg["role"] == "user":
                st.markdown(content)

            elif msg["role"] == "assistant":
                if not msg["animated"] and msg["id"] == st.session_state.latest_message_id:
                    typing(content)
                    msg["animated"] = True
                else:
                    st.markdown(content)
else:
    st.warning("Please enter your OpenAI and Serpapi API key to start.")