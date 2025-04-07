import streamlit as st
import openai
import time
from openai import OpenAIError, RateLimitError

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]  # or use a hardcoded string for testing

st.set_page_config(page_title="OpenAI ChatBot", layout="centered")
st.title("🤖 OpenAI ChatBot")

# Input prompt
user_input = st.text_input("Enter your message:")

# Display response
if user_input:
    try:
        with st.spinner("Thinking..."):
            response_stream = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}],
                stream=True,
            )

            # Stream the response
            response_text = ""
            for chunk in response_stream:
                if "choices" in chunk and chunk["choices"][0]["delta"].get("content"):
                    content = chunk["choices"][0]["delta"]["content"]
                    response_text += content
                    st.markdown(response_text)

    except RateLimitError:
        st.error("⚠️ Rate limit reached. Please wait a bit and try again.")
        time.sleep(10)
    except OpenAIError as e:
        st.error(f"🚨 OpenAI error: {str(e)}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
