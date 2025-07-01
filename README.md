# Document Parser App

A FastAPI web application that parses .docx files and displays their content organized by sections, paragraphs, and sentences.

## Features

- **File Upload**: Drag-and-drop or click to upload .docx files
- **Content Parsing**: Automatically extracts and organizes document content into:
  - Sections (headers and titles)
  - Paragraphs (complete text blocks)
  - Sentences (individual sentence breakdown)
- **Interactive View**: Toggle between different content views with color-coded display
- **Responsive UI**: Clean, modern interface that works on different screen sizes

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Open your browser and go to: `http://localhost:8000`

## Usage

1. Visit the web interface at `http://localhost:8000`
2. Upload a .docx file using drag-and-drop or the file picker
3. Use the toggle buttons to switch between viewing:
   - **Sections**: Document headers and section titles
   - **Paragraphs**: Complete text paragraphs
   - **Sentences**: Individual sentences from the document

## Dependencies

- FastAPI - Web framework
- python-docx - Document parsing
- Uvicorn - ASGI server
- Jinja2 - Template engine
- python-multipart - File upload support