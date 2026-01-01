"""
Prompt formatter for different model types (GPT-4o vs Llama 3)
"""

from typing import List, Dict, Any
from .config import Config


class PromptFormatter:
    """Formats prompts for different model types"""
    
    @staticmethod
    def format_for_gpt(system_prompt: str, user_content: str) -> List[Dict[str, str]]:
        """
        Format prompts for OpenAI GPT models.
        
        Args:
            system_prompt: System prompt content
            user_content: User prompt content
            
        Returns:
            List of message dictionaries for OpenAI API
        """
        return [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_content
            }
        ]
    
    @staticmethod
    def format_for_llama3(system_prompt: str, user_content: str) -> str:
        """
        Format prompts for Llama 3 Instruct models.
        
        Args:
            system_prompt: System prompt content
            user_content: User prompt content
            
        Returns:
            Formatted string for Llama 3 Instruct
        """
        # Llama 3 Instruct format
        formatted_prompt = (
            "<|begin_of_text|>"
            "<|start_header_id|>system<|end_header_id|>\n"
            f"{system_prompt}"
            "<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"{user_content}"
            "<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>"
        )
        return formatted_prompt
    
    @staticmethod
    def format_for_model(model_choice: str, system_prompt: str, user_content: str):
        """
        Format prompts based on model choice.
        
        Args:
            model_choice: Either "gpt4o" or "llama3_custom"
            system_prompt: System prompt content
            user_content: User prompt content
            
        Returns:
            Formatted prompt appropriate for the selected model
        """
        if model_choice == "gpt4o":
            return PromptFormatter.format_for_gpt(system_prompt, user_content)
        elif model_choice == "llama3_custom":
            return PromptFormatter.format_for_llama3(system_prompt, user_content)
        else:
            raise ValueError(f"Unknown model choice: {model_choice}")
    
    @staticmethod
    def get_model_id(model_choice: str) -> str:
        """
        Get the actual model ID for the given choice.
        
        Args:
            model_choice: Either "gpt4o" or "llama3_custom"
            
        Returns:
            Model ID string
        """
        if model_choice == "gpt4o":
            return Config.GPT4O_MODEL_ID
        elif model_choice == "llama3_custom":
            if not Config.has_custom_llama3():
                raise ValueError("Custom Llama 3 model not available")
            return Config.CUSTOM_LLAMA3_MODEL_ID
        else:
            raise ValueError(f"Unknown model choice: {model_choice}")
    
    @staticmethod
    def is_text_only_model(model_choice: str) -> bool:
        """
        Check if the model is text-only (no vision capabilities).
        
        Args:
            model_choice: Model choice string
            
        Returns:
            True if model is text-only, False if it has vision capabilities
        """
        # All strategist models are text-only
        return True
