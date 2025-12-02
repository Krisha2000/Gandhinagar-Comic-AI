"""
Configuration module for Gandhinagar Comic AI
Loads all API keys and constants from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
POLLINATIONS_API_URL = os.getenv("POLLINATIONS_API_URL", "https://image.pollinations.ai/prompt/")

# Model Configuration
GEMINI_MODEL = "gemini-2.0-flash"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Pollinations Safety Suffix
# This MUST be appended to every image generation prompt
SAFETY_SUFFIX = (
    "Comic book art style, clean lines, vibrant colors, slightly anime-influenced webtoon aesthetic, "
    "safe for work, no nudity, no sexual content, no gore, no real people, "
    "no copyrighted characters or logos, original characters only, all-ages friendly"
)

# Directory Paths
BASE_DIR = "gandhinagar_school_project"
CHARACTERS_DIR = os.path.join(BASE_DIR, "data", "1_characters", "students")
IMAGES_DIR = os.path.join(BASE_DIR, "data", "4_images")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")
STORIES_DIR = os.path.join(BASE_DIR, "stories")
COMICS_DIR = os.path.join(BASE_DIR, "comics")

# Comic Generation Settings
NUM_PANELS = 6
PANEL_ASPECT_RATIO = "16:9"

# Validation
def validate_config():
    """Validate that required configuration is present"""
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file")
    return True

# Auto-validate on import
try:
    validate_config()
except ValueError as e:
    print(f"[WARNING] Configuration validation failed: {e}")
