"""
Image processing utilities for LinkedIn Profile Optimization Agent
"""

import base64
import io
from typing import Tuple
from PIL import Image


def resize_image(image_file, max_width: int = 1024) -> Image.Image:
    """
    Resize an image to the specified maximum width while maintaining aspect ratio.
    
    Args:
        image_file: Uploaded file object from Streamlit
        max_width: Maximum width for the resized image
        
    Returns:
        PIL Image object
    """
    try:
        # Open the image
        image = Image.open(image_file)
        
        # Convert to RGB if necessary (for PNG with alpha channel)
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Calculate new dimensions
        width, height = image.size
        if width > max_width:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
        
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")


def encode_image_base64(image: Image.Image) -> str:
    """
    Encode a PIL Image as a base64 string.
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string
    """
    try:
        # Convert image to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=85)
        image_bytes = buffer.getvalue()
        
        # Encode to base64
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return base64_string
        
    except Exception as e:
        raise ValueError(f"Error encoding image to base64: {str(e)}")


def process_uploaded_images(uploaded_files, max_width: int = 1024) -> list:
    """
    Process multiple uploaded image files and return base64 encoded strings.
    
    Args:
        uploaded_files: List of uploaded file objects from Streamlit
        max_width: Maximum width for resized images
        
    Returns:
        List of base64 encoded image strings
    """
    base64_images = []
    
    for uploaded_file in uploaded_files:
        try:
            # Resize and encode each image
            resized_image = resize_image(uploaded_file, max_width)
            base64_image = encode_image_base64(resized_image)
            base64_images.append(base64_image)
        except Exception as e:
            print(f"Warning: Failed to process {uploaded_file.name}: {str(e)}")
            continue
    
    return base64_images


def get_image_info(image_file) -> Tuple[str, int, int]:
    """
    Get basic information about an uploaded image.
    
    Args:
        image_file: Uploaded file object from Streamlit
        
    Returns:
        Tuple of (format, width, height)
    """
    try:
        image = Image.open(image_file)
        return image.format, image.width, image.height
    except Exception as e:
        raise ValueError(f"Error reading image info: {str(e)}")
