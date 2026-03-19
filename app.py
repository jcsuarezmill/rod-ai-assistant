import streamlit as st
import smtplib
from email.mime.text import MIMEText
from groq import Groq

# PAGE SETUP
st.set_page_config(page_title="Rod's AI Assistant", page_icon="🤖")

# API CONFIG
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# EMAIL FUNCTION
def send_chat_to_email():
    try:
        sender_email = st.secrets["EMAIL_ADDRESS"]
        sender_password = st.secrets["GMAIL_APP_PASSWORD"] 
        receiver_email = "varodsalm@gmail.com"
        
        chat_log = "Chat Transcript:\n\n"
        for msg in st.session_state.messages:
            chat_log += f"{msg['role'].upper()}: {msg['content']}\n\n"
            
        msg = MIMEText(chat_log)
        msg['Subject'] = "New Portfolio Lead"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except: return False

# LOAD KB
with open("knowledge_base.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm Rod's assistant. How can I help you today?"}]

# SIDEBAR
with st.sidebar:
    if st.button("📩 Send Chat to Rod's Email"):
        if send_chat_to_email(): st.success("Sent!")
        else: st.error("Error sending.")

# CHAT UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask me about Rod..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            temperature=0.5
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
