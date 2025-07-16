import streamlit as st
from database_test import get_sql_database_chain
import os

# Set page config for a cleaner look
st.set_page_config(
    page_title="SQL Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for modern, minimal design
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    div.stMarkdown {
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("SQL Query Assistant 🤖")
st.markdown("""
    Welcome to the SQL Query Assistant! This chatbot helps you query your database using natural language.
    Simply type your question, and I'll convert it into SQL and fetch the results for you.
""")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Create a container for the chat interface
chat_container = st.container()

# Input field for user question
with st.form(key='query_form'):
    user_input = st.text_area("Ask a question about your data:", height=100)
    submit_button = st.form_submit_button("Get Answer")

# Initialize the SQL chain
try:
    chain = get_sql_database_chain()
except Exception as e:
    st.error(f"Error initializing database connection: {str(e)}")
    st.info("Please make sure your environment variables (DATABASE_URL, GOOGLE_API_KEY) are properly set.")
    st.stop()

# Process the query when submitted
if submit_button and user_input:
    with st.spinner('Generating response...'):
        try:
            # Get response from the chain
            response = chain.invoke({"query": user_input})
            
            # Add to chat history
            st.session_state.chat_history.append({"question": user_input, "answer": response['result']})
            
        except Exception as e:
            st.error(f"Error processing your query: {str(e)}")

# Display chat history
with chat_container:
    for chat in reversed(st.session_state.chat_history):
        st.markdown("### 🤔 Question")
        st.markdown(chat["question"])
        st.markdown("### 💡 Answer")
        st.markdown(chat["answer"])
        st.markdown("---")

# Custom CSS for the footer
st.markdown("""
    <style>
        footer {display: none !important;}
        .footer-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: rgb(38,39,47);
            z-index: 999;
            padding: 0.8rem;
        }
        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0.5rem;
        }
        .main-container {
            margin-bottom: 80px;
        }
    </style>
""", unsafe_allow_html=True)

# Wrap the main content
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Display chat history
with chat_container:
    for chat in reversed(st.session_state.chat_history):
        st.markdown("### 🤔 Question")
        st.markdown(chat["question"])
        st.markdown("### 💡 Answer")
        st.markdown(chat["answer"])
        st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-container">
        <div class="footer-content">
            <span style='color: #E2E8F0; font-size: 0.85rem; opacity: 0.8;'>© 2025 SQL Query Assistant</span>
        </div>
    </div>
""", unsafe_allow_html=True)
