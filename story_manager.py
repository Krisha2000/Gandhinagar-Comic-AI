"""
Story Manager Module
Handles saving, loading, and deleting stories on disk and in RAG.
"""
import os
import json
import uuid
from datetime import datetime
import config
import rag_index

def get_all_stories() -> list:
    """
    Get all saved stories sorted by date (newest first).
    
    Returns:
        List of story dictionaries
    """
    stories = []
    if not os.path.exists(config.STORIES_DIR):
        os.makedirs(config.STORIES_DIR, exist_ok=True)
        return stories
        
    for filename in os.listdir(config.STORIES_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(config.STORIES_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                    stories.append(story_data)
            except Exception as e:
                print(f"[WARN] Failed to load story {filename}: {e}")
    
    # Sort by date (newest first)
    stories.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return stories

def save_story(story_text: str, title: str = None) -> dict:
    """
    Save a story to disk and RAG.
    
    Args:
        story_text: Content of the story
        title: Optional title (defaults to first few words)
    
    Returns:
        The saved story dictionary
    """
    if not os.path.exists(config.STORIES_DIR):
        os.makedirs(config.STORIES_DIR, exist_ok=True)
        
    story_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    if not title:
        # Generate title from first few words
        title = " ".join(story_text.split()[:5]) + "..."
        
    story_data = {
        "id": story_id,
        "title": title,
        "content": story_text,
        "created_at": timestamp,
        "type": "story"
    }
    
    # Save to disk
    filename = f"{story_id}.json"
    filepath = os.path.join(config.STORIES_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, indent=2)
        
    # Add to RAG
    rag_index.add_story_to_index(story_text, metadata=story_data)
    
    print(f"[✓] Story '{title}' saved and indexed.")
    return story_data

def delete_story(story_id: str) -> bool:
    """
    Delete a story from disk and RAG.
    
    Args:
        story_id: ID of the story to delete
        
    Returns:
        True if successful, False otherwise
    """
    filename = f"{story_id}.json"
    filepath = os.path.join(config.STORIES_DIR, filename)
    
    # Delete from disk
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"[ERR] Failed to delete file {filepath}: {e}")
            return False
    else:
        print(f"[WARN] Story file {filepath} not found.")
        
    # Delete from RAG
    rag_index.delete_document(story_id)
    
    print(f"[✓] Story {story_id} deleted.")
    return True

if __name__ == "__main__":
    # Test
    s = save_story("Once upon a time in Gandhinagar...", "Test Story")
    print(f"Saved: {s['id']}")
    stories = get_all_stories()
    print(f"Total stories: {len(stories)}")
    # delete_story(s['id'])
