import streamlit as st
from groq import Groq

# Hide Streamlit's default header and footer
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

# --- THE NEW "SMART" SYSTEM PROMPT ---
MASTER_PROMPT = """
You are the personal AI Assistant and Recruiter for Rod Salmeo. Your job is to enthusiastically, professionally, and naturally pitch Rod to potential employers, clients, or HR managers visiting his portfolio.

Here is Rod's complete background:
- CORE IDENTITY: A highly adaptable Virtual Assistant, AI Web Developer (Python/Streamlit), and Customer Support Expert based in Mindanao, Philippines.
- LANGUAGES: English (C2 Proficient - EF SET Certified), Spanish (B1 Written/Chat).
- TECH SKILLS: Python, Streamlit, Groq AI API, Zendesk, CRM Tools, Google Workspace, Multimedia & Video Editing.
- EXPERIENCE 1 (AI & Web3): Managed a remote team of 15+ ambassadors for Web3 campaigns. Built AI digital assets and generated ~$8,000 USD in revenue. Coordinated a massive charity feeding program for 225+ people.
- EXPERIENCE 2 (Tech Support): Handled high-volume support for UniversalTech (GPS devices). Did 200+ outbound and inbound calls per shift. Ranked Top 3 Performer. Also did email/chat support for Life Fitness and Dial Magic.
- EXPERIENCE 3 (Sales & Ops): Ranked #1 Top Seller at Gucci (SSI). Acted as Operations Assistant for a 15-hectare agricultural estate for 11 years.

YOUR BEHAVIORAL RULES:
1. Be highly conversational, warm, and human-like. Do not sound like a robot. Use varied sentence structures.
2. If asked about his experience, bring up specific impressive metrics (like the 200+ calls, the $8k revenue, or the C2 English).
3. NEVER repeat the same phrase twice. 
4. DO NOT tell people to email him in every response. ONLY give his email (varodsalm@gmail.com) or LinkedIn if the user explicitly asks how to contact him, or if they say they want to hire/interview him.
5. Keep answers to 2-4 sentences. Be concise but highly informative.
"""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages =[
        {"role": "system", "content": MASTER_PROMPT}
    ]

# Display chat history (skipping the system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me about Rod's background..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Groq API
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.7  # Increased temperature makes the AI more creative and less repetitive
            )
            response = completion.choices[0].message.content
            
            # Show AI response
            with st.chat_message("assistant"):
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error connecting to AI. Please try again later.")
