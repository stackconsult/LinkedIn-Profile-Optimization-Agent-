# LinkedIn Profile Optimization Agent - Installation Guide

## Core Features Installation

### Complete Installation (All Features)
```bash
pip install -r requirements.txt
```

This includes:
- **LinkedIn screenshot analysis** (Core)
- **PDF profile analysis** (Core)
- **OCR text extraction** (Core)
- **Phase 2 intelligence features** (Core)
- **One-click implementation** (Core)

## Core Requirements
- Python 3.8+
- streamlit>=1.28.0
- openai>=1.3.0
- python-dotenv>=1.0.0
- pydantic>=2.5.0
- PyPDF2>=3.0.1 (PDF processing)
- pdfplumber>=0.10.0 (PDF processing)
- pytesseract>=0.3.10 (OCR)
- PyMuPDF>=1.23.0 (OCR)
- Pillow>=10.0.0 (Image processing)

## Features Included

### ✅ Core Features (Always Available)
- LinkedIn screenshot analysis
- PDF resume/CV analysis with OCR
- Complete profile optimization
- Quality scoring system
- Dynamic checklist generation
- One-click implementation
- Professional UI/UX

### 🎯 Optional Features
- Together AI models (requires together library and API key)
- Advanced MLOps fine-tuning (requires Together AI)

## Troubleshooting

### Common Issues
- `ModuleNotFoundError`: Install missing packages from requirements.txt
- `PDF processing failed`: Ensure all PDF libraries are installed
- `OCR processing failed`: Install Tesseract OCR system dependency

### System Dependencies for OCR
For full OCR functionality, you may need to install Tesseract:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download from https://github.com/UB-Mannheim/tesseract/wiki

## Deployment Notes

### Streamlit Cloud
All core features including PDF analysis and OCR are fully supported on Streamlit Cloud with the complete requirements.txt file.

### Local Development
Full feature set available with complete installation.

## Quick Start
1. Install all requirements: `pip install -r requirements.txt`
2. Set up your OpenAI API key
3. Run: `streamlit run app.py`
4. Upload LinkedIn screenshots or PDF files
5. Get your optimized profile!

The LinkedIn Profile Optimization Agent is designed to be a comprehensive tool with PDF analysis as a core feature, not an optional add-on.
