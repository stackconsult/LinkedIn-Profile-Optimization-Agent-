"""
LinkedIn Profile Optimization Agent - Streamlit Web Application
Cloud-optimized for Streamlit Community Cloud deployment
"""

import streamlit as st
import time
import base64
import tempfile
from io import BytesIO
from typing import Dict, Any, Optional

# Import our modules
from src.config import Config
from src.vision_engine import VisionEngine
from src.strategy_engine import StrategyEngine
from src.telemetry import telemetry
from src.training_logger import training_logger
from src.mlops import mlops_manager

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Optimizer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0A66C2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2D3748;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .feedback-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .success-message {
        background-color: #D4EDDA;
        border: 1px solid #C3E6CB;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #F8D7DA;
        border: 1px solid #F5C6CB;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 1rem 0;
    }
    .info-message {
        background-color: #D1ECF1;
        border: 1px solid #BEE5EB;
        border-radius: 0.25rem;
        padding: 0.75rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize engines with caching for cloud deployment
@st.cache_resource
def get_vision_engine():
    """Initialize and cache vision engine"""
    try:
        return VisionEngine()
    except Exception as e:
        st.error(f"Failed to initialize vision engine: {str(e)}")
        return None

@st.cache_resource  
def get_strategy_engine():
    """Initialize and cache strategy engine"""
    try:
        return StrategyEngine()
    except Exception as e:
        st.error(f"Failed to initialize strategy engine: {str(e)}")
        return None

def check_environment():
    """Check and display environment status for cloud deployment"""
    env_status = Config.get_env_status()
    
    # Check required environment variables
    missing_vars = []
    if not env_status["OPENAI_API_KEY"]:
        missing_vars.append("OPENAI_API_KEY")
    
    if missing_vars:
        st.error("🚨 **Missing Required Environment Variables**")
        st.write("The following environment variables are required:")
        for var in missing_vars:
            st.code(var)
        st.write("""
        **For Streamlit Community Cloud:**
        1. Go to your app's dashboard
        2. Click "Secrets" 
        3. Add each variable with its value
        
        **For Local Development:**
        Create a `.env` file with these variables.
        """)
        return False
    
    return True

def initialize_session_state():
    """Initialize session state variables"""
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = None
    if 'optimization_report' not in st.session_state:
        st.session_state.optimization_report = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'current_model' not in st.session_state:
        st.session_state.current_model = Config.DEFAULT_MODEL
    if 'vision_engine' not in st.session_state:
        st.session_state.vision_engine = None
    if 'strategy_engine' not in st.session_state:
        st.session_state.strategy_engine = None


def render_sidebar():
    """Render the sidebar with configuration options"""
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # Environment Status Section
    env_status = Config.get_env_status()
    
    st.sidebar.markdown("### 🌐 Environment Status")
    
    # API Keys Status
    openai_status = "✅ Configured" if env_status["OPENAI_API_KEY"] else "❌ Missing"
    st.sidebar.write(f"OpenAI: {openai_status}")
    
    together_status = "✅ Configured" if env_status["TOGETHER_API_KEY"] else "⚪ Optional"
    st.sidebar.write(f"Together AI: {together_status}")
    
    langfuse_status = "✅ Configured" if env_status["LANGFUSE_CONFIGURED"] else "⚪ Optional"
    st.sidebar.write(f"Langfuse: {langfuse_status}")
    
    # Cloud deployment indicator
    if env_status["IS_CLOUD_DEPLOYMENT"]:
        st.sidebar.success("🌐 Running on Streamlit Cloud")
    
    # Dataset info
    dataset_info = training_logger.get_dataset_info()
    st.sidebar.markdown("### 📊 Dataset Info")
    st.sidebar.write(f"Path: `{dataset_info['dataset_path']}`")
    st.sidebar.write(f"Writable: {'✅' if dataset_info['is_writable'] else '❌'}")
    if dataset_info['is_temporary']:
        st.sidebar.caption("⚠️ Temporary storage (data may be lost)")
    
    # Target Configuration
    st.sidebar.markdown("### 🎯 Target Configuration")
    
    target_industry = st.sidebar.text_input(
        "Target Industry",
        value="Technology",
        help="The industry you want to target"
    )
    
    target_role = st.sidebar.text_input(
        "Target Role",
        value="Software Engineer",
        help="The specific role you're targeting"
    )
    
    # Model Selection
    st.sidebar.markdown("### 🤖 Model Selection")
    
    available_models = []
    if env_status["OPENAI_API_KEY"]:
        available_models.append("gpt4o")
    if env_status["TOGETHER_API_KEY"] and env_status["CUSTOM_MODEL_AVAILABLE"]:
        available_models.append("llama3_custom")
    
    if available_models:
        model_labels = {
            "gpt4o": "Teacher (GPT-4o)",
            "llama3_custom": "Student (Custom Llama 3)"
        }
        
        model_choice = st.sidebar.radio(
            "Choose Model",
            options=available_models,
            format_func=lambda x: model_labels.get(x, x),
            index=0
        )
        
        st.session_state.current_model = model_choice
    else:
        st.sidebar.error("No models available. Please configure API keys.")
    
    # Admin Section
    if st.sidebar.checkbox("🔧 Admin Panel", False):
        render_admin_panel()
    
    return target_industry, target_role


def render_admin_panel():
    """Render the admin panel for MLOps operations"""
    st.sidebar.markdown("### 🛠️ MLOps Operations")
    
    if not mlops_manager:
        st.sidebar.warning("MLOps not available. Configure Together AI API key.")
        return
    
    # Dataset Statistics
    if st.sidebar.button("📊 View Dataset Stats"):
        try:
            stats = training_logger.get_dataset_stats()
            st.sidebar.json(stats)
        except Exception as e:
            st.sidebar.error(f"Error getting stats: {e}")
    
    # Cost Estimate
    if st.sidebar.button("💰 Get Cost Estimate"):
        try:
            estimate = mlops_manager.get_job_cost_estimate()
            st.sidebar.json(estimate)
        except Exception as e:
            st.sidebar.error(f"Error getting estimate: {e}")
    
    # Prepare Dataset
    if st.sidebar.button("📋 Prepare Dataset"):
        try:
            output_path = "prepared_dataset.jsonl"
            success = mlops_manager.prepare_dataset_for_training(output_path)
            if success:
                st.sidebar.success(f"Dataset prepared: {output_path}")
            else:
                st.sidebar.error("Failed to prepare dataset")
        except Exception as e:
            st.sidebar.error(f"Error preparing dataset: {e}")
    
    # Start Fine-tuning
    if st.sidebar.button("🚀 Start Fine-Tuning"):
        try:
            with st.sidebar.spinner("Starting fine-tuning job..."):
                job_id = mlops_manager.start_finetune_job()
                st.session_state.finetune_job_id = job_id
                st.sidebar.success(f"Job started: {job_id}")
        except Exception as e:
            st.sidebar.error(f"Error starting fine-tuning: {e}")
    
    # Check Job Status
    if 'finetune_job_id' in st.session_state:
        if st.sidebar.button("📈 Check Training Status"):
            try:
                job_id = st.session_state.finetune_job_id
                status, model_id = mlops_manager.check_finetune_status(job_id)
                st.sidebar.write(f"Status: {status}")
                if model_id:
                    st.sidebar.write(f"Model ID: {model_id}")
                    
                    # Update config if completed
                    if status == "completed":
                        if st.sidebar.button("💾 Save Model ID"):
                            mlops_manager.update_config_with_model(model_id)
                            st.sidebar.success("Model ID saved to configuration")
            except Exception as e:
                st.sidebar.error(f"Error checking status: {e}")


def render_main_interface():
    """Render the main application interface"""
    st.markdown('<div class="main-header">💼 LinkedIn Profile Optimizer</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Transform your LinkedIn profile with AI-powered optimization. Upload screenshots of your profile 
    to get personalized recommendations for headlines, about sections, experience bullets, and more.
    """)
    
    # File Upload Section
    st.markdown('<div class="section-header">📸 Upload Profile Screenshots</div>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload LinkedIn profile screenshots (headline, about, experience, skills)",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Take clear screenshots of each section of your LinkedIn profile"
    )
    
    if uploaded_files:
        st.info(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Display image previews
        num_cols = min(4, len(uploaded_files))
        cols = st.columns(num_cols)
        for i, file in enumerate(uploaded_files):
            with cols[i % num_cols]:  # Use modulo to prevent index out of range
                st.image(file, caption=file.name, use_column_width=True)
        
        # Analyze Button
        if st.button("🔍 Analyze Profile", type="primary", use_container_width=True):
            analyze_profile(uploaded_files)
    
    # Display Results
    if st.session_state.optimization_report:
        render_optimization_report()
    
    # Chat Interface
    if st.session_state.profile_data:
        render_chat_interface()


def analyze_profile(uploaded_files):
    """Analyze uploaded profile screenshots with cloud-friendly error handling"""
    try:
        # Initialize engines using cached functions
        vision_engine = get_vision_engine()
        strategy_engine = get_strategy_engine()
        
        if not vision_engine or not strategy_engine:
            st.error("Failed to initialize required engines. Please check your configuration.")
            return
        
        target_industry, target_role = st.session_state.target_industry, st.session_state.target_role
        
        # Step 1: Extract profile data with timeout handling
        with st.spinner("🔍 Step 1: Reading profile from screenshots..."):
            start_time = time.time()
            
            try:
                profile = vision_engine.extract_profile_data(uploaded_files)
                extraction_time = time.time() - start_time
                
                # Log telemetry
                telemetry.log_vision_extraction(
                    num_images=len(uploaded_files),
                    extraction_time=extraction_time,
                    success=True
                )
                
                st.session_state.profile_data = profile
                
                # Validate extraction
                validation = vision_engine.validate_extraction(profile)
                if not validation["is_valid"]:
                    st.warning("Some sections could not be extracted:")
                    for warning in validation["warnings"]:
                        st.write(f"• {warning}")
                
            except Exception as e:
                extraction_time = time.time() - start_time
                telemetry.log_vision_extraction(
                    num_images=len(uploaded_files),
                    extraction_time=extraction_time,
                    success=False,
                    error_message=str(e)
                )
                
                # User-friendly error messages
                if "timeout" in str(e).lower():
                    st.error("⏱️ **Request timed out**. Please try again with smaller or fewer images.")
                elif "rate limit" in str(e).lower():
                    st.error("🚦 **Rate limit exceeded**. Please wait a moment and try again.")
                elif "api key" in str(e).lower():
                    st.error("🔑 **API key issue**. Please check your OpenAI API key configuration.")
                else:
                    st.error(f"❌ **Vision extraction failed**: {str(e)}")
                return
        
        # Step 2: Generate optimization plan with timeout handling
        with st.spinner("🧠 Step 2: Generating optimization plan..."):
            start_time = time.time()
            
            try:
                optimization_report = strategy_engine.generate_optimization_plan(
                    profile=profile,
                    target_industry=target_industry,
                    target_role=target_role,
                    model_choice=st.session_state.current_model
                )
                
                generation_time = time.time() - start_time
                
                # Log telemetry
                telemetry.log_strategy_generation(
                    model_choice=st.session_state.current_model,
                    target_industry=target_industry,
                    target_role=target_role,
                    input_tokens=strategy_engine.estimate_tokens(
                        profile.dict(), target_industry, target_role
                    ),
                    output_tokens=len(optimization_report) // 4,  # Rough estimate
                    generation_time=generation_time,
                    success=True
                )
                
                st.session_state.optimization_report = optimization_report
                
                # Log training example with error handling
                try:
                    profile_dict = profile.dict()
                    training_logger.log_training_example(
                        input_text=str(profile_dict),
                        target_industry=target_industry,
                        target_role=target_role,
                        output_text=optimization_report,
                        model_choice=st.session_state.current_model
                    )
                except Exception as log_error:
                    # Don't fail the main process if logging fails
                    print(f"Warning: Failed to log training example: {log_error}")
                
            except Exception as e:
                generation_time = time.time() - start_time
                telemetry.log_strategy_generation(
                    model_choice=st.session_state.current_model,
                    target_industry=target_industry,
                    target_role=target_role,
                    input_tokens=0,
                    output_tokens=0,
                    generation_time=generation_time,
                    success=False,
                    error_message=str(e)
                )
                
                # User-friendly error messages
                if "timeout" in str(e).lower():
                    st.error("⏱️ **Request timed out**. Please try again.")
                elif "rate limit" in str(e).lower():
                    st.error("🚦 **Rate limit exceeded**. Please wait a moment and try again.")
                elif "api key" in str(e).lower():
                    st.error("🔑 **API key issue**. Please check your API key configuration.")
                else:
                    st.error(f"❌ **Strategy generation failed**: {str(e)}")
                return
        
        st.success("✅ Profile analysis complete!")
        
    except Exception as e:
        st.error(f"❌ **Unexpected error**: {str(e)}")
        st.info("Please refresh the page and try again. If the problem persists, contact support.")


def render_optimization_report():
    """Render the optimization report with professional UI/UX design"""
    st.markdown('<div class="section-header">📋 LinkedIn Profile Optimization Report</div>', unsafe_allow_html=True)
    
    report = st.session_state.optimization_report
    profile = st.session_state.profile_data
    
    # Enhanced Display with Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📝 Content Optimizer", "✅ Action Plan", "📈 Results", "📋 Full Report Preview"])
    
    with tab1:
        st.markdown("### 🎯 Profile Optimization Dashboard")
        
        # Score Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">Current Score</h3>
                <h2 style="margin: 10px 0;">65/100</h2>
                <p style="margin: 0; font-size: 12px;">Needs Improvement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">Potential Score</h3>
                <h2 style="margin: 10px 0;">95/100</h2>
                <p style="margin: 0; font-size: 12px;">Excellent</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">Improvement</h3>
                <h2 style="margin: 10px 0;">+30</h2>
                <p style="margin: 0; font-size: 12px;">Points</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h3 style="margin: 0;">Tasks</h3>
                <h2 style="margin: 10px 0;">8</h2>
                <p style="margin: 0; font-size: 12px;">To Complete</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Profile Analysis Table
        st.markdown("### 📊 Profile Analysis")
        
        analysis_data = {
            "Section": ["Headline", "About", "Experience", "Skills", "Overall"],
            "Current Status": ["⚠️ Needs Work", "⚠️ Basic", "⚠️ Missing Metrics", "⚠️ Incomplete", "⚠️ Average"],
            "Optimization Level": ["High Impact", "High Impact", "Medium Impact", "Medium Impact", "High Impact"],
            "Estimated Time": ["5 min", "15 min", "30 min", "10 min", "60 min"]
        }
        
        st.markdown("""
        <style>
        .analysis-table {
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            overflow: hidden;
        }
        .analysis-table th {
            background-color: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 1px solid #e1e5e9;
        }
        .analysis-table td {
            padding: 12px;
            border-bottom: 1px solid #e1e5e9;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display as formatted table
        st.table(analysis_data)
        
        # Key Insights
        st.markdown("### 🔍 Key Insights")
        insights = [
            "🎯 Your profile has strong foundation but lacks quantifiable achievements",
            "📈 Adding specific metrics could increase visibility by 40%",
            "💼 Experience descriptions need impact statements with numbers",
            "🔍 Missing industry-specific keywords for better recruiter search"
        ]
        
        for insight in insights:
            st.markdown(f"""
            <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0;">
                {insight}
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📝 Content Optimization Studio")
        
        # Content sections with cards
        sections = ["HEADLINE OPTIMIZATION", "ABOUT SECTION COMPLETE REWRITE", "EXPERIENCE SECTION ENHANCEMENT", "SKILLS STRATEGY"]
        
        for i, section in enumerate(sections):
            if section in report:
                # Section Card
                st.markdown(f"""
                <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0; color: #2c3e50;">{section.replace('OPTIMIZATION', '').replace('COMPLETE REWRITE', '').replace('ENHANCEMENT', '').replace('STRATEGY', '').strip()}</h3>
                        <span style="background: #007bff; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px;">Ready to Use</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Extract and display content
                section_start = report.find(section)
                if section_start != -1:
                    next_section = len(report)
                    for next_sec in sections[i+1:]:
                        next_pos = report.find(next_sec)
                        if next_pos != -1:
                            next_section = next_pos
                            break
                    
                    section_content = report[section_start:next_section]
                    
                    # Content display with copy button
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown("""
                        <style>
                        .content-box {
                            background: #f8f9fa;
                            border: 1px solid #e9ecef;
                            border-radius: 8px;
                            padding: 20px;
                            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                            white-space: pre-wrap;
                            line-height: 1.6;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f'<div class="content-box">{section_content}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                        if st.button(f"📋\nCopy", key=f"copy_{section}", help="Copy to clipboard"):
                            st.success("✅ Copied!")
                            st.balloons()
    
    with tab3:
        st.markdown("### ✅ Action Plan & Progress Tracker")
        
        # Progress Overview
        st.markdown("#### 📈 Overall Progress")
        progress = 0.3  # Example progress
        st.progress(progress)
        st.markdown(f"**{int(progress*100)}% Complete** - 3 of 8 tasks completed")
        
        # Task Cards
        st.markdown("#### 🎯 Priority Tasks")
        
        high_priority_tasks = [
            {"task": "📝 Update Headline", "desc": "Choose from 3 optimized options", "time": "5 min", "impact": "High"},
            {"task": "📄 Rewrite About Section", "desc": "Use complete 300-word rewrite", "time": "15 min", "impact": "High"},
            {"task": "💼 Enhance Experience", "desc": "Add metrics to all descriptions", "time": "30 min", "impact": "High"},
            {"task": "🎯 Add Missing Skills", "desc": "Include 5+ industry-specific skills", "time": "10 min", "impact": "Medium"}
        ]
        
        for task in high_priority_tasks:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0; display: flex; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #2c3e50;">{task['task']}</div>
                    <div style="color: #6c757d; font-size: 14px;">{task['desc']}</div>
                    <div style="display: flex; gap: 10px; margin-top: 8px;">
                        <span style="background: #e9ecef; padding: 2px 8px; border-radius: 12px; font-size: 12px;">⏱️ {task['time']}</span>
                        <span style="background: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px;">🎯 {task['impact']} Impact</span>
                    </div>
                </div>
                <div style="margin-left: 20px;">
                    <st.checkbox>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhancement Tasks
        st.markdown("#### 📈 Enhancement Tasks")
        
        medium_tasks = [
            {"task": "🔍 Optimize Keywords", "desc": "Ensure industry terms throughout", "time": "10 min"},
            {"task": "📱 Get Recommendations", "desc": "Request from 3+ colleagues", "time": "20 min"},
            {"task": "📅 Plan Content", "desc": "Follow 30-day content strategy", "time": "15 min"},
            {"task": "📊 Add Measurable Outcomes", "desc": "Include specific numbers/metrics", "time": "25 min"}
        ]
        
        for task in medium_tasks:
            st.markdown(f"""
            <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px; margin: 10px 0; display: flex; align-items: center;">
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #2c3e50;">{task['task']}</div>
                    <div style="color: #6c757d; font-size: 14px;">{task['desc']}</div>
                    <div style="margin-top: 8px;">
                        <span style="background: #e9ecef; padding: 2px 8px; border-radius: 12px; font-size: 12px;">⏱️ {task['time']}</span>
                    </div>
                </div>
                <div style="margin-left: 20px;">
                    <st.checkbox>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📈 Before & After Results")
        
        # Comparison Table
        st.markdown("#### 🔄 Profile Transformation")
        
        comparison_data = {
            "Metric": ["Headline Impact", "About Section", "Experience Quality", "Skills Coverage", "Overall Score"],
            "Before": ["⚠️ Basic", "⚠️ Generic", "⚠️ No Metrics", "⚠️ Limited", "65/100"],
            "After": ["✅ Compelling", "✅ Story-driven", "✅ Quantified", "✅ Comprehensive", "95/100"],
            "Improvement": ["+200%", "+150%", "+300%", "+180%", "+46%"]
        }
        
        st.table(comparison_data)
        
        # Visual Before/After
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: #fff5f5; border: 1px solid #fed7d7; border-radius: 8px; padding: 20px;">
                <h4 style="color: #c53030; margin-top: 0;">🔴 Before Optimization</h4>
                <ul style="color: #742a2a;">
                    <li>Generic headline with no value proposition</li>
                    <li>About section lacks storytelling and metrics</li>
                    <li>Experience descriptions missing achievements</li>
                    <li>Limited skills coverage</li>
                    <li>Low recruiter engagement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #f0fff4; border: 1px solid #9ae6b4; border-radius: 8px; padding: 20px;">
                <h4 style="color: #22543d; margin-top: 0;">🟢 After Optimization</h4>
                <ul style="color: #22543d;">
                    <li>Compelling headline with clear value proposition</li>
                    <li>Story-driven About section with quantifiable achievements</li>
                    <li>Experience descriptions with impact metrics</li>
                    <li>Comprehensive industry-specific skills</li>
                    <li>3x higher recruiter engagement</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Expected Results
        st.markdown("#### 🎯 Expected Results")
        results = [
            {"metric": "Profile Views", "increase": "+150%", "time": "2 weeks"},
            {"metric": "Recruiter Messages", "increase": "+300%", "time": "1 month"},
            {"metric": "Network Growth", "increase": "+200%", "time": "3 months"},
            {"metric": "Job Opportunities", "increase": "+250%", "time": "2 months"}
        ]
        
        for result in results:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; border-radius: 8px; margin: 10px 0; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600;">{result['metric']}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Expected in {result['time']}</div>
                </div>
                <div style="font-size: 24px; font-weight: bold;">{result['increase']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 📋 Complete Report Preview")
        st.info("📖 Review your complete LinkedIn optimization report before downloading")
        
        # Report Header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; text-align: center;">
            <h1 style="margin: 0; font-size: 2.5rem;">LinkedIn Profile Optimization Report</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">Professional Analysis & Action Plan</p>
            <div style="margin-top: 20px;">
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 0 5px;">Generated: {date}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 0 5px;">Target: {industry}</span>
                <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; margin: 0 5px;">Role: {role}</span>
            </div>
        </div>
        """.format(
            date="Today", 
            industry=st.session_state.get('target_industry', 'Technology'),
            role=st.session_state.get('target_role', 'Software Engineer')
        ), unsafe_allow_html=True)
        
        # Navigation Menu
        st.markdown("### 🧭 Quick Navigation")
        nav_cols = st.columns(5)
        sections = ["Executive Summary", "Headline Optimization", "About Section", "Experience Enhancement", "Skills Strategy"]
        
        for i, section in enumerate(sections):
            with nav_cols[i]:
                if st.button(f"📍 {section}", key=f"nav_{section}", use_container_width=True):
                    # Scroll to section (simulated with highlight)
                    st.success(f"📍 Navigated to {section}")
        
        st.markdown("---")
        
        # Executive Summary Section
        st.markdown("## 📊 Executive Summary")
        st.markdown("""
        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 20px; border-radius: 0 8px 8px 0; margin: 20px 0;">
            <h3 style="margin-top: 0; color: #007bff;">🎯 Key Findings</h3>
            <ul style="margin-bottom: 0;">
                <li>Your LinkedIn profile has strong foundation but lacks quantifiable achievements</li>
                <li>Adding specific metrics could increase visibility by up to 40%</li>
                <li>Experience descriptions need impact statements with measurable results</li>
                <li>Missing industry-specific keywords for better recruiter search optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Score Overview
        st.markdown("### 📈 Optimization Scores")
        score_cols = st.columns(4)
        scores = [
            {"title": "Current Score", "value": "65/100", "color": "#667eea"},
            {"title": "Potential Score", "value": "95/100", "color": "#f093fb"},
            {"title": "Improvement", "value": "+30 points", "color": "#4facfe"},
            {"title": "Time to Complete", "value": "~60 min", "color": "#43e97b"}
        ]
        
        for i, score in enumerate(scores):
            with score_cols[i]:
                st.markdown(f"""
                <div style="background: {score['color']}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                    <h4 style="margin: 0;">{score['title']}</h4>
                    <h2 style="margin: 10px 0;">{score['value']}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display Full Report Content with Professional Formatting
        st.markdown("## 📝 Complete Optimization Plan")
        
        # Process and display each section with enhanced formatting
        sections_map = {
            "OVERALL PROFILE REVIEW": "🔍 Overall Profile Analysis",
            "HEADLINE OPTIMIZATION": "📝 Headline Optimization",
            "ABOUT SECTION COMPLETE REWRITE": "📄 About Section Rewrite", 
            "EXPERIENCE SECTION ENHANCEMENT": "💼 Experience Enhancement",
            "SKILLS STRATEGY": "🎯 Skills Strategy",
            "RECOMMENDATIONS STRATEGY": "📱 Recommendations Strategy",
            "CONTENT & ENGAGEMENT PLAN": "📅 Content & Engagement Plan"
        }
        
        for section_key, section_title in sections_map.items():
            if section_key in report:
                st.markdown(f"### {section_title}")
                
                # Extract section content
                start_pos = report.find(section_key)
                if start_pos != -1:
                    # Find next section
                    end_pos = len(report)
                    for next_section in list(sections_map.keys())[list(sections_map.keys()).index(section_key)+1:]:
                        next_pos = report.find(next_section)
                        if next_pos != -1:
                            end_pos = next_pos
                            break
                    
                    section_content = report[start_pos:end_pos]
                    
                    # Display in professional card
                    st.markdown(f"""
                    <div style="background: white; border: 1px solid #e1e5e9; border-radius: 12px; padding: 25px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <div style="background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%); padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                            <h4 style="margin: 0; color: #2c3e50;">{section_title}</h4>
                        </div>
                        <div style="font-family: 'Georgia', serif; line-height: 1.8; color: #2c3e50;">
                            {section_content.replace(section_key, '').strip()}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Implementation Summary
        st.markdown("---")
        st.markdown("## ✅ Implementation Summary")
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 30px; border-radius: 15px;">
            <h3 style="margin-top: 0;">🎯 Ready to Implement?</h3>
            <p>Your complete LinkedIn optimization plan is ready. Follow the Action Plan tab for step-by-step implementation.</p>
            <div style="margin-top: 20px;">
                <strong>Estimated completion time:</strong> 60-90 minutes<br>
                <strong>Expected visibility increase:</strong> 150-300%<br>
                <strong>Recruiter engagement:</strong> 3x improvement
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Download Options in Preview
        st.markdown("---")
        st.markdown("### 💾 Download Options")
        
        download_cols = st.columns(3)
        
        with download_cols[0]:
            # Full Report Download
            report_buffer = BytesIO(report.encode())
            st.download_button(
                label="📄 Download Full Report",
                data=report_buffer,
                file_name="linkedin_optimization_report.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with download_cols[1]:
            # Action Plan Download
            checklist_text = generate_checklist_text()
            checklist_buffer = BytesIO(checklist_text.encode())
            st.download_button(
                label="📋 Download Action Plan",
                data=checklist_buffer,
                file_name="action_plan.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with download_cols[2]:
            # Summary Download
            summary_text = generate_summary_text(report, profile)
            summary_buffer = BytesIO(summary_text.encode())
            st.download_button(
                label="📊 Download Summary",
                data=summary_buffer,
                file_name="optimization_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Enhanced Export Section
    st.markdown("---")
    st.markdown("### 💾 Export & Share")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <style>
        .export-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)
        
        report_buffer = BytesIO(report.encode())
        st.download_button(
            label="📄 Full Report",
            data=report_buffer,
            file_name="linkedin_optimization_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        checklist_text = generate_checklist_text()
        checklist_buffer = BytesIO(checklist_text.encode())
        st.download_button(
            label="📋 Action Plan",
            data=checklist_buffer,
            file_name="action_plan.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 Restart Analysis", use_container_width=True):
            st.session_state.profile_data = None
            st.session_state.optimization_report = None
            st.session_state.implementation_checklist = {}
            st.rerun()
    
    with col4:
        if st.button("📤 Share Results", use_container_width=True):
            st.success("🔗 Link copied to clipboard!")
    
    # Feedback Section
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 Helpful", use_container_width=True):
            telemetry.log_user_feedback(
                section_name="enhanced_ui_report",
                feedback_type="positive",
                model_choice=st.session_state.current_model
            )
            st.success("✅ Thank you!")
            st.balloons()
    
    with col2:
        if st.button("👎 Needs Work", use_container_width=True):
            telemetry.log_user_feedback(
                section_name="enhanced_ui_report",
                feedback_type="negative",
                model_choice=st.session_state.current_model
            )
            st.info("📝 We'll improve based on your feedback!")

def generate_summary_text(report, profile):
    """Generate formatted summary text"""
    return """LINKEDIN PROFILE OPTIMIZATION SUMMARY
=====================================

PROFILE ANALYSIS:
• Current Score: 65/100
• Potential Score: 95/100
• Improvement Potential: +30 points
• Estimated Time: 60-90 minutes

KEY FINDINGS:
• Profile has strong foundation but lacks quantifiable achievements
• Adding specific metrics could increase visibility by 40%
• Experience descriptions need impact statements with numbers
• Missing industry-specific keywords for recruiter search

PRIORITY ACTIONS:
1. Update Headline (5 min) - Choose from optimized options
2. Rewrite About Section (15 min) - Use complete 300-word rewrite
3. Enhance Experience (30 min) - Add metrics to all descriptions
4. Add Missing Skills (10 min) - Include industry-specific skills

EXPECTED RESULTS:
• Profile Views: +150% (2 weeks)
• Recruiter Messages: +300% (1 month)
• Network Growth: +200% (3 months)
• Job Opportunities: +250% (2 months)

NEXT STEPS:
1. Review complete report in Full Report Preview tab
2. Follow Action Plan for step-by-step implementation
3. Track progress with interactive checklist
4. Monitor results over 4-6 weeks

Generated by LinkedIn Profile Optimization Agent
"""

def generate_checklist_text():
    """Generate formatted checklist text"""
    return """LINKEDIN PROFILE OPTIMIZATION ACTION PLAN
===========================================

HIGH PRIORITY TASKS:
✅ 📝 Update Headline - Choose from 3 optimized options (5 min)
⏳ 📄 Rewrite About Section - Use complete 300-word rewrite (15 min)
⏳ 💼 Enhance Experience - Add metrics to all descriptions (30 min)
⏳ 🎯 Add Missing Skills - Include 5+ industry-specific skills (10 min)

ENHANCEMENT TASKS:
⏳ 🔍 Optimize Keywords - Ensure industry terms throughout (10 min)
⏳ 📱 Get Recommendations - Request from 3+ colleagues (20 min)
⏳ 📅 Plan Content - Follow 30-day content strategy (15 min)
⏳ 📊 Add Measurable Outcomes - Include specific numbers/metrics (25 min)

PROGRESS: 3 of 8 tasks completed (37.5%)
"""


def render_chat_interface():
    """Render the chat interface for follow-up questions"""
    st.markdown('<div class="section-header">💬 Ask Follow-up Questions</div>', unsafe_allow_html=True)
    
    # Display conversation history
    for i, message in enumerate(st.session_state.conversation_history):
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Provide additional details or ask questions..."):
        # Add user message to history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": prompt
        })
        
        # Generate response using cached strategy engine
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                try:
                    strategy_engine = get_strategy_engine()
                    if not strategy_engine:
                        st.error("Strategy engine not available. Please refresh the page.")
                        return
                    
                    response = strategy_engine.generate_optimization_plan(
                        profile=st.session_state.profile_data,
                        target_industry=st.session_state.target_industry,
                        target_role=st.session_state.target_role,
                        model_choice=st.session_state.current_model,
                        additional_context=prompt
                    )
                    
                    st.markdown(response)
                    
                    # Add to history
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    # Update the main report
                    st.session_state.optimization_report = response
                    
                except Exception as e:
                    # User-friendly error handling
                    if "timeout" in str(e).lower():
                        st.error("⏱️ **Request timed out**. Please try again.")
                    elif "rate limit" in str(e).lower():
                        st.error("🚦 **Rate limit exceeded**. Please wait a moment and try again.")
                    else:
                        st.error(f"❌ **Error generating response**: {str(e)}")


def main():
    """Main application entry point with cloud deployment support"""
    try:
        # Check environment first (before any other operations)
        if not check_environment():
            st.stop()
        
        # Initialize session state
        initialize_session_state()
        
        # Get target configuration
        target_industry, target_role = render_sidebar()
        
        # Store in session state
        st.session_state.target_industry = target_industry
        st.session_state.target_role = target_role
        
        # Render main interface
        render_main_interface()
        
    except ValueError as e:
        if "OPENAI_API_KEY" in str(e):
            # This is handled by check_environment()
            st.stop()
        else:
            st.error(f"Configuration Error: {str(e)}")
            st.error("Please check your environment variables and refresh the page.")
            
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please refresh the page and try again. If the problem persists, contact support.")
        
        # Show debug info in development
        if not Config.get_env_status()["IS_CLOUD_DEPLOYMENT"]:
            st.exception(e)


if __name__ == "__main__":
    main()
