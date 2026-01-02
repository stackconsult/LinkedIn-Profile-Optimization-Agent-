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
    """Render the optimization report with feedback options"""
    st.markdown('<div class="section-header">📋 Optimization Report</div>', unsafe_allow_html=True)
    
    report = st.session_state.optimization_report
    
    # Display the report
    st.markdown(report)
    
    # Implementation Checklist
    st.markdown('<div class="section-header">✅ Implementation Checklist</div>', unsafe_allow_html=True)
    st.info("📝 Track your progress as you implement the optimization recommendations")
    
    # Initialize checklist in session state if not exists
    if 'implementation_checklist' not in st.session_state:
        st.session_state.implementation_checklist = {}
    
    # Create default checklist items based on common optimization tasks
    default_checklist = {
        "📝 Update Headline": "Choose and implement one of the recommended headlines",
        "📄 Rewrite About Section": "Use the complete About section rewrite provided",
        "💼 Enhance Experience Descriptions": "Update all job descriptions with quantifiable achievements",
        "🎯 Add Missing Skills": "Include all recommended skills for your target role",
        "📊 Add Measurable Outcomes": "Include specific numbers, percentages, and metrics",
        "🔍 Optimize Keywords": "Ensure industry-specific keywords are included throughout",
        "📱 Get Recommendations": "Request recommendations from managers and colleagues",
        "📅 Plan Content Strategy": "Follow the 30-day content and engagement plan"
    }
    
    # Initialize checklist items
    for item, description in default_checklist.items():
        if item not in st.session_state.implementation_checklist:
            st.session_state.implementation_checklist[item] = {
                "completed": False,
                "description": description,
                "notes": ""
            }
    
    # Display interactive checklist
    completed_count = 0
    total_count = len(st.session_state.implementation_checklist)
    
    for item, details in st.session_state.implementation_checklist.items():
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        
        with col1:
            completed = st.checkbox(
                "", 
                value=details["completed"],
                key=f"check_{item}"
            )
            if completed != details["completed"]:
                st.session_state.implementation_checklist[item]["completed"] = completed
                if completed:
                    completed_count += 1
                else:
                    completed_count -= 1
        
        with col2:
            st.markdown(f"**{item}**")
            st.caption(details["description"])
        
        with col3:
            if details["completed"]:
                st.success("✅")
            else:
                st.info("⏳")
    
    # Progress bar
    current_completed = sum(1 for details in st.session_state.implementation_checklist.values() if details["completed"])
    progress = current_completed / total_count
    
    st.markdown("### 📈 Overall Progress")
    st.progress(progress)
    st.write(f"Completed: {current_completed}/{total_count} tasks ({progress:.1%})")
    
    # Export checklist
    st.markdown("### 📋 Export Your Checklist")
    
    checklist_text = "LINKEDIN PROFILE OPTIMIZATION CHECKLIST\n" + "="*50 + "\n\n"
    
    for item, details in st.session_state.implementation_checklist.items():
        status = "✅ COMPLETED" if details["completed"] else "⏳ PENDING"
        checklist_text += f"{status} - {item}\n"
        checklist_text += f"   {details['description']}\n\n"
    
    checklist_buffer = BytesIO(checklist_text.encode())
    st.download_button(
        label="📄 Download Checklist",
        data=checklist_buffer,
        file_name="linkedin_optimization_checklist.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Feedback section
    st.markdown('<div class="section-header">👍 Feedback</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 This was helpful", use_container_width=True):
            # Log positive feedback
            telemetry.log_user_feedback(
                section_name="overall_report",
                feedback_type="positive",
                model_choice=st.session_state.current_model
            )
            st.success("Thank you for your feedback!")
    
    with col2:
        if st.button("👎 Not helpful", use_container_width=True):
            # Log negative feedback
            telemetry.log_user_feedback(
                section_name="overall_report",
                feedback_type="negative",
                model_choice=st.session_state.current_model
            )
            st.info("Thank you - we'll use this to improve!")
    
    # Download buttons - cloud-friendly with in-memory buffers
    st.markdown('<div class="section-header">💾 Export Options</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # In-memory download without relying on filesystem
        text_buffer = BytesIO(report.encode())
        st.download_button(
            label="📄 Download Report",
            data=text_buffer,
            file_name="linkedin_optimization_report.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        if st.button("🗑️ Clear Session", use_container_width=True):
            # Clear session state
            st.session_state.profile_data = None
            st.session_state.optimization_report = None
            st.session_state.conversation_history = []
            st.rerun()


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
