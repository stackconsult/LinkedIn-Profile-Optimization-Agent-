"""
Strategy engine for LinkedIn profile optimization
"""

import json
from typing import Dict, Any, Optional
from openai import OpenAI

# Optional together library
try:
    import together
    TOGETHER_AVAILABLE = True
except ImportError:
    TOGETHER_AVAILABLE = False

from .config import Config
from .prompt_templates import get_system_prompt, format_profile_for_prompt, format_followup_content
from .prompt_formatter import PromptFormatter
from .vision_engine import LinkedInProfile


class StrategyEngine:
    """Engine for generating LinkedIn profile optimization strategies"""
    
    def __init__(self):
        """Initialize the strategy engine"""
        self.openai_client = None
        self.together_client = None
        
        # Initialize OpenAI client
        if Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        # Initialize Together client (optional)
        if Config.TOGETHER_API_KEY and TOGETHER_AVAILABLE:
            together.api_key = Config.TOGETHER_API_KEY
            self.together_client = together
    
    def _call_openai_model(self, messages: list, model_id: str) -> str:
        """Call OpenAI model (GPT-4o)"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        response = self.openai_client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _call_together_model(self, prompt: str, model_id: str) -> str:
        """Call Together AI model (Llama 3)"""
        if not TOGETHER_AVAILABLE:
            raise ImportError("Together library not available. Install with: pip install together")
        
        if not self.together_client:
            raise ValueError("Together client not initialized")
        
        response = self.together_client.Complete.create(
            model=model_id,
            prompt=prompt,
            max_tokens=4000,
            temperature=0.7,
            stop=["<|eot_id|>"]
        )
        
        return response['choices'][0]['text']
    
    def _generate_strategy(
        self, 
        profile_data: Dict[str, Any], 
        target_industry: str, 
        target_role: str,
        model_choice: str,
        additional_context: Optional[str] = None
    ) -> str:
        """
        Generate optimization strategy using the specified model.
        
        Args:
            profile_data: Profile data from vision engine
            target_industry: Target industry
            target_role: Target role
            model_choice: Either "gpt4o" or "llama3_custom"
            additional_context: Optional additional context from user
            
        Returns:
            Optimization strategy as markdown string
        """
        # Get system prompt
        system_prompt = get_system_prompt(target_industry, target_role)
        
        # Get user content
        if additional_context:
            user_content = format_followup_content(additional_context)
        else:
            user_content = format_profile_for_prompt(profile_data, target_industry, target_role)
        
        # Format for specific model
        formatted_prompt = PromptFormatter.format_for_model(
            model_choice, system_prompt, user_content
        )
        
        # Get model ID
        model_id = PromptFormatter.get_model_id(model_choice)
        
        # Call appropriate model
        if model_choice == "gpt4o":
            response = self._call_openai_model(formatted_prompt, model_id)
        elif model_choice == "llama3_custom":
            response = self._call_together_model(formatted_prompt, model_id)
        else:
            raise ValueError(f"Unknown model choice: {model_choice}")
        
        return response
    
    def generate_optimization_plan(
        self,
        profile: LinkedInProfile,
        target_industry: str,
        target_role: str,
        model_choice: str = "gpt4o",
        additional_context: Optional[str] = None
    ) -> str:
        """
        Generate a complete optimization plan for a LinkedIn profile.
        
        Args:
            profile: LinkedInProfile object from vision engine
            target_industry: Target industry
            target_role: Target role
            model_choice: Model to use for generation
            additional_context: Optional additional context
            
        Returns:
            Complete optimization plan as markdown
        """
        # Convert profile to dict
        profile_data = {
            "headline": profile.headline,
            "about": profile.about,
            "experience": [
                {
                    "title": exp.title,
                    "company": exp.company,
                    "dates": exp.dates,
                    "description": exp.description
                }
                for exp in profile.experience
            ],
            "skills": profile.skills
        }
        
        # Generate strategy
        strategy = self._generate_strategy(
            profile_data, target_industry, target_role, model_choice, additional_context
        )
        
        return strategy
    
    def validate_model_availability(self, model_choice: str) -> bool:
        """
        Check if the specified model is available.
        
        Args:
            model_choice: Model choice to validate
            
        Returns:
            True if model is available, False otherwise
        """
        if model_choice == "gpt4o":
            return bool(self.openai_client)
        elif model_choice == "llama3_custom":
            return bool(self.together_client) and Config.has_custom_llama3()
        else:
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available models.
        
        Returns:
            List of available model choices
        """
        available = []
        
        if self.openai_client:
            available.append("gpt4o")
        
        if self.together_client and Config.has_custom_llama3():
            available.append("llama3_custom")
        
        return available
    
    def estimate_tokens(self, profile_data: Dict[str, Any], target_industry: str, target_role: str) -> int:
        """
        Estimate token count for the request.
        
        Args:
            profile_data: Profile data
            target_industry: Target industry
            target_role: Target role
            
        Returns:
            Estimated token count
        """
        # Rough estimation: 1 token ≈ 4 characters
        user_content = format_profile_for_prompt(profile_data, target_industry, target_role)
        system_prompt = get_system_prompt(target_industry, target_role)
        
        total_text = user_content + system_prompt
        estimated_tokens = len(total_text) // 4
        
        return estimated_tokens
