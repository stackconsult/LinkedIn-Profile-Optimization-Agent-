"""
LinkedIn Profile Optimization Agent
A Streamlit application that analyzes and optimizes LinkedIn profiles
based on best practices for attracting clients or job opportunities.
"""

import streamlit as st
import os
from typing import Dict, List, Optional
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Optimizer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0077B5;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #0077B5;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .recommendation-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0077B5;
        margin-bottom: 1rem;
    }
    .metric-box {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


class LinkedInOptimizer:
    """Main class for LinkedIn profile optimization"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def analyze_headline(self, headline: str, target: str) -> Dict:
        """Analyze LinkedIn headline and provide recommendations"""
        if not self.api_key:
            return {
                "score": 0,
                "feedback": "Please configure your OpenAI API key in the environment variables.",
                "suggestions": []
            }
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a LinkedIn profile optimization expert. Analyze the headline and provide specific, actionable feedback."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this LinkedIn headline for someone targeting {target}: '{headline}'. Provide a score out of 10, specific feedback, and 3 concrete suggestions for improvement. Format your response as: SCORE: X/10\nFEEDBACK: (your feedback)\nSUGGESTIONS:\n1. (suggestion)\n2. (suggestion)\n3. (suggestion)"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_analysis(content)
            
        except Exception as e:
            return {
                "score": 0,
                "feedback": f"Error analyzing headline: {str(e)}",
                "suggestions": ["Please check your API key and try again."]
            }
    
    def analyze_about_section(self, about: str, target: str) -> Dict:
        """Analyze LinkedIn About section and provide recommendations"""
        if not self.api_key:
            return {
                "score": 0,
                "feedback": "Please configure your OpenAI API key in the environment variables.",
                "suggestions": []
            }
        
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a LinkedIn profile optimization expert. Analyze the About section and provide specific, actionable feedback."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this LinkedIn About section for someone targeting {target}: '{about}'. Provide a score out of 10, specific feedback, and 3 concrete suggestions for improvement. Format your response as: SCORE: X/10\nFEEDBACK: (your feedback)\nSUGGESTIONS:\n1. (suggestion)\n2. (suggestion)\n3. (suggestion)"
                    }
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return self._parse_analysis(content)
            
        except Exception as e:
            return {
                "score": 0,
                "feedback": f"Error analyzing About section: {str(e)}",
                "suggestions": ["Please check your API key and try again."]
            }
    
    def _parse_analysis(self, content: str) -> Dict:
        """Parse the analysis response from OpenAI"""
        try:
            lines = content.split('\n')
            score = 0
            feedback = ""
            suggestions = []
            
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith("SCORE:"):
                    score_text = line.replace("SCORE:", "").strip()
                    score = int(score_text.split('/')[0].strip())
                elif line.startswith("FEEDBACK:"):
                    feedback = line.replace("FEEDBACK:", "").strip()
                    current_section = "feedback"
                elif line.startswith("SUGGESTIONS:"):
                    current_section = "suggestions"
                elif current_section == "feedback" and line and not line.startswith(("1.", "2.", "3.")):
                    feedback += " " + line
                elif current_section == "suggestions" and line:
                    if line[0].isdigit() and '.' in line[:3]:
                        suggestions.append(line.split('.', 1)[1].strip())
            
            return {
                "score": score,
                "feedback": feedback.strip(),
                "suggestions": suggestions
            }
        except Exception as e:
            return {
                "score": 0,
                "feedback": content,
                "suggestions": ["Unable to parse suggestions from response"]
            }


def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">💼 LinkedIn Profile Optimizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyze and optimize your LinkedIn profile based on best practices</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key to enable AI-powered analysis"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your OpenAI API Key")
        
        st.markdown("---")
        
        # Target selection
        st.header("🎯 Optimization Target")
        target = st.selectbox(
            "I'm optimizing my profile to attract:",
            [
                "Job Opportunities",
                "Client Projects",
                "Business Partnerships",
                "Investors",
                "Speaking Engagements",
                "Consulting Opportunities"
            ]
        )
        
        st.markdown("---")
        
        # Information
        st.header("ℹ️ About")
        st.info(
            "This tool uses AI to analyze your LinkedIn profile and provide "
            "personalized recommendations to help you achieve your professional goals."
        )
    
    # Main content
    optimizer = LinkedInOptimizer()
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 Headline", "👤 About Section", "📊 Overall Score"])
    
    with tab1:
        st.markdown('<div class="section-header">Analyze Your Headline</div>', unsafe_allow_html=True)
        st.write("Your headline is the first thing people see. Make it count!")
        
        headline = st.text_input(
            "Current Headline",
            placeholder="e.g., Software Engineer | Python Developer | Open Source Contributor",
            max_chars=220
        )
        
        if headline and st.button("Analyze Headline", key="analyze_headline"):
            with st.spinner("Analyzing your headline..."):
                results = optimizer.analyze_headline(headline, target)
                
                # Display score
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                    st.metric("Score", f"{results['score']}/10")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Display feedback
                st.markdown('<div class="section-header">Feedback</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="recommendation-box">{results["feedback"]}</div>', unsafe_allow_html=True)
                
                # Display suggestions
                if results['suggestions']:
                    st.markdown('<div class="section-header">Suggestions for Improvement</div>', unsafe_allow_html=True)
                    for i, suggestion in enumerate(results['suggestions'], 1):
                        st.markdown(f'<div class="recommendation-box">**{i}.** {suggestion}</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-header">Analyze Your About Section</div>', unsafe_allow_html=True)
        st.write("Your About section tells your story. Make it compelling!")
        
        about = st.text_area(
            "Current About Section",
            placeholder="Enter your current LinkedIn About section here...",
            height=200,
            max_chars=2600
        )
        
        if about and st.button("Analyze About Section", key="analyze_about"):
            with st.spinner("Analyzing your About section..."):
                results = optimizer.analyze_about_section(about, target)
                
                # Display score
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                    st.metric("Score", f"{results['score']}/10")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Display feedback
                st.markdown('<div class="section-header">Feedback</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="recommendation-box">{results["feedback"]}</div>', unsafe_allow_html=True)
                
                # Display suggestions
                if results['suggestions']:
                    st.markdown('<div class="section-header">Suggestions for Improvement</div>', unsafe_allow_html=True)
                    for i, suggestion in enumerate(results['suggestions'], 1):
                        st.markdown(f'<div class="recommendation-box">**{i}.** {suggestion}</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-header">Profile Optimization Tips</div>', unsafe_allow_html=True)
        
        st.write("### General Best Practices for LinkedIn Profiles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Profile Completeness
            - ✅ Professional profile photo
            - ✅ Custom background banner
            - ✅ Compelling headline
            - ✅ Detailed About section
            - ✅ Complete work experience
            - ✅ Education history
            - ✅ Skills (at least 5)
            - ✅ Recommendations
            """)
            
            st.markdown("""
            #### Content Strategy
            - 📝 Post regularly (2-3 times per week)
            - 💬 Engage with others' content
            - 🔗 Share valuable insights
            - 📊 Use relevant hashtags
            - 🎯 Focus on your niche
            """)
        
        with col2:
            st.markdown("""
            #### Headline Tips
            - Use keywords relevant to your field
            - Highlight your unique value proposition
            - Include your target audience
            - Keep it under 220 characters
            - Avoid buzzwords without substance
            """)
            
            st.markdown("""
            #### About Section Tips
            - Start with a hook
            - Tell your professional story
            - Highlight achievements with numbers
            - Include a clear call-to-action
            - Make it scannable with line breaks
            - Show personality while staying professional
            """)
        
        st.markdown("---")
        st.info(
            "💡 **Pro Tip**: Consistency is key! Update your profile regularly and "
            "engage with your network to maximize visibility."
        )


if __name__ == "__main__":
    main()
