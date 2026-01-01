"""
Training data logger for fine-tuning dataset collection
Cloud-optimized for Streamlit Community Cloud deployment
"""

import json
import os
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime

from .config import Config


class TrainingLogger:
    """Logger for collecting training examples for fine-tuning"""
    
    def __init__(self, dataset_path: Optional[str] = None):
        """
        Initialize training logger.
        
        Args:
            dataset_path: Path to the training dataset file (uses Config.TRAINING_DATA_PATH if not provided)
        """
        self.dataset_path = dataset_path or Config.TRAINING_DATA_PATH
        self._ensure_dataset_file()
    
    def _ensure_dataset_file(self):
        """Ensure the dataset file exists - cloud-friendly with error handling"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
            
            if not os.path.exists(self.dataset_path):
                # Create empty dataset file
                with open(self.dataset_path, 'w') as f:
                    f.write("")  # Start with empty file
        except Exception as e:
            # Fallback to temporary directory if original path fails
            temp_path = os.path.join(tempfile.gettempdir(), "training_dataset.jsonl")
            self.dataset_path = temp_path
            try:
                with open(self.dataset_path, 'w') as f:
                    f.write("")
            except Exception as fallback_error:
                print(f"Warning: Could not create training dataset file: {fallback_error}")
                self.dataset_path = None
    
    def _read_existing_examples(self) -> list:
        """Read existing examples from the dataset file"""
        examples = []
        
        if os.path.exists(self.dataset_path):
            try:
                with open(self.dataset_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        # Read line by line for JSONL format
                        for line in content.split('\n'):
                            if line.strip():
                                examples.append(json.loads(line))
            except Exception as e:
                print(f"Warning: Could not read existing examples: {e}")
        
        return examples
    
    def log_training_example(
        self,
        input_text: str,
        target_industry: str,
        target_role: str,
        output_text: str,
        model_choice: str,
        feedback_score: Optional[str] = None,  # "positive", "negative", or None
        additional_context: Optional[str] = None
    ) -> bool:
        """
        Log a training example to the dataset.
        
        Args:
            input_text: The input prompt (profile data + context)
            target_industry: Target industry
            target_role: Target role
            output_text: The generated optimization plan
            model_choice: Model that generated the output
            feedback_score: User feedback on the quality
            additional_context: Any additional context provided
            
        Returns:
            True if logging was successful, False otherwise
        """
        if not self.dataset_path:
            print("Warning: No valid dataset path available for logging")
            return False
            
        try:
            # Create training example
            example = {
                "timestamp": datetime.utcnow().isoformat(),
                "input": {
                    "profile_data": input_text,
                    "target_industry": target_industry,
                    "target_role": target_role,
                    "additional_context": additional_context
                },
                "output": output_text,
                "metadata": {
                    "model_choice": model_choice,
                    "feedback_score": feedback_score,
                    "input_length": len(input_text),
                    "output_length": len(output_text)
                }
            }
            
            # Append to dataset file (JSONL format)
            with open(self.dataset_path, 'a') as f:
                f.write(json.dumps(example) + '\n')
            
            return True
            
        except Exception as e:
            print(f"Failed to log training example: {e}")
            return False
    
    def log_section_feedback(
        self,
        section_name: str,
        current_text: str,
        recommended_text: str,
        target_industry: str,
        target_role: str,
        feedback_type: str,  # "positive" or "negative"
        model_choice: str
    ) -> bool:
        """
        Log feedback on a specific section for fine-tuning.
        
        Args:
            section_name: Name of the section (headline, about, etc.)
            current_text: Original text
            recommended_text: Recommended text
            target_industry: Target industry
            target_role: Target role
            feedback_type: Type of feedback
            model_choice: Model that generated the recommendation
            
        Returns:
            True if logging was successful, False otherwise
        """
        if not self.dataset_path:
            print("Warning: No valid dataset path available for logging")
            return False
            
        try:
            # Create section-specific training example
            example = {
                "timestamp": datetime.utcnow().isoformat(),
                "type": "section_optimization",
                "input": {
                    "section_name": section_name,
                    "current_text": current_text,
                    "target_industry": target_industry,
                    "target_role": target_role
                },
                "output": recommended_text,
                "metadata": {
                    "model_choice": model_choice,
                    "feedback_type": feedback_type,
                    "input_length": len(current_text),
                    "output_length": len(recommended_text)
                }
            }
            
            # Append to dataset file
            with open(self.dataset_path, 'a') as f:
                f.write(json.dumps(example) + '\n')
            
            return True
            
        except Exception as e:
            print(f"Failed to log section feedback: {e}")
            return False
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the training dataset.
        
        Returns:
            Dictionary with dataset statistics
        """
        examples = self._read_existing_examples()
        
        stats = {
            "total_examples": len(examples),
            "positive_examples": 0,
            "negative_examples": 0,
            "neutral_examples": 0,
            "sections": {},
            "industries": {},
            "roles": {},
            "models": {},
            "avg_input_length": 0,
            "avg_output_length": 0
        }
        
        total_input_length = 0
        total_output_length = 0
        
        for example in examples:
            # Feedback distribution
            feedback = example.get("metadata", {}).get("feedback_score")
            if feedback == "positive":
                stats["positive_examples"] += 1
            elif feedback == "negative":
                stats["negative_examples"] += 1
            else:
                stats["neutral_examples"] += 1
            
            # Section distribution (for section-specific examples)
            if example.get("type") == "section_optimization":
                section = example.get("input", {}).get("section_name", "unknown")
                stats["sections"][section] = stats["sections"].get(section, 0) + 1
            
            # Industry distribution
            industry = example.get("input", {}).get("target_industry", "unknown")
            stats["industries"][industry] = stats["industries"].get(industry, 0) + 1
            
            # Role distribution
            role = example.get("input", {}).get("target_role", "unknown")
            stats["roles"][role] = stats["roles"].get(role, 0) + 1
            
            # Model distribution
            model = example.get("metadata", {}).get("model_choice", "unknown")
            stats["models"][model] = stats["models"].get(model, 0) + 1
            
            # Length statistics
            input_len = example.get("metadata", {}).get("input_length", 0)
            output_len = example.get("metadata", {}).get("output_length", 0)
            total_input_length += input_len
            total_output_length += output_len
        
        # Calculate averages
        if len(examples) > 0:
            stats["avg_input_length"] = total_input_length / len(examples)
            stats["avg_output_length"] = total_output_length / len(examples)
        
        return stats
    
    def export_clean_dataset(self, output_path: str, min_quality: str = "neutral") -> bool:
        """
        Export a clean dataset for fine-tuning.
        
        Args:
            output_path: Path to save the clean dataset
            min_quality: Minimum quality level to include ("positive", "neutral", "negative")
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            examples = self._read_existing_examples()
            clean_examples = []
            
            # Filter by quality
            quality_order = {"positive": 3, "neutral": 2, "negative": 1}
            min_score = quality_order.get(min_quality, 2)
            
            for example in examples:
                feedback = example.get("metadata", {}).get("feedback_score", "neutral")
                score = quality_order.get(feedback, 2)
                
                if score >= min_score:
                    # Create clean example for fine-tuning
                    clean_example = {
                        "input": example["input"],
                        "output": example["output"]
                    }
                    clean_examples.append(clean_example)
            
            # Write clean dataset
            with open(output_path, 'w') as f:
                for example in clean_examples:
                    f.write(json.dumps(example) + '\n')
            
            print(f"Exported {len(clean_examples)} examples to {output_path}")
            return True
            
        except Exception as e:
            print(f"Failed to export clean dataset: {e}")
            return False
    
    def clear_dataset(self) -> bool:
        """
        Clear the training dataset.
        
        Returns:
            True if clearing was successful, False otherwise
        """
        if not self.dataset_path:
            print("Warning: No valid dataset path available")
            return False
            
        try:
            with open(self.dataset_path, 'w') as f:
                f.write("")
            return True
        except Exception as e:
            print(f"Failed to clear dataset: {e}")
            return False
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the dataset for cloud UI display.
        
        Returns:
            Dictionary with dataset information
        """
        info = {
            "dataset_path": self.dataset_path,
            "path_exists": os.path.exists(self.dataset_path) if self.dataset_path else False,
            "is_writable": False,
            "is_temporary": self.dataset_path and tempfile.gettempdir() in self.dataset_path
        }
        
        if info["path_exists"]:
            try:
                # Test writeability
                with open(self.dataset_path, 'a') as f:
                    f.write("")
                info["is_writable"] = True
            except:
                info["is_writable"] = False
        
        return info


# Global training logger instance
training_logger = TrainingLogger()
