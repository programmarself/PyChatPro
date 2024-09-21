import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load ignore keywords from a file
ignore_keywords = []
with open('ignore_keywords.txt', 'r') as file:
    ignore_keywords = [line.strip().lower() for line in file]


# Configure API Key
api_key = os.getenv("Gemini_API_Key")
if api_key is None:
    st.error("API key not found. Please set the environment variable 'Gemini_API_Key'.")
    st.stop()

genai.configure(api_key=api_key)

# Set title
st.title("PyChatPro")

# Model Initiation
model = genai.GenerativeModel('gemini-1.5-flash')

# Define a method to get a response from the model
def getResponseFromModel(user_input):
    try:
        greetings = ["hello", "hi", "hey", "aslam u alaikum", "wa alaikum salam", "salam", "goodbye", "bye"]
        if any(greet in user_input.lower() for greet in greetings):
            if "bye" in user_input.lower() or "goodbye" in user_input.lower():
                return "Goodbye! Have a nice day!"
            elif "aslam u alaikum" in user_input.lower() or 'salam' in user_input.lower():
                return "Wa Alaikum Assalam! How can I assist you with Python programming today?"
            else:
                return "Hello! How can I assist you with Python programming today?"

        # Check if input contains any ignore keywords
        elif any(keyword in user_input.lower() for keyword in ignore_keywords):
            return "I only assist with Python programming questions. Please ask about Python-related topics."

        else:
            response = model.generate_content(f"""
    You are PyChatPro, an AI chatbot that assists users with Python programming.
    - Provide responses that are concise and to the point.
    - Avoid unnecessary details; keep explanations between 3-5 lines.
    - If the user needs help with Python code, offer clear, necessary guidance.
    - Do not answer questions unrelated to Python programming.
    - Do not answer any question which is not related to python.
    - If the user's input includes greetings or farewells, respond politely and end the conversation if necessary.
    - User input: {user_input}
""")

            if response and hasattr(response, 'text'):
                return response.text
            else:
                return "Sorry, I couldn't generate a valid response. Please try rephrasing your question."
        
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Initialize session state if not already done
if "history" not in st.session_state:
    st.session_state.history = []

# Custom CSS for message styling
st.markdown("""
    <style>
    .user-message {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        display: inline-block;
        max-width: 80%;
        text-align: right;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #e0e0e0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        display: inline-block;
        max-width: 80%;
        text-align: left;
        float: left;
        clear: both;
    }
    .stCodeBlock {
        background-color: #000000 !important;
        color: #ffffff !important;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        max-height: 400px;
        overflow-y: auto;
        font-family: "Courier New", Courier, monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Form for user input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your Python programming question:", max_chars=2000)
    
    # Create two columns for buttons (side by side)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        submit_button = st.form_submit_button("Generate")
    
    with col2:
        clear_button = st.form_submit_button("Clear Conversation")

    if submit_button and user_input:
        # Add user input to history
        st.session_state.history.insert(0, ("user", user_input))
        
        # Get model response
        output = getResponseFromModel(user_input)
        if output:
            # Add model response to history
            st.session_state.history.insert(0, ("bot", output))

    # Clear conversation history when clear button is clicked
    if clear_button:
        st.session_state.history = []

# Display conversation history (newest first)
for entry in reversed(st.session_state.history):
    role, message = entry
    if role == "user":
        st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
    else:
        if "```" in message:  # Check if the message contains code
            parts = message.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd index means this is a code block
                    st.code(part.strip(), language="python")
                else:
                    st.markdown(f'<div class="bot-message">{part}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message}</div>', unsafe_allow_html=True)
