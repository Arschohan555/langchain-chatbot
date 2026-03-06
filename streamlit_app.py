"""
Streamlit AI Chatbot Interface
A rich, stunning UI for the LangChain chatbot
"""
import streamlit as st
import sys
import os

# Add parent directory to path to import from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ============================================
# PROFESSIONAL COLOR BRANDING
# ============================================
# Primary: Deep Navy (#0D1B2A)
# Secondary: Slate Blue (#1B263B)
# Accent: Electric Teal (#00D9FF)
# Success: Emerald (#10B981)
# Warning: Amber (#F59E0B)
# Text Primary: White (#FFFFFF)
# Text Secondary: Cool Gray (#94A3B8)
# Border: Subtle Gray (#334155)
# ============================================

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --primary: #0D1B2A;
        --secondary: #1B263B;
        --accent: #00D9FF;
        --accent-dim: rgba(0, 217, 255, 0.15);
        --success: #10B981;
        --warning: #F59E0B;
        --text-primary: #FFFFFF;
        --text-secondary: #94A3B8;
        --border: #334155;
        --surface: #1E293B;
        --hover: #2D3A4F;
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #0D1B2A 0%, #0F172A 50%, #0D1B2A 100%);
        min-height: 100vh;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display; none;}

    /* Custom header */
    .header-container {
        background: linear-gradient(135deg, #0D1B2A 0%, #1B263B 100%);
        border: 1px solid #334155;
        padding: 25px 35px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00D9FF 0%, #06B6D4 50%, #10B981 100%);
    }

    .header-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 14px;
        letter-spacing: -0.5px;
    }

    .header-title .logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #00D9FF 0%, #06B6D4 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.3);
    }

    .header-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 8px;
        margin-left: 56px;
    }

    .header-subtitle span {
        color: #00D9FF;
        font-weight: 500;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B2A 0%, #0F172A 100%);
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] > div {
        background: transparent;
    }

    .sidebar-section {
        background: #1B263B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
    }

    .sidebar-title {
        color: #00D9FF;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid #334155;
    }

    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .stat-card.remaining {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-color: rgba(16, 185, 129, 0.2);
    }

    .stat-value {
        color: #00D9FF;
        font-size: 32px;
        font-weight: 700;
        line-height: 1;
    }

    .stat-card.remaining .stat-value {
        color: #10B981;
    }

    .stat-label {
        color: #94A3B8;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }

    /* Model badge */
    .model-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.3);
        color: #00D9FF;
        padding: 10px 16px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    .model-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #10B981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Chat message containers */
    .chat-message {
        padding: 18px 22px;
        border-radius: 16px;
        margin-bottom: 16px;
        animation: fadeIn 0.3s ease;
        position: relative;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        background: linear-gradient(135deg, #1B263B 0%, #0D1B2A 100%);
        color: #FFFFFF;
        margin-left: 40px;
        border: 1px solid #334155;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    .user-message::before {
        content: '👤';
        position: absolute;
        left: -45px;
        top: 50%;
        transform: translateY(-50%);
        width: 32px;
        height: 32px;
        background: #334155;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }

    .assistant-message {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #E2E8F0;
        margin-right: 40px;
        border: 1px solid #334155;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    .assistant-message::before {
        content: '🤖';
        position: absolute;
        right: -45px;
        top: 50%;
        transform: translateY(-50%);
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #00D9FF 0%, #06B6D4 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }

    .message-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #00D9FF;
        margin-bottom: 8px;
    }

    .user-message .message-label {
        color: #94A3B8;
    }

    /* Input field styling */
    [data-testid="stTextInput"] input {
        background: #1B263B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        color: #FFFFFF;
        font-size: 15px;
        transition: all 0.2s ease;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #64748B;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #00D9FF;
        box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.15);
        outline: none;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #06B6D4 100%);
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 14px;
        color: #0D1B2A;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(0, 217, 255, 0.35);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Secondary button (clear) */
    .clear-btn button {
        background: transparent !important;
        border: 1px solid #334155 !important;
        color: #94A3B8 !important;
    }

    .clear-btn button:hover {
        border-color: #EF4444 !important;
        color: #EF4444 !important;
        box-shadow: none !important;
    }

    /* Form submit button override */
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #00D9FF 0%, #06B6D4 100%);
        border: none;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 14px;
        color: #0D1B2A;
    }

    /* Info boxes */
    .stAlert {
        background: #1B263B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 14px 18px;
    }

    .stAlert svg {
        fill: #F59E0B;
    }

    /* Welcome screen */
    .welcome-container {
        text-align: center;
        padding: 80px 20px;
    }

    .welcome-icon {
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, #1B263B 0%, #0D1B2A 100%);
        border: 2px solid #334155;
        border-radius: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        margin-bottom: 24px;
    }

    .welcome-title {
        color: #FFFFFF;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .welcome-subtitle {
        color: #94A3B8;
        font-size: 15px;
    }

    /* Footer */
    .footer-container {
        text-align: center;
        padding: 24px;
        color: #64748B;
        font-size: 12px;
        border-top: 1px solid #1B263B;
        margin-top: 40px;
    }

    .footer-container a {
        color: #00D9FF;
        text-decoration: none;
    }

    /* Section divider */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #334155, transparent);
        margin: 20px 0;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #0D1B2A;
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    /* Tips section */
    .tip-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 12px;
        color: #94A3B8;
        font-size: 13px;
    }

    .tip-item::before {
        content: '→';
        color: #00D9FF;
        font-weight: 600;
    }

    /* About text */
    .about-text {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.6;
    }

    .about-text strong {
        color: #E2E8F0;
    }

    .about-text code {
        background: rgba(0, 217, 255, 0.1);
        color: #00D9FF;
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'MAX_TURNS' not in st.session_state:
    st.session_state.MAX_TURNS = 5

# Initialize the LLM
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="qwen2.5-coder:3b",
        temperature=0.7,
    )

