import streamlit as st
import requests

FASTAPI_URL = "http://127.0.0.1:8000"

st.title("ML hack backend and frontend template: load file or text input")

uploaded_file = st.file_uploader("Load file", type=["txt"])

def send_file_to_backend(file):
    files = {"file": (file.name, file, file.type)}
    response = requests.post(f"{FASTAPI_URL}/process-file", files=files)
    return response.json()

if uploaded_file is not None:
    st.write("File details:")
    st.write(f"Name: {uploaded_file.name}")
    file_details = {
        "Name": uploaded_file.name,
        "Type": uploaded_file.type,
        "Size": f"{uploaded_file.size} bytes",
    }
    st.json(file_details)

    if uploaded_file.type == "text/plain":
        st.write("File content:")
        content = uploaded_file.read().decode("utf-8")
        st.text(content)

    if st.button("Send File"):
        response = send_file_to_backend(uploaded_file)
        st.write("Backend response:", response)

user_text = st.text_area("Input text")

def send_text_to_backend(text):
    response = requests.post(f"{FASTAPI_URL}/process-text", json={"text": text})
    return response.json()

if user_text:
    st.write("User input text:")
    st.write(user_text)

    if st.button("Send data"):
        response = send_text_to_backend(user_text)
        st.success("Data sent successfully!")
        st.write("Backend response:", response)
