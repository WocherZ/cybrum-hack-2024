from fastapi import (HTTPException, 
                     UploadFile, 
                     FastAPI, 
                     File)
from pydantic import BaseModel
from llama_cpp import Llama
from typing import Dict
import random
import string
import uuid


app = FastAPI()

llm = Llama(model_path="models/Meta-Llama-3-8B.Q3_K_L.gguf", verbose=False)

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

@app.post("/process-text", response_model=MessageResponse)
async def send_message(request: MessageRequest) -> MessageResponse:
    try:
        prompt = f"Q: {request.message} A: "
        response = llm(prompt, max_tokens=256, stop=["Q:", "\n"])
        print(response)
        answer_text = response['choices'][0]['text']
        return MessageResponse(response=answer_text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
