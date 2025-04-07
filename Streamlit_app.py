import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Set Streamlit page configuration
st.set_page_config(page_title="OpenAI Chatbot", layout="centered")

# Session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream response from OpenAI
        response_stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in response_stream:
            delta = chunk.choices[0].delta
            if delta.content:
                full_response += delta.content
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
