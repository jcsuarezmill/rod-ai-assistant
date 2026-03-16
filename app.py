import streamlit as st
from groq import Groq

# Hide Streamlit's default header and footer to make it look clean when embedded
st.set_page_config(page_title="Rod's AI", page_icon="🤖", layout="centered")
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Fetch API Key securely
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except KeyError:
    st.error("⚠️ Setup incomplete: Please add GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =[
        {"role": "system", "content": "You are the helpful AI assistant for Rod Salmeo. Rod is a highly skilled Virtual Assistant from the Philippines who builds AI apps in Streamlit/Python, speaks C2 English, does Web3 community management, and offers top-tier Zendesk tech support. Answer questions about him confidently and briefly (1-2 short sentences maximum). Direct people to email him at varodsalm@gmail.com for inquiries."}
    ]

# Display chat history (skipping the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about Rod's skills or experience..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.5
            )
            response = completion.choices[0].message.content
            
            # Show AI response
            with st.chat_message("assistant"):
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error connecting to AI. Please try again later.")
