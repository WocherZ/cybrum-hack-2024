from fastapi import (HTTPException, 
                     UploadFile, 
                     FastAPI, 
                     Form,
                     File)

from pydantic import BaseModel
from llama_cpp import Llama
from typing import Dict, Optional
import re

app = FastAPI()

# llm = Llama(model_path="models/Meta-Llama-3-8B.Q3_K_L.gguf", verbose=False)
llm = Llama(model_path="models/Vikhr-Nemo-12B-Instruct-R-21-09-24.Q4_0.gguf", verbose=False)

class MessageRequest(BaseModel):
    content: str

class MessageResponse(BaseModel):
    response: str

class FileResponse(BaseModel):
    filename: str
    content_preview: Optional[str]
    response: str

@app.post("/process-text", response_model=MessageResponse)
async def send_message(request: MessageRequest) -> MessageResponse:
    """
    Endpoint to process text input and return a response.
    """
    print(request.content)
    try:
        prompt = f"Q: {request.content} A: "
        # print(prompt)

        response = llm(prompt, max_tokens=512, stop=["Q:", "\n"])
        print(response)

        answer_text = response['choices'][0]['text']

        return MessageResponse(response=answer_text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-file")
async def upload_file(file: UploadFile = File(...),
                      content: str = Form(...), 
                      model: str = Form(...)) -> FileResponse:
    """
    Endpoint to upload and process a file, returning metadata and sample content.
    Reads the uploaded file, generates random data, and returns metadata and a preview.
    """
    try:
        file_content = await file.read()
        file_text = content.decode("utf-8", errors="ignore")
        
        prompt = f"{content}: {file_text[:500]} A: "
        response = llm(prompt, max_tokens=512, stop=["Q:", "\n"])
        # print(response)
        answer_text = response['choices'][0]['text'].strip()

        content_preview = file_text[:100] if file_text else None

        return FileResponse(filename=file.filename,
                            content_preview=content_preview,
                            response=answer_text)

    except Exception as e:
        # Handle errors with an HTTP exception
        raise HTTPException(status_code=500, detail=f"Failed to process the file: {str(e)}")

@app.get("/")
async def root() -> Dict[str, str]:
    """
    Debug endpoint. Returns a message indicating that the API is running.
    """
    return {"message": "API is running"}
