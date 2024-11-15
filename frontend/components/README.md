components/file_uploader.py
```(python)
import streamlit as st
from typing import Optional

def file_uploader(label: str = "Upload file") -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
    uploaded_file = st.file_uploader(label, type=["csv", "txt", "jpg", "png", "pdf"])
    if uploaded_file is not None:
        st.write(f"Loaded file: {uploaded_file.name}")
    return uploaded_file
```

components/text_input.py
```(python)
import streamlit as st

def text_input(label: str = "Enter text") -> str:
    user_text = st.text_area(label)
    if user_text:
        st.write(f"Text entered: {user_text}")
    return user_text
```

