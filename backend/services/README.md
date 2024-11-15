services/inference.py

```(python)
import random
import string

def generate_text_response(text: str) -> str:
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return f"Processed text for '{text}': {random_text}"
```

services/data_processing.py
```(python)
import random
import string

def process_file_content(file_content: bytes, filename: str, content_type: str) -> dict:
    random_number = random.randint(1, 100)
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    content_preview = file_content[:100].decode("utf-8", errors="ignore")

    return {
        "filename": filename,
        "content_type": content_type,
        "size": str(len(file_content)),
        "content_preview": content_preview,
        "random_number": random_number,
        "random_string": random_string
    }
```

