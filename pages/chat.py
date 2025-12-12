import streamlit as st 
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])



st.title('Chat with your CPT-5.2')

if 'messages' not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])





prompt = st.chat_input('Ask me anything!')

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
       model="gpt-5.2",
       messages=st.session_state.messages 
     )

    reply = completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message('assistant'):
        st.markdown(reply)


# st.chat_message('user').markdown(prompt)


