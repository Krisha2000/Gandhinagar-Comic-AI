"""
Character Manager Module
Handles character creation, storage, and management
"""
import os
import json
import uuid
from PIL import Image
import google.generativeai as genai
import config
import rag_index
import comic_renderer

genai.configure(api_key=config.GOOGLE_API_KEY)

def add_character_from_images(name: str, role: str, description: str, 
                               image_files: list, age: str = "", 
                               personality: str = "", tags: list = None) -> dict:
    """
    Add a character with uploaded images.
    
    Args:
        name: Character name
        role: Character role/archetype
        description: Visual description
        image_files: List of uploaded image file objects (Streamlit UploadedFile)
        age: Optional age
        personality: Optional personality description
        tags: Optional list of tags
    
    Returns:
        Character metadata dictionary
    """
    # Generate character ID
    char_id = name.lower().replace(" ", "_") + "_" + str(uuid.uuid4())[:8]
    
    # Create character directory
    char_dir = os.path.join(config.CHARACTERS_DIR, char_id)
    os.makedirs(char_dir, exist_ok=True)
    
    # Save images
    image_paths = []
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(char_dir, f"reference_{i+1}.png")
        
        # Handle both Streamlit UploadedFile and regular file objects
        if hasattr(img_file, 'read'):
            img = Image.open(img_file)
            img.save(img_path)
        else:
            # Direct file path
            img = Image.open(img_file)
            img.save(img_path)
        
        image_paths.append(img_path)
    
    # Create metadata
    char_data = {
        "id": char_id,
        "name": name,
        "role": role,
        "age": age,
        "visual_description": description,
        "personality_description": personality,
        "tags": tags or ["student", "school"],
        "image_paths": image_paths
    }
    
    # Save JSON
    json_path = os.path.join(char_dir, "metadata.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(char_data, f, indent=2)
    
    # Add to RAG index
    rag_index.add_character_to_index(char_data, json_path)
    
    print(f"[✓] Character '{name}' added successfully with {len(image_paths)} images")
    return char_data

def add_character_from_description(name: str, role: str, description: str,
                                   age: str = "", personality: str = "", 
                                   tags: list = None) -> dict:
    """
    Add a character by generating their image from description.
    
    Args:
        name: Character name
        role: Character role/archetype
        description: Visual description (will be used to generate image)
        age: Optional age
        personality: Optional personality description
        tags: Optional list of tags
    
    Returns:
        Character metadata dictionary
    """
    # Generate character ID
    char_id = name.lower().replace(" ", "_") + "_" + str(uuid.uuid4())[:8]
    
    # Create character directory
    char_dir = os.path.join(config.CHARACTERS_DIR, char_id)
    os.makedirs(char_dir, exist_ok=True)
    
    # Generate character image
    print(f"[*] Generating reference image for {name}...")
    
    image_prompt = f"""Character portrait of {name}, {role}. 
{description}. 
{f'Age: {age}.' if age else ''}
Full body or upper body shot, clear view of face and outfit.
{config.SAFETY_SUFFIX}"""
    
    img = comic_renderer.generate_image_from_prompt(image_prompt, panel_num=0)
    
    if not img:
        raise Exception("Failed to generate character image")
    
    # Save generated image
    img_path = os.path.join(char_dir, "reference_generated.png")
    img.save(img_path)
    
    # Create metadata
    char_data = {
        "id": char_id,
        "name": name,
        "role": role,
        "age": age,
        "visual_description": description,
        "personality_description": personality,
        "tags": tags or ["student", "school"],
        "image_paths": [img_path],
        "generated": True
    }
    
    # Save JSON
    json_path = os.path.join(char_dir, "metadata.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(char_data, f, indent=2)
    
    # Add to RAG index
    rag_index.add_character_to_index(char_data, json_path)
    
    print(f"[✓] Character '{name}' created and added successfully")
    return char_data

def get_character_by_id(char_id: str) -> dict:
    """Get character metadata by ID"""
    char_dir = os.path.join(config.CHARACTERS_DIR, char_id)
    json_path = os.path.join(char_dir, "metadata.json")
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def list_all_characters() -> list:
    """List all characters"""
    return rag_index.get_all_characters()

if __name__ == "__main__":
    # Test
    chars = list_all_characters()
    print(f"Found {len(chars)} characters")
    for c in chars:
        print(f"- {c.get('name')}: {c.get('role')}")
