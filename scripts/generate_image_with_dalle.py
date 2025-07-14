import openai
import requests
import os
import time
import sys
import argparse
from PIL import Image
import io
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIG ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../assets/images/image.png')
DEFAULT_PROMPT = "A professional golf ball label design with elegant typography, clean white background, landscape orientation, suitable for 3D model texturing"

# Initialize OpenAI client
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_image_with_dalle(prompt=DEFAULT_PROMPT, size: Literal["1024x1024", "1792x1024", "1024x1792"] = "1792x1024"):
    """
    Generate an image using DALL-E 3 and save it to the specified path.
    
    Args:
        prompt (str): The text prompt for image generation
        size (str): Image size (1024x1024, 1792x1024, 1024x1792)
    """
    try:
        print(f"[INFO] Generating image with prompt: {prompt}")
        print(f"[INFO] Using size: {size}")
        
        # Add system prompt to ensure text height matches image height
        system_prompt = "All text in the image should have a height equal to the full height of the image. Text should be large, bold, and fill the vertical space completely."
        enhanced_prompt = f"{system_prompt} {prompt}"
        
        # Generate image with DALL-E 3
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size=size,
            quality="standard",
            n=1,
        )
        
        # Get the image URL
        if not response.data or len(response.data) == 0:
            raise ValueError("No image data received from DALL-E")
        
        image_url = response.data[0].url
        if not image_url:
            raise ValueError("No image URL received from DALL-E")
        
        # Download the image
        print("[INFO] Downloading generated image...")
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        # Open and process the image
        image = Image.open(io.BytesIO(image_response.content))
        
        # Convert to landscape if needed (DALL-E 3 doesn't support custom aspect ratios)
        if size == "1024x1024":
            # Crop to landscape aspect ratio (16:9)
            width, height = image.size
            target_width = int(height * 16 / 9)
            left = (width - target_width) // 2
            right = left + target_width
            image = image.crop((left, 0, right, height))
        
        # Save the image
        image.save(IMAGE_PATH, "PNG")
        print(f"[INFO] Image saved to: {IMAGE_PATH}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to generate image: {str(e)}")
        return False

def generate_custom_label(prompt=None):
    """
    Generate a custom golf ball label with user-provided prompt.
    """
    if prompt is None:
        prompt = input("Enter your label design prompt (or press Enter for default): ").strip()
        if not prompt:
            prompt = DEFAULT_PROMPT
    
    # Add landscape orientation to the prompt
    if "landscape" not in prompt.lower():
        prompt += ", landscape orientation"
    
    return generate_image_with_dalle(prompt, "1792x1024")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate golf ball labels with DALL-E")
    parser.add_argument("--prompt", type=str, help="Custom prompt for image generation")
    return parser.parse_args()

def main():
    """
    Main function to run the image generation.
    """
    print("=== DALL-E Image Generator for Golf Labels ===")
    print("This script will generate an image and save it to image.png")
    print("The async_blend.py script will detect this change and update your 3D model.")
    print()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check if the target directory exists
    target_dir = os.path.dirname(IMAGE_PATH)
    if not os.path.exists(target_dir):
        print(f"[ERROR] Target directory does not exist: {target_dir}")
        return
    
    # Generate the image
    if args.prompt:
        success = generate_custom_label(args.prompt)
    else:
        success = generate_custom_label()
    
    if success:
        print("\n[SUCCESS] Image generated and saved!")
        print("The async_blend.py script should detect this change and update your 3D model.")
        print("Check the exported_label.glb file for your updated 3D model.")
    else:
        print("\n[ERROR] Failed to generate image. Please check your API key and try again.")

if __name__ == "__main__":
    main() 