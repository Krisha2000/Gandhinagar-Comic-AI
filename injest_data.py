
import os
import json
import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document
import os
os.environ["CHROMADB_TELEMETRY"] = "False"

def load_json_files(directory):
    """Load all JSON files from a directory"""
    documents = []
    
    if not os.path.exists(directory):
        print(f"[WARNING] Directory not found: {directory}")
        return documents
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Convert JSON to text format
                        name = data.get("name", "Unknown")
                        content = f"Name: {name}\n" + json.dumps(data, indent=2)

                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": filepath,
                                "type": "character",
                                "name": data.get("name", "Unknown")
                            }
                        )
                        documents.append(doc)
                        print(f"   [+] Loaded: {file}")
                except Exception as e:
                    print(f"   [ERROR] Failed to load {file}: {e}")
    
    return documents

def load_text_files(directory):
    """Load all TXT files from a directory"""
    documents = []
    
    if not os.path.exists(directory):
        print(f"[WARNING] Directory not found: {directory}")
        return documents
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": filepath,
                                "type": "text"
                            }
                        )
                        documents.append(doc)
                        print(f"   [+] Loaded: {file}")
                except Exception as e:
                    print(f"   [ERROR] Failed to load {file}: {e}")
    
    return documents

def ingest_gandhinagar_data():
    """Main function to ingest all data into ChromaDB"""
    
    print("\n" + "="*60)
    print("  GANDHINAGAR SCHOOL PROJECT - DATA INGESTION")
    print("="*60 + "\n")
    
    # Define paths
    base_dir = "gandhinagar_school_project"
    characters_dir = os.path.join(base_dir, "data", "1_characters")
    families_dir = os.path.join(base_dir, "data", "2_families")
    locations_dir = os.path.join(base_dir, "data", "3_locations")
    vector_db_dir = os.path.join(base_dir, "vector_db")
    
    # Check if base directory exists
    if not os.path.exists(base_dir):
        print(f"[ERROR] Project directory '{base_dir}' not found!")
        print(f"[INFO] Please run setup.py first to create the project structure.")
        return
    
    # Load all documents
    print("[*] Loading Character Data...")
    character_docs = load_json_files(characters_dir)
    
    print("\n[*] Loading Family Data...")
    family_docs = load_text_files(families_dir)
    
    print("\n[*] Loading Location Data...")
    location_docs = load_text_files(locations_dir)
    
    # Combine all documents
    all_documents = character_docs + family_docs + location_docs
    
    if not all_documents:
        print("\n[ERROR] No documents found to ingest!")
        return
    
    print(f"\n[*] Total Documents Loaded: {len(all_documents)}")
    
    # Initialize embeddings (using free HuggingFace embeddings)
    print("\n[*] Initializing Embeddings Model...")
    print("    (First run will download the model - may take a few minutes)")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Split documents if needed (optional for small documents)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    split_docs = text_splitter.split_documents(all_documents)
    print(f"[*] Documents split into {len(split_docs)} chunks")
    
    # Create or load ChromaDB
    print(f"\n[*] Creating Vector Database at: {vector_db_dir}")
    
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=vector_db_dir,
        collection_name="gandhinagar_school"
    )
    
    print("\n" + "="*60)
    print("  [SUCCESS] Data Ingestion Complete!")
    print("="*60)
    print(f"\n[INFO] Vector database saved to: {vector_db_dir}")
    print(f"[INFO] Total chunks stored: {len(split_docs)}")
    print("\n[NEXT STEP] You can now query this database!")
    print("            Try running: python query_data.py\n")

if __name__ == "__main__":
    ingest_gandhinagar_data()