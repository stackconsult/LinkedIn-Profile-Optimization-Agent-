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
        return """You are extracting LinkedIn profile data from screenshots. Your task is to extract ALL visible text with high accuracy. Return ONLY a JSON object with this exact structure:

{
    "headline": "professional title here",
    "about": "complete summary text here - include all paragraphs and details",
    "experience": [
        {
            "title": "exact job title",
            "company": "exact company name", 
            "dates": "exact employment dates",
            "description": "complete job description with all responsibilities, achievements, and details visible"
        }
    ],
    "skills": ["skill1", "skill2", "skill3"]
}

CRITICAL EXTRACTION REQUIREMENTS:
- Extract ALL text visible in the screenshots - do not skip any details
- Include complete job descriptions with all bullet points and responsibilities
- Capture all skills listed, including technical and soft skills
- Preserve exact wording while cleaning up formatting
- If information is not visible in any screenshot, use empty strings "" or empty arrays []
- Escape quotes in text with backslash: \\"
- Do not invent information - only transcribe what you see
- Pay special attention to job descriptions - extract ALL responsibilities and achievements

IMPORTANT: Extract everything visible, especially job descriptions and skills. Return ONLY the JSON object.
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
            print(f"Raw response received: {response_text[:300]}...")
            
            # Clean up the response text in case there's any extra formatting
            response_text = response_text.strip()
            
            # Remove any introductory text before JSON
            if not response_text.startswith('{'):
                # Look for the start of JSON
                json_start = response_text.find('{')
                if json_start != -1:
                    response_text = response_text[json_start:]
                else:
                    raise ValueError("No JSON found in response")
            
            # Remove markdown code blocks
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Find the complete JSON object
            brace_count = 0
            json_end = -1
            for i, char in enumerate(response_text):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end != -1:
                response_text = response_text[:json_end]
            
            # Basic JSON validation before parsing
            if not response_text.startswith('{') or not response_text.endswith('}'):
                raise ValueError("Response doesn't appear to be valid JSON")
            
            # Simple cleaning approach - avoid complex regex
            # Remove trailing commas
            response_text = response_text.replace(',}', '}').replace(',]', ']')
            
            # Replace problematic characters
            response_text = response_text.replace('\n', '\\n').replace('\r', '\\r')
            
            print(f"Cleaned JSON: {response_text[:300]}...")
            
            # Parse JSON with multiple fallback attempts
            try:
                data = json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"First JSON parse failed: {e}")
                
                # Try more aggressive cleaning - manual quote escaping
                try:
                    # Simple approach: manually escape quotes in values
                    cleaned_text = self._manual_quote_escape(response_text)
                    data = json.loads(cleaned_text)
                except Exception as e2:
                    print(f"Second JSON parse failed: {e2}")
                    # Final attempt - create minimal valid structure
                    try:
                        return self._create_fallback_profile(response_text)
                    except Exception:
                        raise ValueError(f"Failed to parse JSON after multiple attempts: {e2}")
            
            # Validate and create profile object
            profile = LinkedInProfile(**data)
            return profile
            
        except Exception as e:
            print(f"Final parsing error: {e}")
            print(f"Response text: {response_text[:500]}...")
            raise ValueError(f"Failed to parse JSON response: {e}")
    
    def _manual_quote_escape(self, text: str) -> str:
        """Manually escape quotes in JSON values - no regex"""
        result = []
        in_quotes = False
        escape_next = False
        
        for i, char in enumerate(text):
            if escape_next:
                result.append(char)
                escape_next = False
                continue
                
            if char == '\\':
                result.append(char)
                escape_next = True
                continue
                
            if char == '"' and not in_quotes:
                # Opening quote for a key or value
                result.append(char)
                in_quotes = True
            elif char == '"' and in_quotes:
                # Closing quote - check if this is end of value or internal quote
                # Look ahead to see if this is followed by a comma, brace, or bracket
                next_chars = text[i+1:i+3].strip()
                if next_chars.startswith(',') or next_chars.startswith('}') or next_chars.startswith(']') or i == len(text) - 1:
                    # This is a closing quote
                    result.append(char)
                    in_quotes = False
                else:
                    # This is an internal quote that needs escaping
                    result.append('\\"')
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _create_fallback_profile(self, response_text: str) -> LinkedInProfile:
        """Create a basic profile from malformed JSON response"""
        # Extract basic information using simple string methods
        headline = ""
        about = ""
        
        # Simple string search for headline
        headline_start = response_text.find('"headline"')
        if headline_start != -1:
            value_start = response_text.find(':', headline_start)
            if value_start != -1:
                quote_start = response_text.find('"', value_start)
                if quote_start != -1:
                    quote_end = response_text.find('"', quote_start + 1)
                    if quote_end != -1:
                        headline = response_text[quote_start + 1:quote_end]
        
        # Simple string search for about
        about_start = response_text.find('"about"')
        if about_start != -1:
            value_start = response_text.find(':', about_start)
            if value_start != -1:
                quote_start = response_text.find('"', value_start)
                if quote_start != -1:
                    quote_end = response_text.find('"', quote_start + 1)
                    if quote_end != -1:
                        about = response_text[quote_start + 1:quote_end]
        
        return LinkedInProfile(
            headline=headline,
            about=about,
            experience=[],
            skills=[]
        )
    
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
