"""
Image Analyzer Module
Handles image analysis, story generation, and image recreation using Gemini Vision
"""
import os
from PIL import Image
import google.generativeai as genai
import config
import comic_renderer
import rag_index

genai.configure(api_key=config.GOOGLE_API_KEY)

def analyze_image(image_file, prompt: str) -> str:
    """
    Analyze an image using Gemini Vision and respond to user prompt.
    
    Args:
        image_file: PIL Image or file path
        prompt: User's question/instruction about the image
    
    Returns:
        AI-generated response
    """
    try:
        # Load image if it's a path
        if isinstance(image_file, str):
            img = Image.open(image_file)
        else:
            img = image_file
        
        # Use Gemini Vision model
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        
        response = model.generate_content([prompt, img])
        return response.text.strip()
    
    except Exception as e:
        return f"Error analyzing image: {e}"

def generate_story_from_image(image_file) -> str:
    """
    Generate a story based on the uploaded image.
    
    Args:
        image_file: PIL Image or file path
    
    Returns:
        Generated story text
    """
    prompt = """Analyze this image and create an engaging short story (6-8 sentences) based on what you see.

The story should:
- Be set in an Indian school context (Gandhinagar School)
- Include realistic dialogue
- Be fun, relatable, and appropriate for all ages
- Capture the mood and action shown in the image
- Have a beginning, middle, and end

Write the story now:"""
    
    return analyze_image(image_file, prompt)

def describe_image(image_file) -> str:
    """
    Provide a detailed description of the image.
    
    Args:
        image_file: PIL Image or file path
    
    Returns:
        Detailed image description
    """
    prompt = """Describe this image in detail. Include:
1. Main subjects/characters (age, appearance, clothing, expressions)
2. Setting/background
3. Actions/activities happening
4. Mood/atmosphere
5. Art style (if applicable)
6. Any text or speech bubbles visible

Be specific and thorough:"""
    
    return analyze_image(image_file, prompt)

def recreate_with_characters(image_file, character_names: list = None, custom_prompt: str = None) -> dict:
    """
    Recreate the image with user's own characters from the database.
    
    Args:
        image_file: PIL Image or file path
        character_names: List of character names to include (if None, uses all available)
        custom_prompt: Optional custom instructions from user
    
    Returns:
        Dictionary with 'description' (text) and 'image_path' (generated image path)
    """
    try:
        # Step 1: Analyze the original image style and composition
        analysis_prompt = """Analyze this image and extract:
1. Art style (anime, cartoon, realistic, etc.)
2. Composition (close-up, group shot, full scene, etc.)
3. Mood/tone (happy, dramatic, action-packed, etc.)
4. Setting/background details
5. Pose and arrangement of subjects

Provide a concise summary in 2-3 sentences that could be used to recreate a similar image:"""
        
        style_description = analyze_image(image_file, analysis_prompt)
        
        # Step 2: Get character descriptions from RAG or File System
        if character_names:
            # Use specified characters
            character_data_list = []
            all_characters = rag_index.get_all_characters() # Cache all characters for fallback
            
            for name in character_names:
                found = False
                
                # Try RAG search first
                results = rag_index.search_characters(name, k=1)
                if results:
                    try:
                        import json
                        content = results[0].page_content
                        if "Full Data:" in content:
                            json_str = content.split("Full Data:", 1)[1].strip()
                            char_data = json.loads(json_str)
                            # Verify name match to avoid fuzzy mismatch
                            if char_data.get("name", "").lower() == name.lower():
                                character_data_list.append(char_data)
                                found = True
                    except:
                        pass
                
                # Fallback: Search in all characters list (File System)
                if not found:
                    print(f"[INFO] RAG search failed for '{name}', trying file system fallback...")
                    for char in all_characters:
                        if char.get("name", "").lower() == name.lower():
                            character_data_list.append(char)
                            found = True
                            break
                
                if not found:
                    print(f"[WARN] Character '{name}' not found in DB or files.")

        else:
            # Use all available characters
            character_data_list = rag_index.get_all_characters()
        
        if not character_data_list:
            return {
                "description": "No characters found in database. Please add characters first!",
                "image_path": None
            }
        
        # Step 3: Build character descriptions
        character_descriptions = []
        for char_data in character_data_list[:3]:  # Max 3 characters
            char_name = char_data.get("name", "character")
            
            visual_desc = ""
            if "visual_description" in char_data:
                visual_desc = char_data["visual_description"]
            elif "visual_features" in char_data:
                features = char_data["visual_features"]
                parts = []
                if isinstance(features, dict):
                    for key, value in features.items():
                        if isinstance(value, str):
                            parts.append(value)
                visual_desc = ", ".join(parts)
            
            role = char_data.get("role", "student")
            character_descriptions.append(f"{char_name} ({role}): {visual_desc}")
        
        # Step 4: Create image generation prompt
        char_names_str = ", ".join([cd.get("name", "character") for cd in character_data_list[:3]])
        
        image_prompt = f"""Recreate this image style with characters {char_names_str}.

ORIGINAL STYLE: {style_description}

CHARACTERS TO INCLUDE:
{'; '.join(character_descriptions)}

{custom_prompt if custom_prompt else ''}

Indian school setting, school uniforms. {config.SAFETY_SUFFIX}"""
        
        # Step 5: Generate the image
        print(f"[*] Generating recreated image with characters: {char_names_str}")
        img = comic_renderer.generate_image_from_prompt(image_prompt, panel_num=0)
        
        if img:
            import tempfile
            import uuid
            temp_dir = tempfile.gettempdir()
            img_filename = f"recreated_{uuid.uuid4().hex[:8]}.png"
            img_path = os.path.join(temp_dir, img_filename)
            img.save(img_path)
            
            return {
                "description": f"✨ Recreated the image with your characters: {char_names_str}! Based on the original style: {style_description}",
                "image_path": img_path
            }
        else:
            return {
                "description": "Failed to generate image. Please try again.",
                "image_path": None
            }
    
    except Exception as e:
        return {
            "description": f"Error during recreation: {e}",
            "image_path": None
        }

if __name__ == "__main__":
    # Test with a sample image
    print("Image Analyzer Module")
    print("Functions available:")
    print("- analyze_image(image, prompt)")
    print("- generate_story_from_image(image)")
    print("- describe_image(image)")
    print("- recreate_with_characters(image, character_names)")
