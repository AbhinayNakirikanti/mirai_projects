import os
import dotenv
import streamlit as st
import google.generativeai as genai


dotenv.load_dotenv()
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("\`API_KEY\` environment variable not set.")
    st.stop()

genai.configure(api_key=api_key)
st.title("AI Multiverse")

PERSONAS = {
    "Wise Sage" : (
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
    ),
}

selected_persona = st.selectbox("Choose your AI Universe:", options=list(PERSONAS.keys()), index=0)

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}

if selected_persona not in st.session_state.chat_histories:
    st.session_state.chat_histories[selected_persona] = []

for msg in st.session_state.chat_histories[selected_persona]:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Say something to your AI..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_histories[selected_persona].append(
        {
            "role" : "user",
            "content" : prompt,
        }
    )

    system_instruction = PERSONAS[selected_persona]

    history_text = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.chat_histories[selected_persona]
    )
    full_prompt = f"{system_instruction}\n\nConversation so far:\n{history_text}\n\nAssistant:"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(full_prompt, stream=True)
        answer_placeholder = st.empty()
        full_answer = ""
        for chunk in response:
            if chunk.text:
                full_answer += chunk.text
                answer_placeholder.markdown(full_answer)
        
        st.session_state.chat_histories[selected_persona].append(
            {"role": "assistant", "content": full_answer}
        )
    except Exception as e:
        st.error(f"Gemini error: {e}")

if st.button("Clear chat"):
    st.session_state.chat_histories[selected_persona] = []
    st.rerun()