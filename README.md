# LinkedIn Profile Optimization Agent

A production-ready AI-powered web application that optimizes LinkedIn profiles using a two-stage pipeline: vision-based profile extraction and AI-driven optimization strategies.

## 🚀 Features

### Core Functionality
- **Vision Digitizer**: Extracts structured text from LinkedIn profile screenshots
- **AI Strategist**: Generates comprehensive optimization plans using GPT-4o or custom fine-tuned Llama 3
- **Multi-Model Support**: Switch between teacher (GPT-4o) and student (custom Llama 3) models
- **Interactive Chat**: Follow-up questions and iterative improvements
- **Training Data Collection**: Collects high-quality examples for fine-tuning

### Optimization Sections
- Overall profile review and positioning
- Headline optimization with 3 alternatives
- About section storytelling rewrite
- Experience bullet enhancement with metrics
- Skills strategy and recommendations
- Recommendations strategy
- 30-day content and engagement plan

### MLOps Features
- Together AI integration for Llama 3 fine-tuning
- Real-time training job monitoring
- Cost estimation for fine-tuning
- Dataset preparation and quality filtering
- Model deployment and testing

## 🌐 Deploying to Streamlit Community Cloud

This application is optimized for Streamlit Community Cloud deployment with no brittle local paths.

### Quick Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Create Streamlit Cloud App**
   - Go to [Streamlit Community Cloud](https://share.streamlit.io/)
   - Click "New app" 
   - Connect your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure Environment Secrets**
   In your Streamlit Cloud app dashboard, go to **Secrets** and add:

   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   TOGETHER_API_KEY=your_together_api_key_here
   # Optional:
   LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
   LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
   LANGFUSE_HOST=your_langfuse_host_here
   ```

4. **Optional: Set Custom Paths**
   ```bash
   TRAINING_DATA_PATH=/tmp/training_dataset.jsonl
   ```

### Cloud Deployment Features

✅ **Environment-Aware Configuration**
- Automatically detects cloud vs local environment
- Uses environment variables only (no .env dependency in cloud)
- Graceful fallbacks for missing optional services

✅ **Ephemeral Storage Handling**
- All file operations use `/tmp/` directory
- Training data and logs are stored in temporary locations
- Clear UI indicators when using temporary storage

✅ **Optimized for Cloud Constraints**
- Minimal dependencies for faster installation
- Memory-efficient logging with automatic cleanup
- Cached engine initialization for better performance
- User-friendly error messages for common cloud issues

✅ **Production Ready**
- Comprehensive error handling and timeouts
- Rate limit detection and user guidance
- In-memory file downloads (no filesystem dependencies)
- Environment status dashboard

### Important Notes for Cloud Deployment

⚠️ **Data Persistence**: Training data and logs are ephemeral on Streamlit Cloud and may be cleared when the app stops or is redeployed. For production-grade persistence, integrate external storage (S3, database, etc.).

⚠️ **Resource Limits**: Streamlit Cloud has memory and time limits. The app includes optimizations like:
- Image resizing to reduce memory usage
- Token estimation to prevent large requests
- Automatic log cleanup (keeps only 1000 recent entries)

⚠️ **API Costs**: Be mindful of OpenAI API usage when deploying publicly. The app shows token usage estimates in the admin panel.

### Troubleshooting Cloud Deployment

| Issue | Solution |
|-------|----------|
| **Missing environment variables** | Check Secrets section in Streamlit Cloud dashboard |
| **App crashes on startup** | Verify all required API keys are configured |
| **Slow startup** | Dependencies are optimized, but initial API key validation may take time |
| **Data disappears** | This is expected - use external storage for persistence |
| **Rate limiting** | Built-in rate limit detection with user-friendly messages |

## 📋 Requirements

### System Requirements
- Python 3.8+
- 4GB+ RAM recommended
- Stable internet connection

### API Keys Required
- **OpenAI API Key**: For GPT-4o vision and text models
- **Together AI Key**: For Llama 3 fine-tuning and inference (optional)
- **Langfuse Keys**: For observability (optional)

## 🛠️ Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd linkedin-optimizer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TOGETHER_API_KEY=your_together_api_key_here
# Optional:
LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
LANGFUSE_HOST=your_langfuse_host_here
```

## 🚀 Running the Application

### Start Streamlit App
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload Profile Screenshots
- Take clear screenshots of your LinkedIn profile sections:
  - Headline area
  - About section
  - Experience entries
  - Skills section
- Upload multiple screenshots using the file uploader

### 2. Configure Target
- Set your target industry (e.g., "Technology", "Finance", "Healthcare")
- Specify your target role (e.g., "Software Engineer", "Product Manager")
- Choose between GPT-4o or custom Llama 3 model

### 3. Analyze and Optimize
- Click "Analyze Profile" to extract data and generate recommendations
- Review the comprehensive optimization report
- Use feedback buttons to improve future recommendations

### 4. Iterate with Chat
- Ask follow-up questions in the chat interface
- Provide additional context for more personalized recommendations
- Download the final report as text file

## 🤖 Fine-Tuning Your Own Model

### 1. Collect Training Data
- Use the app regularly to generate optimization examples
- Provide feedback (👍/👎) on recommendations
- High-quality examples are automatically saved to `training_dataset.jsonl`

### 2. Prepare Dataset
```python
# Via Admin Panel in the app
# Or programmatically:
from src.mlops import mlops_manager
mlops_manager.prepare_dataset_for_training("clean_dataset.jsonl")
```

### 3. Start Fine-Tuning
```python
job_id = mlops_manager.start_finetune_job()
print(f"Training job started: {job_id}")
```

### 4. Monitor Progress
```python
status, model_id = mlops_manager.check_finetune_status(job_id)
print(f"Status: {status}")
if model_id:
    print(f"Model ready: {model_id}")
```

### 5. Use Custom Model
- The fine-tuned model will appear as "Student (Custom Llama 3)" option
- Switch between models to compare performance

## 📊 Architecture

### Two-Stage Pipeline
1. **Vision Stage**: GPT-4o Vision processes screenshots → Structured JSON
2. **Strategy Stage**: Text-only models generate optimization recommendations

### Key Components
- `src/vision_engine.py`: Profile data extraction from images
- `src/strategy_engine.py`: Optimization plan generation
- `src/prompt_templates.py`: Industry-specific prompts
- `src/mlops.py`: Fine-tuning and model management
- `src/telemetry.py`: Observability and logging
- `src/training_logger.py`: Training data collection

### Data Flow
```
Screenshots → Vision Engine → Profile JSON → Strategy Engine → Markdown Report
                                      ↓
                              Training Dataset → Fine-tuning → Custom Model
```

## 🔧 Configuration Options

### Model Settings
- `MAX_IMAGE_WIDTH`: Maximum width for image processing (default: 1024)
- `DEFAULT_MODEL`: Default model choice (default: "gpt4o")
- `CUSTOM_LLAMA3_MODEL_ID`: Fine-tuned model identifier

### Fine-Tuning Parameters
- Base model: `meta-llama-3-8b-instruct`
- Training epochs: 3
- Batch size: 4
- Learning rate: 1e-5

## 📈 Monitoring and Analytics

### Telemetry
- Vision extraction metrics (success rate, processing time)
- Strategy generation metrics (token usage, model performance)
- User feedback tracking
- Usage statistics by industry and role

### Dataset Analytics
- Training example quality distribution
- Industry and role coverage
- Model performance comparison
- Cost estimation for fine-tuning

## 🐛 Troubleshooting

### Common Issues

#### API Key Errors
```
Configuration Error: OPENAI_API_KEY is required
```
**Solution**: Ensure your `.env` file contains valid API keys

#### Image Processing Issues
```
Error processing image: Unsupported format
```
**Solution**: Use PNG, JPG, or JPEG formats under 10MB

#### Model Unavailable
```
Custom Llama 3 model not available
```
**Solution**: Complete fine-tuning process or switch to GPT-4o

#### Memory Issues
**Solution**: Reduce image size or limit number of concurrent uploads

### Debug Mode
Enable detailed logging by setting environment variable:
```bash
export STREAMLIT_LOG_LEVEL=debug
```

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
pytest tests/

# Code formatting
black src/ app.py
```

### Project Structure
```
linkedin-optimizer/
├── app.py                 # Streamlit web application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # This file
└── src/
    ├── __init__.py
    ├── config.py         # Configuration management
    ├── vision_engine.py  # Image processing and OCR
    ├── strategy_engine.py # AI optimization generation
    ├── prompt_templates.py # Dynamic prompt generation
    ├── prompt_formatter.py # Model-specific formatting
    ├── image_utils.py    # Image processing utilities
    ├── telemetry.py      # Observability and logging
    ├── training_logger.py # Training data collection
    └── mlops.py          # Fine-tuning operations
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o vision and text capabilities
- Together AI for Llama 3 fine-tuning infrastructure
- Streamlit for the web framework
- Langfuse for observability tools

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the configuration requirements
3. Create an issue with detailed error messages and system information

---

**Transform your LinkedIn presence with AI-powered optimization! 🚀**
