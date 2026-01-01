"""
MLOps module for Llama 3 fine-tuning via Together AI
"""

import os
import time
import json
from typing import Dict, Any, Optional, Tuple
import together

from .config import Config
from .training_logger import training_logger


class MLOpsManager:
    """Manager for ML operations including fine-tuning"""
    
    def __init__(self):
        """Initialize MLOps manager"""
        if not Config.is_together_configured():
            raise ValueError("Together AI API key is required for MLOps operations")
        
        together.api_key = Config.TOGETHER_API_KEY
    
    def start_finetune_job(
        self,
        dataset_path: Optional[str] = None,
        model_name: str = Config.LLAMA3_BASE_MODEL,
        job_name: str = "linkedin-optimizer-finetune"
    ) -> str:
        """
        Start a fine-tuning job on Together AI.
        
        Args:
            dataset_path: Path to training dataset
            model_name: Base model to fine-tune
            job_name: Name for the fine-tuning job
            
        Returns:
            Job ID for tracking
        """
        try:
            dataset_path = dataset_path or Config.TRAINING_DATASET_PATH
            
            # Check if dataset exists and has examples
            if not os.path.exists(dataset_path):
                raise ValueError(f"Dataset file not found: {dataset_path}")
            
            # Upload dataset to Together AI
            print("Uploading dataset to Together AI...")
            upload_response = together.Files.upload(file=dataset_path)
            
            if not upload_response or 'id' not in upload_response:
                raise ValueError("Failed to upload dataset to Together AI")
            
            file_id = upload_response['id']
            print(f"Dataset uploaded with file ID: {file_id}")
            
            # Start fine-tuning job
            print(f"Starting fine-tuning job for model: {model_name}")
            
            finetune_params = {
                "model": model_name,
                "training_file": file_id,
                "n_epochs": 3,
                "batch_size": 4,
                "learning_rate": 1e-5,
                "suffix": job_name.replace('-', '_'),
                "wandb_api_key": None  # Can be configured if needed
            }
            
            job_response = together.Finetune.create(**finetune_params)
            
            if not job_response or 'id' not in job_response:
                raise ValueError("Failed to start fine-tuning job")
            
            job_id = job_response['id']
            print(f"Fine-tuning job started with ID: {job_id}")
            
            return job_id
            
        except Exception as e:
            raise RuntimeError(f"Failed to start fine-tuning job: {str(e)}")
    
    def check_finetune_status(self, job_id: str) -> Tuple[str, Optional[str]]:
        """
        Check the status of a fine-tuning job.
        
        Args:
            job_id: Job ID to check
            
        Returns:
            Tuple of (status, model_id) where model_id is None if not completed
        """
        try:
            # Get job status
            job_response = together.Finetune.retrieve(job_id)
            
            if not job_response:
                raise ValueError(f"Job not found: {job_id}")
            
            status = job_response.get('status', 'unknown')
            model_id = job_response.get('fine_tuned_model')
            
            # Additional status information
            if status == 'queued':
                print(f"Job {job_id} is queued")
            elif status == 'running':
                epochs = job_response.get('trained_epochs', 0)
                total_epochs = job_response.get('n_epochs', 0)
                print(f"Job {job_id} is running: {epochs}/{total_epochs} epochs completed")
            elif status == 'completed':
                print(f"Job {job_id} completed successfully")
                print(f"Fine-tuned model ID: {model_id}")
            elif status == 'failed':
                error = job_response.get('error', 'Unknown error')
                print(f"Job {job_id} failed: {error}")
            else:
                print(f"Job {job_id} status: {status}")
            
            return status, model_id
            
        except Exception as e:
            raise RuntimeError(f"Failed to check job status: {str(e)}")
    
    def wait_for_completion(self, job_id: str, check_interval: int = 60, timeout: int = 3600) -> Tuple[str, Optional[str]]:
        """
        Wait for a fine-tuning job to complete.
        
        Args:
            job_id: Job ID to wait for
            check_interval: Seconds between status checks
            timeout: Maximum time to wait in seconds
            
        Returns:
            Tuple of (final_status, model_id)
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                status, model_id = self.check_finetune_status(job_id)
                
                if status in ['completed', 'failed']:
                    return status, model_id
                
                print(f"Waiting {check_interval} seconds for next check...")
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Error checking status: {e}")
                time.sleep(check_interval)
        
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
    
    def deploy_model(self, model_id: str) -> bool:
        """
        Deploy a fine-tuned model.
        
        Args:
            model_id: ID of the fine-tuned model to deploy
            
        Returns:
            True if deployment was successful, False otherwise
        """
        try:
            # Together AI typically makes models available automatically after fine-tuning
            # This method can be extended if specific deployment steps are needed
            print(f"Model {model_id} should be available for use")
            return True
            
        except Exception as e:
            print(f"Error deploying model: {e}")
            return False
    
    def test_model(self, model_id: str, test_prompt: str) -> str:
        """
        Test a fine-tuned model with a sample prompt.
        
        Args:
            model_id: ID of the model to test
            test_prompt: Test prompt to send
            
        Returns:
            Model response
        """
        try:
            response = together.Complete.create(
                model=model_id,
                prompt=test_prompt,
                max_tokens=500,
                temperature=0.7,
                stop=["<|eot_id|>"]
            )
            
            return response['choices'][0]['text']
            
        except Exception as e:
            raise RuntimeError(f"Failed to test model: {str(e)}")
    
    def get_job_cost_estimate(self, dataset_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Get cost estimate for fine-tuning.
        
        Args:
            dataset_path: Path to training dataset
            
        Returns:
            Dictionary with cost estimate details
        """
        try:
            dataset_path = dataset_path or Config.TRAINING_DATASET_PATH
            
            # Count examples and estimate tokens
            examples = []
            if os.path.exists(dataset_path):
                with open(dataset_path, 'r') as f:
                    for line in f:
                        if line.strip():
                            examples.append(json.loads(line))
            
            num_examples = len(examples)
            
            # Estimate tokens (rough calculation)
            total_chars = 0
            for example in examples:
                input_text = json.dumps(example.get('input', {}))
                output_text = example.get('output', '')
                total_chars += len(input_text) + len(output_text)
            
            estimated_tokens = total_chars // 4  # Rough estimate: 1 token ≈ 4 chars
            
            # Cost estimation (Together AI pricing - approximate)
            # These are rough estimates and actual costs may vary
            cost_per_1k_tokens = 0.0008  # Approximate cost for Llama 3 8B
            estimated_cost = (estimated_tokens / 1000) * cost_per_1k_tokens * 3  # 3 epochs
            
            return {
                "num_examples": num_examples,
                "estimated_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost,
                "model": Config.LLAMA3_BASE_MODEL,
                "epochs": 3
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to estimate costs: {str(e)}")
    
    def prepare_dataset_for_training(
        self,
        output_path: str,
        min_examples: int = 10,
        quality_filter: str = "neutral"
    ) -> bool:
        """
        Prepare and clean dataset for training.
        
        Args:
            output_path: Path to save the prepared dataset
            min_examples: Minimum number of examples required
            quality_filter: Minimum quality level to include
            
        Returns:
            True if preparation was successful, False otherwise
        """
        try:
            # Get dataset stats
            stats = training_logger.get_dataset_stats()
            
            if stats["total_examples"] < min_examples:
                print(f"Insufficient examples: {stats['total_examples']} < {min_examples}")
                return False
            
            # Export clean dataset
            success = training_logger.export_clean_dataset(output_path, quality_filter)
            
            if success:
                print(f"Dataset prepared successfully: {output_path}")
                print(f"Total examples: {stats['total_examples']}")
                print(f"Positive examples: {stats['positive_examples']}")
                print(f"Negative examples: {stats['negative_examples']}")
            
            return success
            
        except Exception as e:
            print(f"Failed to prepare dataset: {e}")
            return False
    
    def update_config_with_model(self, model_id: str) -> bool:
        """
        Update configuration with the new fine-tuned model ID.
        
        Args:
            model_id: ID of the fine-tuned model
            
        Returns:
            True if update was successful, False otherwise
        """
        try:
            # Update .env file
            env_file = ".env"
            env_lines = []
            
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    env_lines = f.readlines()
            
            # Update or add CUSTOM_LLAMA3_MODEL_ID
            model_line_found = False
            for i, line in enumerate(env_lines):
                if line.startswith("CUSTOM_LLAMA3_MODEL_ID="):
                    env_lines[i] = f"CUSTOM_LLAMA3_MODEL_ID={model_id}\n"
                    model_line_found = True
                    break
            
            if not model_line_found:
                env_lines.append(f"CUSTOM_LLAMA3_MODEL_ID={model_id}\n")
            
            # Write back to file
            with open(env_file, 'w') as f:
                f.writelines(env_lines)
            
            print(f"Updated {env_file} with new model ID: {model_id}")
            return True
            
        except Exception as e:
            print(f"Failed to update configuration: {e}")
            return False


# Global MLOps manager instance
try:
    mlops_manager = MLOpsManager()
except ValueError:
    # MLOps not available (no Together AI key)
    mlops_manager = None
