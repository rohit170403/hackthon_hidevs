import streamlit as st
from datetime import datetime
from legal import chatbot  # Your existing chatbot function

# Page configuration
st.set_page_config(
    page_title="Constitution Chatbot",
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS for attractive styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        margin-left: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        margin-right: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Suggested questions
SUGGESTED_QUESTIONS = [
    "What does Article 1(1) say?",
    "Which articles in the constitution define the judges of the Supreme Court in India?",
    "Who was Ms. Ammu Swaminathan in the Constituent Assembly?",
    "What is the 38th Amendment Act of the Constitution?"
]

# Main header
st.markdown("""
<div class="main-header">
    <h1>⚖️ Constitution Chatbot</h1>
    <p>Your AI-powered guide to constitutional knowledge</p>
</div>
""", unsafe_allow_html=True)

# Suggested questions section (only show if no messages)
if len(st.session_state.messages) == 0:
    st.markdown("### 💡 Click on a question to get started:")
    
    # Create columns for suggested questions
    cols = st.columns(2)
    for i, question in enumerate(SUGGESTED_QUESTIONS):
        with cols[i % 2]:
            if st.button(question, key=f"suggestion_{i}", use_container_width=True):
                # Add user message
                st.session_state.messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Get bot response immediately
                with st.spinner("🤖 Thinking..."):
                    try:
                        bot_response = chatbot(question)
                        
                        # Add bot message
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": bot_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                    except Exception as e:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "I apologize, but I encountered an error. Please try again.",
                            "timestamp": datetime.now().isoformat()
                        })
                
                st.rerun()

# Chat messages display
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>You:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong>🤖 Bot:</strong> {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything about the Constitution...")

# Handle user input
if user_input:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().isoformat()
    })
    
    # Get bot response
    with st.spinner("🤖 Thinking..."):
        try:
            bot_response = chatbot(user_input)
            
            # Add bot message
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_response,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "I apologize, but I encountered an error. Please try again.",
                "timestamp": datetime.now().isoformat()
            })
    
    st.rerun()