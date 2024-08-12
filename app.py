import streamlit as st
from utils import DisabilityFormAssistant
import os
from dotenv import load_dotenv

# Set page config at the very beginning
st.set_page_config(page_title="Disability Form Assistant", page_icon="📝")

# Load environment variables
load_dotenv()

# Initialize the DisabilityFormAssistant
@st.cache_resource
def get_assistant():
    api_key = os.getenv("OPENAI_API_KEY")
    return DisabilityFormAssistant(api_key=api_key)

# Initialize session state
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_rating' not in st.session_state:
        st.session_state.user_rating = None
    if 'dialogue' not in st.session_state:
        st.session_state.dialogue = ""

# Main function
def main():
    assistant = get_assistant()

    st.title("Adult Disability Payment Form Assistant")

    # Initialize session state
    init_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the Adult Disability Payment form"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.dialogue += f"User: {prompt}\n"
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            response, response_time = assistant.get_response(prompt)
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.dialogue += f"Assistant: {response}\n"
            st.session_state.dialogue += f"Response time: {response_time:.2f} seconds\n\n"
            st.caption(f"Response time: {response_time:.2f} seconds")

    # User rating
    if st.button("End Conversation and Rate"):
        st.session_state.user_rating = st.slider(
            "Please rate your experience",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="1 = Poor, 5 = Excellent"
        )
        st.session_state.dialogue += f"User rating: {st.session_state.user_rating}/5\n"

        assistant.save_dialogue(st.session_state.dialogue)
        st.success("Conversation saved successfully!")

    # Sidebar with additional information
    st.sidebar.title("About")
    st.sidebar.info(
        "This AI assistant is designed to help you with questions about the "
        "Adult Disability Payment form. Feel free to ask any questions you have "
        "about the application process, eligibility, or specific sections of the form."
    )

    st.sidebar.title("Tips")
    st.sidebar.markdown(
        """
        - Be specific in your questions
        - You can ask about multiple topics
        - If you're unsure, ask for clarification
        - Remember to rate your experience after the conversation
        """
    )

if __name__ == "__main__":
    main()
