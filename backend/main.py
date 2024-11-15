from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Dict
import random
import string

app = FastAPI()


class TextData(BaseModel):
    """Модель данных для передачи текстовой информации."""
    text: str

@app.post("/process-text")
async def process_text(data: TextData) -> Dict[str, str]:
    """
    Эндпоинт для обработки текстовых данных.
    
    Генерирует случайный ответ и возвращает его вместе с переданным текстом.
    """
    # TODO: insert real text processing

    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    processed_text = f"User text: {data.text}\n Answer: {random_text}"
    
    return {"processed_text": processed_text}

@app.post("/process-file")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Эндпоинт для загрузки и обработки файла.
    
    Возвращает информацию о файле и случайные данные.
    """
    content = await file.read()
    
    random_number = random.randint(1, 100)
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": str(len(content)),               # Преобразование в строку
        "content_preview": content[:100].decode("utf-8", errors="ignore"),
        "random_number": str(random_number),      # Преобразование в строку
        "random_string": random_string
    }

@app.get("/")
async def root() -> Dict[str, str]:
    """
    Проверочный эндпоинт для подтверждения работы API.
    
    Возвращает простое сообщение.
    """
    return {"message": "API is running"}
