from fastapi import (HTTPException, 
                     UploadFile, 
                     FastAPI, 
                     File)
from pydantic import BaseModel
from llama_cpp import Llama
from typing import Dict, Optional


app = FastAPI()

llm = Llama(model_path="models/Meta-Llama-3-8B.Q3_K_L.gguf", verbose=False)

class MessageRequest(BaseModel):
    message: str

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
    try:
        prompt = f"Q: {request.message} A: "
        response = llm(prompt, max_tokens=256, stop=["Q:", "\n"])
        # print(response)
        answer_text = response['choices'][0]['text']

        return MessageResponse(response=answer_text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-file")
async def upload_file(file: UploadFile = File(...)) -> FileResponse:
    """
    Endpoint to upload and process a file, returning metadata and sample content.
    Reads the uploaded file, generates random data, and returns metadata and a preview.
    """
    try:
        content = await file.read()
        content_text = content.decode("utf-8", errors="ignore")
        
        prompt = f"Q: {content_text[:500]} A: "
        response = llm(prompt, max_tokens=512, stop=["Q:", "\n"])
        # print(response)
        answer_text = response['choices'][0]['text'].strip()

        content_preview = content_text[:100] if content_text else None

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
