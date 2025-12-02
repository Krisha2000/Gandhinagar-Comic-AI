"""
Comic Renderer Module
Generates comic panel images using Pollinations API with safety controls
"""
import os
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import config

def generate_image_from_prompt(prompt: str, panel_num: int = 1) -> Image.Image:
    """
    Generate image from prompt using Pollinations API.
    Safety suffix is automatically added by prompt_generator.py
    
    Args:
        prompt: Image generation prompt (already includes safety suffix)
        panel_num: Panel number for logging
    
    Returns:
        PIL Image object or None if failed
    """
    print(f"[*] Generating Panel {panel_num}...")
    
    # Sanitize prompt: remove newlines and extra spaces
    clean_prompt = " ".join(prompt.split())
    
    # Encode prompt for URL
    import urllib.parse
    safe_prompt = urllib.parse.quote(clean_prompt)
    url = f"{config.POLLINATIONS_API_URL}{safe_prompt}"
    
    try:
        response = requests.get(url, timeout=90)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        print(f"    [✓] Panel {panel_num} generated successfully")
        return img
    except Exception as e:
        print(f"    [✗] Panel {panel_num} failed: {e}")
        print(f"    [DEBUG] URL was: {url[:100]}...") # Print start of URL for debug
        return None

def add_dialogue_overlay(image: Image.Image, dialogue: str) -> Image.Image:
    """
    Add dialogue text box to comic panel.
    
    Args:
        image: PIL Image
        dialogue: Text to display
    
    Returns:
        Image with dialogue overlay
    """
    if not dialogue or not dialogue.strip():
        return image
    
    # Create a copy to avoid modifying original
    img = image.copy()
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Load font
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
    
    # Wrap text
    wrapped_text = textwrap.fill(dialogue, width=45)
    
    # Calculate text size
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Box dimensions
    padding = 25
    box_w = min(width - 40, text_w + (padding * 2))
    box_h = text_h + (padding * 2)
    box_x = (width - box_w) // 2
    box_y = height - box_h - 30
    
    # Draw white box with black border
    draw.rectangle(
        [(box_x, box_y), (box_x + box_w, box_y + box_h)],
        fill="white",
        outline="black",
        width=4
    )
    
    # Draw text (centered)
    text_x = box_x + (box_w - text_w) // 2
    text_y = box_y + padding
    
    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        fill="black",
        font=font,
        align="center"
    )
    
    return img

def render_comic_panels(prompts: list, output_dir: str = "comic_output") -> list:
    """
    Render all comic panels from prompts.
    
    Args:
        prompts: List of prompt dictionaries from prompt_generator
        output_dir: Directory to save images
    
    Returns:
        List of image file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    
    for prompt_data in prompts:
        panel_num = prompt_data.get("panel", 1)
        image_prompt = prompt_data.get("image_prompt", "")
        dialogue = prompt_data.get("dialogue", "")
        
        # Generate image
        img = generate_image_from_prompt(image_prompt, panel_num)
        
        if img:
            # Add dialogue
            if dialogue:
                img = add_dialogue_overlay(img, dialogue)
            
            # Save
            save_path = os.path.join(output_dir, f"panel_{panel_num}.png")
            img.save(save_path)
            image_paths.append(save_path)
            print(f"    [✓] Saved to {save_path}")
        else:
            print(f"    [✗] Panel {panel_num} skipped due to generation failure")
    
    return image_paths

if __name__ == "__main__":
    # Test
    test_prompts = [
        {
            "panel": 1,
            "image_prompt": "School classroom, student looking worried. " + config.SAFETY_SUFFIX,
            "dialogue": "Oh no, I'm late!"
        }
    ]
    paths = render_comic_panels(test_prompts)
    print(f"\nGenerated {len(paths)} panels")
