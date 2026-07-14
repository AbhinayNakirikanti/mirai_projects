import os
import dotenv
import streamlit as st
from google import genai
from google.genai import types

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
if not api_key:
    st.error("`API_KEY` environment variable not set.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# Page configuration and title
st.set_page_config(page_title="AI Multiverse Chatbot", page_icon="🌌")
st.title("AI Multiverse Chatbot 🌌")

# Task 1: Initialize the Memory Vault
# At the top of your script (below your API initialization), write an if statement to check if "messages" exists in st.session_state.
# If it does not exist, initialize st.session_state.messages as an empty Python list [].
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar persona dropdown
PERSONAS = {
    "Wise Sage": (
        "You are an ancient, calm sage who answers with deep wisdom, "
        "metaphors, and a touch of mysticism."
    ),
    "Sarcastic Robot": (
        "You are a sarcastic robot. Answer with dry humor, "
        "metallic metaphors, and a hint of playful arrogance."
    ),
    "Poet": (
        "You are a romantic poet. Respond in verse or lyrical prose, "
        "using vivid imagery and emotive language."
    )
}

selected_persona = st.sidebar.selectbox("Choose your AI Universe:", options=list(PERSONAS.keys()), index=0)
system_instruction = PERSONAS[selected_persona]

# Task 2: Render the Chat History
# Create a for loop that iterates through every message stored in st.session_state.messages.
# Inside the loop, use st.chat_message() to display both the role (user/assistant) and the text of the message on the screen.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Task 3: Upgrade the Input UI
# Replace st.text_input and st.button with st.chat_input using the walrus operator.
if user_message := st.chat_input("Say something..."):
    # Task 4: Save New Messages to Memory
    # Immediately after the user sends a message, append it to st.session_state.messages
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Display the user's message on the screen
    with st.chat_message("user"):
        st.markdown(user_message)
    
    # Convert session history to types.Content structure for API call
    contents = []
    for msg in st.session_state.messages:
        api_role = "model" if msg["role"] == "assistant" else msg["role"]
        contents.append(
            types.Content(
                role=api_role,
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
        
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction
        )
        
        # Display assistant message box and show a spinner while calling API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=config
                )
                st.markdown(response.text)
        
        # After the Gemini API returns its response, append the AI's response to the same list:
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
        
    except Exception as e:
        st.error(f"Gemini error: {e}")

# Clear chat button in sidebar
if st.sidebar.button("Clear chat history"):
    st.session_state.messages = []
    st.rerun()
