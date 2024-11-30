import uuid
import requests
import streamlit as st

from config import API_URL, MODELS
from components.chat_functions import (create_chat, 
                                       handle_input)

# Initialize session states
if "chats" not in st.session_state:
    st.session_state["chats"] = {}
    st.session_state["current_chat_id"] = None  # Active chat ID
    st.session_state["clear_input_flag"] = False  # Flag for clearing input field
    st.session_state["edit_mode"] = False  # Toggle for editing chat name
    
# Create a new chat if it doesn't exist
if not st.session_state["chats"]:
    create_chat()

# Sidebar content
with st.sidebar:
    # Model selection dropdown
    st.selectbox("Выберите модель",
                 options=MODELS,
                 key="selected_model",
                 help="Выберите модель, которая будет использоваться для обработки сообщений.")
    
    # Display source code link
    st.markdown("""[![Source Code](https://github.com/codespaces/badge.svg)](https://github.com/WocherZ/cybrum-hack-2024)""")

    # Title for chat section
    st.title("Чаты")

    # Button to create a new chat
    if st.button("Новый чат"):
        create_chat()
        st.rerun()

    # Radio button to select a chat
    chat_id = st.radio("Выберите чат", 
                       options=list(st.session_state["chats"].keys()),
                       format_func=lambda x: st.session_state["chats"][x]["title"])

# Update the current chat ID
st.session_state["current_chat_id"] = chat_id

# Main content of the app
if st.session_state["current_chat_id"]:
    chat = st.session_state["chats"][st.session_state["current_chat_id"]]

    # Show title and chat name edit button
    col1, col2 = st.columns([9, 1])
    with col1:
        if st.session_state["edit_mode"]:
            # Show input for editing
            new_title = st.text_input("Введите название чата",
                                      value=chat["title"],
                                      key="chat_title_input")
            
            # Save changes and exit edit mode
            if st.button("Сохранить", key="save_title"):
                st.session_state["chats"][st.session_state["current_chat_id"]]["title"] = new_title
                st.session_state["edit_mode"] = False
                st.rerun()
        else:
            # Show title
            st.title(f"💬 {chat['title']}")
    
    with col2:    
        if st.button("✏️", 
                     key="edit_title", 
                     help="Редактировать название чата",
                     on_click=lambda: st.session_state.update({'edit_mode': True})
                     ):
            # Enable edit mode
            st.session_state["edit_mode"] = True

    st.caption("🚀 Демо сервис команды AXIOM")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant",
                                         "content": "Как я могу помочь?"}]
        
    # Display existing chat messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    user_message = st.chat_input("Введите сообщение")

    # Handle new user input
    if user_message:
        st.session_state.messages.append({"role": "user", 
                                          "content": user_message})
        st.chat_message("user").write(user_message)

        # Generate response
        response = handle_input(content=user_message,
                                selected_model=st.session_state["selected_model"],
                                input_type="message")

        # Extract and display assistant's response
        msg = response["content"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    
    st.divider()
    with st.expander("📂 Загрузить файл", expanded=False):
        # css = '''
        #     <style>
        #         [data-testid='stFileUploader'] {
        #             width: max-content;
        #         }
        #         [data-testid='stFileUploader'] section {
        #             padding: 0;
        #             float: left;
        #         }
        #         [data-testid='stFileUploader'] section > input + div {
        #             display: none;
        #         }
        #         [data-testid='stFileUploader'] section + div {
        #             float: right;
        #             padding-top: 0;
        #         }
        #     </style>
        #     '''
        
        uploaded_file = st.file_uploader("Выберите файл",
                                         type=["txt", "pdf", "docx"],
                                         label_visibility="collapsed")
        # st.markdown(css, unsafe_allow_html=True)

        if uploaded_file is not None:
            if user_message:
                st.session_state.messages.append({"role": "user", 
                                          "content": user_message})
                st.chat_message("user").write(user_message)

                response = handle_input(content=user_message, 
                                        uploaded_file=uploaded_file, 
                                        selected_model=st.session_state["selected_model"],
                                        input_type="file")
                msg = response["content"]
                if "Ошибка" not in msg:
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    st.chat_message("assistant").write(msg)