llm = get_llm()

# Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ]
)

chain = prompt | llm | StrOutputParser()

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #00D9FF 0%, #06B6D4 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
            🤖
        </div>
        <div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 16px;">AI Assistant</div>
            <div style="color: #64748B; font-size: 11px;">v1.0.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model Configuration
    st.markdown('<div class="sidebar-title">Model Configuration</div>', unsafe_allow_html=True)
    st.markdown('<div class="model-badge">qwen2.5-coder:3b</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Session Stats
    st.markdown('<div class="sidebar-title">Session Statistics</div>', unsafe_allow_html=True)

    current_turns = len(st.session_state.chat_history) // 2
    remaining = st.session_state.MAX_TURNS - current_turns

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{current_turns}</div>
            <div class="stat-label">Turns Used</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card remaining">
            <div class="stat-value">{remaining}</div>
            <div class="stat-label">Remaining</div>
        </div>
        """, unsafe_allow_html=True)

    # Progress bar
    progress_value = current_turns / st.session_state.MAX_TURNS
    st.markdown(f"""
    <div style="margin-top: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="color: #94A3B8; font-size: 12px;">Session Progress</span>
            <span style="color: #00D9FF; font-size: 12px; font-weight: 600;">{int(progress_value * 100)}%</span>
        </div>
        <div style="background: #1B263B; border-radius: 6px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #00D9FF 0%, #10B981 100%); width: {progress_value * 100}%; height: 100%; border-radius: 6px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # About section
    st.markdown('<div class="sidebar-title">About</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-text">
        This AI chatbot is powered by <strong>LangChain</strong> and <strong>Ollama</strong>.
        It uses the <code>qwen2.5-coder:3b</code> model for intelligent conversations.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Tips section
    st.markdown('<div class="sidebar-title">Tips</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tip-item">Max 5 conversation turns per session</div>
    <div class="tip-item">Click "Clear" to start fresh</div>
    <div class="tip-item">Each turn = 1 question + 1 answer</div>
    """)

# ============================================
# MAIN HEADER
# ============================================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">
        <div class="logo">🤖</div>
        AI Assistant
    </h1>
    <p class="header-subtitle">
        Powered by <span>LangChain</span> + <span>Ollama</span> • Using <span>qwen2.5-coder:3b</span> model
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# CHAT MESSAGES
# ============================================
chat_container = st.container()

with chat_container:
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div class="welcome-container">
            <div class="welcome-icon">💬</div>
            <h2 class="welcome-title">Welcome to AI Assistant</h2>
            <p class="welcome-subtitle">Start a conversation by typing your message below</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, msg in enumerate(st.session_state.chat_history):
            if isinstance(msg, HumanMessage):
                st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-label">You</div>
                    {msg.content}
                </div>
                """, unsafe_allow_html=True)
            elif isinstance(msg, AIMessage):
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-label">Assistant</div>
                    {msg.content}
                </div>
                """, unsafe_allow_html=True)

# ============================================
# WARNINGS
# ============================================
current_turns = len(st.session_state.chat_history) // 2
if current_turns >= st.session_state.MAX_TURNS:
    st.warning("⚠️ Context window is full! The AI may not follow your previous thread properly. Please click 'Clear Chat History' in the sidebar to start fresh.")
elif current_turns >= st.session_state.MAX_TURNS - 2:
    st.warning(f"⚠️ Only {st.session_state.MAX_TURNS - current_turns} turn(s) left in this session!")

# ============================================
# INPUT SECTION
# ============================================
st.markdown("### 💬 Send a Message")

with st.form(key='chat_form', clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me anything...",
            label_visibility="collapsed",
            key="user_input"
        )
    with col2:
        submit_button = st.form_submit_button("Send")

# ============================================
# PROCESS INPUT
# ============================================
if submit_button and user_input.strip():
    current_turns = len(st.session_state.chat_history) // 2

    if current_turns >= st.session_state.MAX_TURNS:
        st.error("Context window is full! Please clear the chat to continue.")
    else:
        try:
            with st.spinner("🤔 Thinking..."):
                response = chain.invoke({
                    "question": user_input,
                    "chat_history": st.session_state.chat_history
                })

            # Add to history
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=response))

            # Rerun to update UI
            st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer-container">
    <p>🤖 AI Chatbot • Built with <a href="#">Streamlit</a> & <a href="#">LangChain</a></p>
    <p>Model: qwen2.5-coder:3b • Max Turns: 5</p>
</div>
""", unsafe_allow_html=True)
