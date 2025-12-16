import streamlit as st
from openai import OpenAI

# Import dashboard pages
from pages import Cyber_Incident, It_Ticket, Meta_Data

# Setup OpenAI
client = OpenAI(api_key=st.secrets["openai_api_key"])

# App title
st.title("Chat with your AI Assistant")

# Page setup
st.set_page_config(page_title='Chart', page_icon='🤖', layout='wide')

# Check login status
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # Set to False by default

# Block access if not logged in
if not st.session_state['logged_in']:
    st.warning('login to Access')
    st.stop()  # Stop here if not logged in

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# User input
user_input = st.chat_input("Ask me anything!")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant for this app. Explain dashboards, charts, and metrics. For exact numbers, direct to the dashboards."
            },
            *st.session_state.messages
        ]
    )
    
    # Get reply
    ai_reply = response.choices[0].message.content
    
    # Add to history and show
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
    st.chat_message("assistant").markdown(ai_reply)
