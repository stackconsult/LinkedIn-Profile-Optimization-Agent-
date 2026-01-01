"""
Vision engine for extracting LinkedIn profile data from screenshots
"""

import json
import time
import re
import base64
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from openai import OpenAI

from .config import Config
from .image_utils import process_uploaded_images


class ExperienceItem(BaseModel):
    """Model for a single experience item"""
    title: str = Field(default="", description="Job title")
    company: str = Field(default="", description="Company name")
    dates: str = Field(default="", description="Employment dates")
    description: str = Field(default="", description="Job description")


class LinkedInProfile(BaseModel):
    """Model for LinkedIn profile data extracted from screenshots"""
    headline: str = Field(default="", description="Profile headline")
    about: str = Field(default="", description="About section")
    experience: List[ExperienceItem] = Field(default_factory=list, description="Work experience")
    skills: List[str] = Field(default_factory=list, description="Skills list")


class VisionEngine:
    """Engine for extracting structured data from LinkedIn screenshots"""
    
    def __init__(self):
        """Initialize the vision engine with OpenAI client"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API key is required for vision engine")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def _create_vision_prompt(self) -> str:
        """Create the prompt for vision model"""
        return """
        Extract LinkedIn profile information from these screenshots. 
        
        Extract the following sections:
        1. Headline - the main professional title under the name
        2. About - the summary section
        3. Experience - list of work experiences with title, company, dates, and description for each
        4. Skills - list of skills shown
        
        CRITICAL REQUIREMENTS:
        - Return ONLY valid JSON - no explanations, no markdown, no extra text
        - Escape all quotes inside text fields with backslashes (\\")
        - Do not invent information - only transcribe what's visible
        - If a section is not visible, use empty string for text fields or empty list for arrays
        - Normalize text formatting but preserve all content
        - Include all experience entries that are visible
        - Handle special characters properly - newlines should be \\n, quotes should be \\"
        
        Use this exact JSON structure:
        {
            "headline": "...",
            "about": "...",
            "experience": [
                {
                    "title": "...",
                    "company": "...",
                    "dates": "...",
                    "description": "..."
                }
            ],
            "skills": ["...", "..."]
        }
        
        IMPORTANT: Your entire response must be valid JSON that can be parsed directly.
        """
    
    def _prepare_messages(self, base64_images: List[str]) -> List[Dict[str, Any]]:
        """Prepare messages for the vision API call"""
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": self._create_vision_prompt()
                    }
                ]
            }
        ]
        
        # Add images to the message
        for base64_image in base64_images:
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "high"
                }
            })
        
        return messages
    
    def _parse_response(self, response_text: str) -> LinkedInProfile:
        """Parse the vision model response into a structured profile"""
        try:
            # Clean up the response text in case there's any extra formatting
            response_text = response_text.strip()
            
            # Remove markdown code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Try to extract JSON if there's extra text
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            # Fix common JSON issues from OCR text
            # Replace unescaped quotes in text fields
            response_text = re.sub(r'(?<!\\)"(?=[^,\[\]\{\}]*[^,\[\]\{\}])', r'\\"', response_text)
            
            # Remove or replace problematic characters
            response_text = response_text.replace('\n', '\\n').replace('\r', '\\r')
            
            # Parse JSON with more robust error handling
            try:
                data = json.loads(response_text)
            except json.JSONDecodeError as e:
                # Try to fix common JSON issues
                # Remove trailing commas
                response_text = re.sub(r',\s*([}\]])', r'\1', response_text)
                # Fix quotes
                response_text = re.sub(r'(?<!\\)"(?=[^,\[\]\{\}]*[^,\[\]\{\}])', r'\\"', response_text)
                
                data = json.loads(response_text)
            
            # Validate and create profile object
            profile = LinkedInProfile(**data)
            return profile
            
        except json.JSONDecodeError as e:
            # Log the problematic response for debugging
            print(f"JSON parsing error: {e}")
            print(f"Response text: {response_text[:500]}...")
            raise ValueError(f"Failed to parse JSON response: {e}")
        except Exception as e:
            raise ValueError(f"Error processing vision response: {e}")
    
    def extract_profile_data(self, uploaded_files) -> LinkedInProfile:
        """
        Extract structured LinkedIn profile data from uploaded screenshots.
        
        Args:
            uploaded_files: List of uploaded file objects from Streamlit
            
        Returns:
            LinkedInProfile object with extracted data
        """
        if not uploaded_files:
            raise ValueError("No image files provided")
        
        try:
            # Process images
            base64_images = process_uploaded_images(
                uploaded_files, 
                max_width=Config.MAX_IMAGE_WIDTH
            )
            
            if not base64_images:
                raise ValueError("No valid images could be processed")
            
            # Prepare API call
            messages = self._prepare_messages(base64_images)
            
            # Call vision model with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=Config.GPT4O_VISION_MODEL_ID,
                        messages=messages,
                        max_tokens=2000,
                        temperature=0.1
                    )
                    break
                except Exception as api_error:
                    if attempt == max_retries - 1:
                        raise api_error
                    time.sleep(2 ** attempt)  # Exponential backoff
            
            # Extract and parse response
            response_text = response.choices[0].message.content
            if not response_text:
                raise ValueError("Empty response from vision model")
            
            # Log the raw response for debugging
            print(f"Raw vision response: {response_text[:200]}...")
            
            profile = self._parse_response(response_text)
            return profile
            
        except Exception as e:
            # Add more context to the error
            error_msg = f"Vision extraction failed: {str(e)}"
            if "JSON" in str(e):
                error_msg += " - The vision model had trouble parsing the LinkedIn screenshots. Please try with clearer images."
            elif "rate limit" in str(e).lower():
                error_msg += " - Rate limit exceeded. Please wait a moment and try again."
            elif "timeout" in str(e).lower():
                error_msg += " - Request timed out. Please try with smaller or fewer images."
            
            raise RuntimeError(error_msg)
    
    def validate_extraction(self, profile: LinkedInProfile) -> Dict[str, Any]:
        """
        Validate the extracted profile data and provide feedback.
        
        Args:
            profile: LinkedInProfile object to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "is_valid": True,
            "warnings": [],
            "missing_sections": []
        }
        
        # Check for empty sections
        if not profile.headline:
            validation_results["missing_sections"].append("headline")
            validation_results["warnings"].append("No headline found")
        
        if not profile.about:
            validation_results["missing_sections"].append("about")
            validation_results["warnings"].append("No about section found")
        
        if not profile.experience:
            validation_results["missing_sections"].append("experience")
            validation_results["warnings"].append("No experience entries found")
        
        if not profile.skills:
            validation_results["missing_sections"].append("skills")
            validation_results["warnings"].append("No skills found")
        
        # Check for incomplete experience entries
        incomplete_exp = []
        for i, exp in enumerate(profile.experience):
            if not exp.title or not exp.company:
                incomplete_exp.append(f"Experience {i+1}")
        
        if incomplete_exp:
            validation_results["warnings"].append(f"Incomplete experience entries: {', '.join(incomplete_exp)}")
        
        validation_results["is_valid"] = len(validation_results["missing_sections"]) == 0
        
        return validation_results
