import streamlit as st
from api_service import chat, upload_pdf, file_chat

# Set page configuration
st.set_page_config(page_title="RAG Chat", page_icon="💬", layout="wide")



st.title("💬 RAG Chatbot")

# Sidebar for file upload
st.sidebar.header("Upload your file")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "txt", "docx"])

if uploaded_file:
    upload_pdf(uploaded_file)
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")
    # You can process the file later using your API
    # For now, we just show the file name

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

def add_user_message():
    if st.session_state.user_input:
        print("User input:", st.session_state.user_input)
        print("From file:", st.session_state.from_file)
        if st.session_state.from_file:
            res = file_chat(st.session_state.user_input, st.session_state.messages)
        else:
            res = chat(st.session_state.user_input, st.session_state.messages)

        st.session_state.messages.append({"prompt": st.session_state.user_input, "response": res})
        st.session_state.user_input = ""  # Clear input


# User input
st.checkbox("Answer from uploaded file", key="from_file", value=False)
st.text_input("Type your message:", key="user_input", on_change=add_user_message)

# Display chat messages
for msg in st.session_state.messages:
    st.markdown(f"**You:** {msg['prompt']}")
    st.markdown(f"**Bot:** {msg['response']}")

# Simulate bot response (only if API is not implemented yet)
if st.session_state.messages and not st.session_state.messages[-1].get("response"):
    user_msg = st.session_state.messages[-1]["prompt"]
    bot_response = f"Echo: {user_msg}"  # simple placeholder response
    st.session_state.messages[-1]["response"] = bot_response
