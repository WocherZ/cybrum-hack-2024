schemas/request_schemas.py

```(python)
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
```

schemas/response_schemas.py
```(python)
from pydantic import BaseModel
from typing import Optional

class TextResponse(BaseModel):
    processed_text: str

class FileResponse(BaseModel):
    filename: str
    content_type: str
    size: str
    random_number: int
    random_string: str
    content_preview: Optional[str] = None
```

