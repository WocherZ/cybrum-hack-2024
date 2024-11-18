import streamlit as st
import requests
import uuid

from config import API_URL

def create_new_chat():
    """
    Create a new chat and switch to it.
    """
    chat_id = str(uuid.uuid4())
    st.session_state["chats"][chat_id] = {
        "title": f"Чат {len(st.session_state['chats']) + 1}",
        "messages": []
    }
    st.session_state["current_chat_id"] = chat_id  # Switch to the new chat

def add_message(user_message):
    """
    Add a message to the current chat.
    """
    chat_id = st.session_state["current_chat_id"]
    if chat_id:
        response = requests.post(f"{API_URL}/process-text/",
                                 json={"message": user_message})
        
        if response.status_code == 200:
            answer_text = response.json()["response"]
            st.session_state["chats"][chat_id]["messages"].append({
                "user": user_message,
                "response": answer_text
            })
            st.session_state["clear_input_flag"] = True
        else:
            st.write("Ошибка на сервере: невозможно получить ответ")

def add_file(file):
    """
    Add a file to the current chat.
    """
    chat_id = st.session_state["current_chat_id"]
    if chat_id:
        response = requests.post(f"{API_URL}/process-file/",
                                 files={"file": file})
        print("Resp", response)
        if response.status_code == 200:
            response_text = response.json()["response"]
            st.session_state["chats"][chat_id]["messages"].append({
                "user": f"Загружен файл: {file.name}",
                "response": response_text
            })
        else:
            st.write("Ошибка при обработке файла")
