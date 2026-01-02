# LinkedIn Profile Optimization Agent - Installation Guide

## Quick Setup

### Basic Installation (Image Analysis Only)
```bash
pip install -r requirements.txt
```

### Full Installation (PDF + OCR Support)
```bash
# Install basic requirements
pip install -r requirements.txt

# Install PDF processing libraries
pip install PyPDF2 pdfplumber

# Install OCR libraries (optional)
pip install pytesseract PyMuPDF Pillow

# Note: OCR may require additional system dependencies:
# - On Ubuntu/Debian: sudo apt-get install tesseract-ocr
# - On macOS: brew install tesseract
# - On Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Troubleshooting

### Streamlit Cloud Deployment Issues
1. Use only basic requirements.txt for initial deployment
2. PDF libraries are optional - app will work with images only
3. OCR libraries are optional - app will work with text extraction only

### Common Errors
- `ModuleNotFoundError`: Install missing packages from requirements.txt
- `PDF processing failed`: PDF libraries not installed (optional)
- `OCR processing failed`: OCR libraries not installed (optional)

## Minimum Requirements
- Python 3.8+
- Streamlit >= 1.28.0
- OpenAI >= 1.3.0
- python-dotenv >= 1.0.0
- pydantic >= 2.5.0

## Optional Features
- PDF upload support: PyPDF2, pdfplumber
- OCR text extraction: pytesseract, PyMuPDF, Pillow

The app will work perfectly with just the basic requirements using image screenshots!
