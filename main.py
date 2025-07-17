import streamlit as st
from langchain_sql_chain import get_sql_database_chain


# Set page config for a cleaner look
st.set_page_config(
    page_title="SQL Chatbot",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for modern, minimal design
st.markdown("""
    <style>
    /* Style for text input and text area */
    .stTextInput > div > div > input, div[data-baseweb="textarea"] > div {
        background-color: #262730;
        color: #ffffff;
        border: 2px solid rgba(33, 150, 243, 0.1);
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        line-height: 1.5;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input:focus, div[data-baseweb="textarea"] > div:focus-within {
        border-color: #2196F3;
        box-shadow: 0 0 20px rgba(33, 150, 243, 0.2);
        outline: none;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder, div[data-baseweb="textarea"] textarea::placeholder {
        color: rgba(255, 255, 255, 0.5);
        font-style: italic;
    }
    
    /* Additional styling for text area specific elements */
    div[data-baseweb="textarea"] {
        background: transparent;
    }
    
    div[data-baseweb="textarea"] textarea {
        background-color: #262730 !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 0.5rem !important;
    }
    
    /* Style for the label */
    .stTextInput label, div[data-baseweb="textarea"] label {
        color: #89CFF0 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 0.5rem !important;
    }
        .stButton > button {
        background-color: #2196F3;
        color: #ffffff;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        border: 1px solid rgba(33, 150, 243, 0.2);
        font-size: 1rem;
        font-weight: 600;
        transition: background 0.3s ease, transform 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1976D2;
        transform: translateY(-1px);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    div.stMarkdown {
        padding: 1rem;
        border-radius: 4px;
    }
    .chat-message {
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
        background-color: #262730;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    .query {
        border-left: 4px solid #2196F3;
    }
    .response {
        border-left: 4px solid #4CAF50;
        background-color: #262730;
    }
    .query-label {
        font-size: 0.8rem;
        color: #89CFF0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .response-label {
        font-size: 0.8rem;
        color: #4fb053;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    .message-content {
        margin-top: 0.5rem;
        line-height: 1.5;
        color: #ffffff;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App title and description
st.title("SQL Query Assistant")
st.markdown("""
        Welcome to the SQL Query Assistant. This professional tool helps you query your database using natural language.
        Simply enter your question below, and the system will convert it into SQL and fetch the results for you.
    
""")

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Create a container for the chat interface
chat_container = st.container()

# Initialize the SQL chain
try:
    chain = get_sql_database_chain()
except Exception as e:
    st.error(f"Error initializing database connection: {str(e)}")
    st.info("Please make sure your environment variables (DATABASE_URL, GOOGLE_API_KEY) are properly set.")
    st.stop()

# Input field for user question - using text_input with dynamic key
user_input = st.text_area(
    "Ask a question about your data:",
    key=f"query_input_{len(st.session_state.chat_history)}",
    placeholder="Type your question here... (e.g., 'How many t-shirts are in stock?')",
    height=100
)

# Submit button
submit_button = st.button("Get Answer")

# Process the query when submitted
if submit_button and user_input.strip():
    with st.spinner('Generating response...'):
        try:
            # Get response from the chain
            response = chain.invoke({"query": user_input})
            
            # Add to chat history
            st.session_state.chat_history.append({"question": user_input, "answer": response['result']})
            
            # Force a rerun to show the new response and create new input field
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing your query: {str(e)}")

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
        # Query message
        st.markdown("""
            <div class="chat-message query">
                <div class="query-label">Query</div>
                <div class="message-content"><p style="margin: 0; padding: 0;">{}</p></div>
            </div>
        """.format(chat["question"]), unsafe_allow_html=True)
        
        # Response message
        st.markdown("""
            <div class="chat-message response">
                <div class="response-label">Response</div>
                <div class="message-content"><p style="margin: 0; padding: 0;">{}</p></div>
            </div>
        """.format(chat["answer"]), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer-container">
        <div class="footer-content">
            <span style='color: #E2E8F0; font-size: 0.85rem; opacity: 0.8;'>© 2025 SQL Query Assistant</span>
        </div>
    </div>
""", unsafe_allow_html=True)