"""
RAG Index Module
Handles vector-based character search and indexing
"""
import os
import json
import uuid
try:
    from langchain_core.documents import Document
except ImportError:
    class Document:
        def __init__(self, page_content: str = "", metadata: dict = None):
            self.page_content = page_content
            self.metadata = metadata or {}

try:
    from langchain_chroma import Chroma
except ImportError:
    class Chroma:
        def __init__(self, persist_directory=None, embedding_function=None, collection_name=None):
            self.persist_directory = persist_directory
            self.embedding_function = embedding_function
            self.collection_name = collection_name
            self._docs = []
        def add_documents(self, docs, ids=None):
            self._docs.extend(docs)
        def similarity_search(self, query, k=5):
            return []
        def delete(self, ids=None):
            pass

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    class HuggingFaceEmbeddings:
        def __init__(self, model_name=None):
            self.model_name = model_name
        def embed_documents(self, docs):
            return []
        def embed_query(self, query):
            return []
import config

def get_vectorstore():
    """Get or create the vector store"""
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
    
    vectorstore = Chroma(
        persist_directory=config.VECTOR_DB_DIR,
        embedding_function=embeddings,
        collection_name="gandhinagar_school"
    )
    
    return vectorstore

def add_character_to_index(char_data: dict, json_path: str):
    """
    Add a character to the RAG index.
    
    Args:
        char_data: Character metadata dictionary
        json_path: Path to the character JSON file
    """
    vectorstore = get_vectorstore()
    
    # Create searchable content
    content = f"""Name: {char_data.get('name', 'Unknown')}
Role: {char_data.get('role', 'Unknown')}
Visual Description: {char_data.get('visual_description', '')}
Personality: {char_data.get('personality_description', '')}
Tags: {', '.join(char_data.get('tags', []))}

Full Data:
{json.dumps(char_data, indent=2)}"""
    
    doc = Document(
        page_content=content,
        metadata={
            "source": json_path,
            "type": "character",
            "name": char_data.get("name", "Unknown"),
            "character_id": char_data.get("id", "unknown")
        }
    )
    
    vectorstore.add_documents([doc])
    print(f"[✓] Added {char_data.get('name')} to RAG index")

def add_story_to_index(story_text: str, metadata: dict = None):
    """
    Add a story to the RAG index.
    
    Args:
        story_text: The full text of the story
        metadata: Optional metadata (date, title, etc.)
    """
    vectorstore = get_vectorstore()
    
    if metadata is None:
        metadata = {}
    
    # Ensure ID is in metadata for deletion later
    if "id" not in metadata:
        metadata["id"] = str(uuid.uuid4())
        
    metadata["type"] = "story"
    metadata["source"] = "user_generated"
    
    doc = Document(
        page_content=story_text,
        metadata=metadata
    )
    
    # Use the ID as the document ID in Chroma
    vectorstore.add_documents([doc], ids=[metadata["id"]])
    print(f"[✓] Added story to RAG index (ID: {metadata['id']})")

def delete_document(doc_id: str):
    """
    Delete a document from the RAG index by ID.
    
    Args:
        doc_id: The ID of the document to delete
    """
    vectorstore = get_vectorstore()
    try:
        vectorstore.delete(ids=[doc_id])
        print(f"[✓] Deleted document {doc_id} from RAG index")
    except Exception as e:
        print(f"[WARN] Failed to delete document {doc_id}: {e}")

def search_characters(query: str, k: int = 5) -> list:
    """
    Search for characters by query.
    
    Args:
        query: Search query
        k: Number of results
    
    Returns:
        List of character documents
    """
    vectorstore = get_vectorstore()
    
    try:
        results = vectorstore.similarity_search(query, k=k)
        return results
    except Exception as e:
        print(f"[WARN] Character search failed: {e}")
        return []

def get_all_characters() -> list:
    """
    Get all characters from the database.
    
    Returns:
        List of character metadata dictionaries
    """
    characters = []
    
    if not os.path.exists(config.CHARACTERS_DIR):
        return characters
    
    for item_name in os.listdir(config.CHARACTERS_DIR):
        item_path = os.path.join(config.CHARACTERS_DIR, item_name)
        
        # Check if it's a directory (new structure)
        if os.path.isdir(item_path):
            json_path = os.path.join(item_path, "metadata.json")
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        char_data = json.load(f)
                        characters.append(char_data)
                except Exception as e:
                    print(f"[WARN] Failed to load {json_path}: {e}")
        
        # Check if it's a JSON file (old structure/fallback)
        elif item_name.endswith('.json'):
            try:
                with open(item_path, 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                    characters.append(char_data)
            except Exception as e:
                print(f"[WARN] Failed to load {item_name}: {e}")
    
    return characters

if __name__ == "__main__":
    # Test
    results = search_characters("student")
    print(f"Found {len(results)} characters")
    for r in results:
        print(f"- {r.metadata.get('name', 'Unknown')}")
