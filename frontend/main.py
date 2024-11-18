import streamlit as st
import requests
import uuid

from config import API_URL
from components.chat_functions import (create_new_chat, 
                                       add_message,
                                       add_file)

if "chats" not in st.session_state:
    st.session_state["chats"] = {}
    st.session_state["current_chat_id"] = None  # Active chat ID
    st.session_state["clear_input_flag"] = False  # Flag for clearing input field

# Create a new chat if it doesn't exist
if not st.session_state["chats"]:
    create_new_chat()

# Sidebar for chat selection
st.sidebar.title("Чаты")

# Button to create a new chat
if st.sidebar.button("Новый чат"):
    create_new_chat()
    st.rerun()

# Radio button to select a chat
chat_id = st.sidebar.radio("Выберите чат", 
                           options=list(st.session_state["chats"].keys()),
                           format_func=lambda x: st.session_state["chats"][x]["title"])

# Update the current chat ID
st.session_state["current_chat_id"] = chat_id

# Main content of the app
if st.session_state["current_chat_id"]:
    chat = st.session_state["chats"][st.session_state["current_chat_id"]]
    st.header(chat["title"])

    # Display chat messages history
    for msg in chat["messages"]:
        st.write(f"**Вы:** {msg['user']}")
        st.write(f"**Ответ:** {msg['response']}")

    # Input text
    user_message = st.text_input("Введите сообщение", 
                                 key="message_input")
    if st.button("Отправить"):
        if user_message:
            add_message(user_message)
            st.rerun()

    # Input file
    uploaded_file = st.file_uploader("Загрузите файл для обработки", 
                                     type=["txt", "pdf", "xlsx"])
    if st.button("Обработать"):
        if uploaded_file is not None:
            add_file(uploaded_file)
            st.rerun()
