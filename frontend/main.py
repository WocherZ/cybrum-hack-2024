import streamlit as st
import requests
import uuid


API_URL = "http://127.0.0.1:8000"

# Инициализация сессий для хранения информации о чатах и сообщениях
if "chats" not in st.session_state:
    st.session_state["chats"] = {}
    st.session_state["current_chat_id"] = None  # ID активного чата
    st.session_state["clear_input_flag"] = False  # Флаг для очистки поля ввода

# Функция для создания нового чата
def create_new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state["chats"][chat_id] = {
        "title": f"Чат {len(st.session_state['chats']) + 1}",
        "messages": []
    }
    st.session_state["current_chat_id"] = chat_id  # Переключаемся на новый чат

# Функция для добавления сообщения в чат
def add_message(user_message):
    chat_id = st.session_state["current_chat_id"]
    if chat_id:
        # Отправляем сообщение на бэкенд
        response = requests.post(
            f"{API_URL}/process-text/",
            json={"message": user_message}
        )
        
        if response.status_code == 200:
            answer_text = response.json()["response"]
            st.session_state["chats"][chat_id]["messages"].append({
                "user": user_message,
                "response": answer_text
            })
            st.session_state["clear_input_flag"] = True
        else:
            st.write("Ошибка на сервере: невозможно получить ответ")

# Создание нового чата по умолчанию, если чатов еще нет
if not st.session_state["chats"]:
    create_new_chat()

# Боковая панель
st.sidebar.title("Чаты")

# Кнопка для создания нового чата
if st.sidebar.button("Новый чат"):
    create_new_chat()

# Список чатов для выбора
chat_id = st.sidebar.radio("Выберите чат", options=list(st.session_state["chats"].keys()),
                           format_func=lambda x: st.session_state["chats"][x]["title"])

# Переключение текущего чата
st.session_state["current_chat_id"] = chat_id


# Основной раздел для отображения и работы с текущим чатом
if st.session_state["current_chat_id"]:
    chat = st.session_state["chats"][st.session_state["current_chat_id"]]
    st.header(chat["title"])

    # Отображение истории сообщений с форматированием чата
    for msg in chat["messages"]:
        st.write(f"**Вы:** {msg['user']}")
        st.write(f"**Ответ:** {msg['response']}")

    # Поле для ввода сообщения
    user_message = st.text_input("Введите сообщение", key="message_input")
    if st.button("Отправить"):
        if user_message:
            add_message(user_message)

    # Компонент для загрузки файла
    uploaded_file = st.file_uploader("Загрузите файл для обработки", type=["txt", "pdf", "xlsx"])
    if uploaded_file is not None:
        response = requests.post(f"{API_URL}/upload_file/", files={"file": uploaded_file})
        if response.status_code == 200:
            response_text = response.json()["response"]
            chat["messages"].append({
                "user": f"Загружен файл: {uploaded_file.name}",
                "response": response_text
            })
        else:
            st.write("Ошибка при обработке файла")