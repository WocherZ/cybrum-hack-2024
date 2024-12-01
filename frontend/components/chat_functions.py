import uuid
import time
import requests
import streamlit as st
from typing import Dict
from pydantic import BaseModel
from streamlit.runtime.uploaded_file_manager import UploadedFile

from config import API_URL


def create_chat() -> None:
    """
    Create a new chat and switch to it.
    """
    chat_id = str(uuid.uuid4())
    num_chats = len(st.session_state["chats"])
    st.session_state["chats"][chat_id] = {
        "title": f"Новый чат {num_chats if num_chats > 0 else ''}",
        "messages": []
    }
    st.session_state["current_chat_id"] = chat_id  # Switch to the new chat

def handle_input(content: str,
                 uploaded_file: UploadedFile = None, 
                 selected_model: str = None,
                 input_type: str = "message") -> Dict:
    """
    Add a message to the current chat.

    Args:
        content (str): The content of the message.
        uploaded_file (st.UploadedFile, optional): The uploaded file. Defaults to None.
        selected_model (str, optional): The selected model. Defaults to None.
        input_type (str, optional): The input type. Defaults to "message".

    Returns:
        dict: The response from the LLM in the format {"role": ..., "content": ...}.
    """
    chat_id = st.session_state["current_chat_id"]
    if chat_id:
        if input_type == "message" and content:
            response = requests.post(f"{API_URL}/process-text/", 
                                     json={"content": content,
                                           "model": selected_model})
            
        elif input_type == "file" and uploaded_file:

            file = {"file": (uploaded_file.name, 
                             uploaded_file.getvalue(), 
                             uploaded_file.type)}
            
            data = {"content": content,
                    "model": selected_model}

            response = requests.post(f"{API_URL}/process-file/", 
                                     files=file,
                                     data=data)
            
        else:
            return {"role": "assistant",
                    "content": "Ошибка: не передан контент или файл."}
        
        if response.status_code == 200:
            response_text = response.json().get("response", 
                                                "Нет ответа от модели.")
            return {"role": "model", 
                    "content": response_text}
        else:
            error_message = response.json().get("error", 
                                                "Неизвестная ошибка.")
            return {"role": "assistant",
                    "content": f"Ошибка: {error_message}"}

def display_text_incrementally(container, text, delay=0.2):
    """
    Display text incrementally in the Streamlit container.
    
    Args:
        container: The Streamlit container (e.g., st.empty()) to update.
        text (str): The full text to display incrementally.
        delay (float): Time in seconds to wait between adding each word.
    """
    words = text.split()
    displayed_text = ""
    for word in words:
        displayed_text += word + " "
        container.markdown(displayed_text)  # Update the container
        time.sleep(delay)  # Wait before showing the next word