from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import tempfile
from docx import Document
import re
from typing import List, Dict

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class DocumentParser:
    def __init__(self):
        pass
    
    def parse_docx(self, file_path: str) -> Dict[str, List[str]]:
        doc = Document(file_path)
        
        sections = []
        paragraphs = []
        sentences = []
        
        current_section = ""
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue
                
            paragraphs.append(text)
            
            if self._is_section_header(text):
                sections.append(text)
                current_section = text
            
            paragraph_sentences = self._split_into_sentences(text)
            sentences.extend(paragraph_sentences)
        
        return {
            "sections": sections,
            "paragraphs": paragraphs,
            "sentences": sentences
        }
    
    def _is_section_header(self, text: str) -> bool:
        return (
            len(text) < 100 and
            (text.isupper() or 
             re.match(r'^[0-9]+\.', text) or
             re.match(r'^[A-Z][a-z\s]+$', text) and len(text.split()) <= 5)
        )
    
    def _split_into_sentences(self, text: str) -> List[str]:
        sentence_endings = re.compile(r'[.!?]+')
        sentences = sentence_endings.split(text)
        return [s.strip() for s in sentences if s.strip()]

parser = DocumentParser()
parsed_content = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "content": parsed_content})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global parsed_content
    
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are allowed")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        parsed_content = parser.parse_docx(temp_file_path)
        parsed_content['filename'] = file.filename
        return {"message": "File processed successfully", "content": parsed_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        os.unlink(temp_file_path)

@app.get("/content")
async def get_content():
    return parsed_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)