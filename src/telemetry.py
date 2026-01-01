"""
Telemetry and observability for LinkedIn Profile Optimization Agent
Cloud-optimized for Streamlit Community Cloud deployment
"""

import time
import json
import os
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime

from .config import Config


class TelemetryLogger:
    """Logger for telemetry and observability with cloud-friendly storage"""
    
    def __init__(self):
        """Initialize telemetry logger"""
        self.langfuse_client = None
        self.local_logs = []
        self.log_file_path = os.path.join(Config.TEMP_DIR, "telemetry_logs.json")
        
        # Initialize Langfuse if configured
        if Config.is_langfuse_configured():
            try:
                from langfuse import Langfuse
                self.langfuse_client = Langfuse(
                    secret_key=Config.LANGFUSE_SECRET_KEY,
                    public_key=Config.LANGFUSE_PUBLIC_KEY,
                    host=Config.LANGFUSE_HOST
                )
            except ImportError:
                print("Langfuse not installed, using local logging only")
            except Exception as e:
                print(f"Failed to initialize Langfuse: {e}")
        
        # Load existing logs if available
        self._load_logs()
    
    def _load_logs(self):
        """Load existing logs from file with error handling"""
        try:
            if os.path.exists(self.log_file_path):
                with open(self.log_file_path, 'r') as f:
                    self.local_logs = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load telemetry logs: {e}")
            self.local_logs = []
    
    def _save_logs(self):
        """Save logs to file with error handling"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            
            with open(self.log_file_path, 'w') as f:
                json.dump(self.local_logs, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save telemetry logs: {e}")
            # Don't fail the application if logging fails
    
    def _add_log_entry(self, log_data: Dict[str, Any]):
        """Add a log entry with cloud-friendly persistence"""
        try:
            # Store locally
            self.local_logs.append(log_data)
            
            # Keep only last 1000 entries to manage memory
            if len(self.local_logs) > 1000:
                self.local_logs = self.local_logs[-1000:]
            
            # Save to file (with error handling)
            self._save_logs()
            
        except Exception as e:
            print(f"Warning: Failed to add log entry: {e}")
            # Don't fail the application if logging fails
    
    def log_vision_extraction(
        self,
        num_images: int,
        extraction_time: float,
        success: bool,
        error_message: Optional[str] = None
    ):
        """
        Log vision extraction metrics.
        
        Args:
            num_images: Number of images processed
            extraction_time: Time taken for extraction in seconds
            success: Whether extraction was successful
            error_message: Error message if extraction failed
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "vision_extraction",
            "num_images": num_images,
            "extraction_time": extraction_time,
            "success": success,
            "error_message": error_message
        }
        
        # Add to local storage
        self._add_log_entry(log_data)
        
        # Send to Langfuse if available
        if self.langfuse_client:
            try:
                trace = self.langfuse_client.trace(
                    name="vision_extraction",
                    input={"num_images": num_images},
                    output={"success": success, "extraction_time": extraction_time}
                )
                
                if not success:
                    trace.level("ERROR")
                    trace.update(output={"error": error_message})
                    
            except Exception as e:
                print(f"Failed to log to Langfuse: {e}")
    
    def log_strategy_generation(
        self,
        model_choice: str,
        target_industry: str,
        target_role: str,
        input_tokens: int,
        output_tokens: int,
        generation_time: float,
        success: bool,
        error_message: Optional[str] = None
    ):
        """
        Log strategy generation metrics.
        
        Args:
            model_choice: Model used for generation
            target_industry: Target industry
            target_role: Target role
            input_tokens: Estimated input tokens
            output_tokens: Estimated output tokens
            generation_time: Time taken for generation in seconds
            success: Whether generation was successful
            error_message: Error message if generation failed
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "strategy_generation",
            "model_choice": model_choice,
            "target_industry": target_industry,
            "target_role": target_role,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "generation_time": generation_time,
            "success": success,
            "error_message": error_message
        }
        
        # Add to local storage
        self._add_log_entry(log_data)
        
        # Send to Langfuse if available
        if self.langfuse_client:
            try:
                trace = self.langfuse_client.trace(
                    name="strategy_generation",
                    input={
                        "model": model_choice,
                        "industry": target_industry,
                        "role": target_role,
                        "input_tokens": input_tokens
                    },
                    output={
                        "output_tokens": output_tokens,
                        "generation_time": generation_time,
                        "success": success
                    }
                )
                
                if not success:
                    trace.level("ERROR")
                    trace.update(output={"error": error_message})
                    
            except Exception as e:
                print(f"Failed to log to Langfuse: {e}")
    
    def log_user_feedback(
        self,
        section_name: str,
        feedback_type: str,  # "positive" or "negative"
        model_choice: str,
        additional_context: Optional[str] = None
    ):
        """
        Log user feedback on generated content.
        
        Args:
            section_name: Name of the section (e.g., "headline", "about")
            feedback_type: Type of feedback ("positive" or "negative")
            model_choice: Model that generated the content
            additional_context: Additional context if provided
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "user_feedback",
            "section_name": section_name,
            "feedback_type": feedback_type,
            "model_choice": model_choice,
            "additional_context": additional_context
        }
        
        # Add to local storage
        self._add_log_entry(log_data)
        
        # Send to Langfuse if available
        if self.langfuse_client:
            try:
                trace = self.langfuse_client.trace(
                    name="user_feedback",
                    input={
                        "section": section_name,
                        "feedback": feedback_type,
                        "model": model_choice
                    },
                    output={"logged": True}
                )
                
            except Exception as e:
                print(f"Failed to log to Langfuse: {e}")
    
    def get_telemetry_status(self) -> Dict[str, Any]:
        """
        Get telemetry system status for cloud UI display.
        
        Returns:
            Dictionary with telemetry status information
        """
        return {
            "langfuse_enabled": self.langfuse_client is not None,
            "local_logs_count": len(self.local_logs),
            "log_file_path": self.log_file_path,
            "log_file_exists": os.path.exists(self.log_file_path),
            "is_temporary_storage": Config.TEMP_DIR in self.log_file_path
        }
    
    def get_local_logs(self, limit: int = 100) -> list:
        """
        Get recent local logs.
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            List of log entries
        """
        return self.local_logs[-limit:]
    
    def export_logs(self, filepath: str) -> bool:
        """
        Export local logs to a JSON file.
        
        Args:
            filepath: Path to save the logs
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.local_logs, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to export logs: {e}")
            return False
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics from local logs.
        
        Returns:
            Dictionary with usage statistics
        """
        stats = {
            "total_events": len(self.local_logs),
            "vision_extractions": 0,
            "strategy_generations": 0,
            "user_feedback": 0,
            "model_usage": {},
            "industry_usage": {},
            "success_rate": {"vision": 0, "strategy": 0}
        }
        
        vision_success = 0
        vision_total = 0
        strategy_success = 0
        strategy_total = 0
        
        for log in self.local_logs:
            event_type = log.get("event_type")
            
            if event_type == "vision_extraction":
                stats["vision_extractions"] += 1
                vision_total += 1
                if log.get("success", False):
                    vision_success += 1
                    
            elif event_type == "strategy_generation":
                stats["strategy_generations"] += 1
                strategy_total += 1
                if log.get("success", False):
                    strategy_success += 1
                    
                # Track model usage
                model = log.get("model_choice", "unknown")
                stats["model_usage"][model] = stats["model_usage"].get(model, 0) + 1
                
                # Track industry usage
                industry = log.get("target_industry", "unknown")
                stats["industry_usage"][industry] = stats["industry_usage"].get(industry, 0) + 1
                    
            elif event_type == "user_feedback":
                stats["user_feedback"] += 1
        
        # Calculate success rates
        if vision_total > 0:
            stats["success_rate"]["vision"] = vision_success / vision_total
        if strategy_total > 0:
            stats["success_rate"]["strategy"] = strategy_success / strategy_total
        
        return stats


# Global telemetry instance
telemetry = TelemetryLogger()
