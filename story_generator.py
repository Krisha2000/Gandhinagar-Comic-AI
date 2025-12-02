"""
Story Generator Module
Generates complete stories from short user ideas using Gemini + RAG
"""
import google.generativeai as genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config

# Configure Gemini
genai.configure(api_key=config.GOOGLE_API_KEY)

def load_retriever():
    """Load ChromaDB retriever for character context"""
    try:
        embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
        vectorstore = Chroma(
            persist_directory=config.VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="gandhinagar_school"
        )
        return vectorstore.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        print(f"[WARN] RAG retriever failed: {e}")
        return None

def generate_story(story_idea: str) -> str:
    """
    Generate a complete, safe story from a short idea.
    
    Args:
        story_idea: Short story concept (e.g., "Kabir woke up late for school")
    
    Returns:
        Full story text (1-3 paragraphs, suitable for 6-panel comic)
    """
    retriever = load_retriever()
    context = ""
    
    # Get character context from RAG
    if retriever:
        try:
            docs = retriever.invoke(story_idea)
            context = "\n\n".join([d.page_content for d in docs])
        except Exception as e:
            print(f"[WARN] RAG query failed: {e}")
    
    # Build prompt
    prompt = f"""You are a creative storyteller for an all-ages comic strip.

CONTEXT (Characters and Settings):
{context if context else "Use generic school characters and settings."}

STORY IDEA: {story_idea}

REQUIREMENTS:
1. Write a complete story (150-250 words) suitable for a 6-panel comic strip
2. Include clear visual scenes with action and emotion
3. Use dialogue to show character personality
4. Keep it funny, heartwarming, and appropriate for all ages
5. NO violence, scary content, or inappropriate themes
6. Make it visually interesting with varied scenes

Write the story now:"""

    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Story generation failed: {e}")

if __name__ == "__main__":
    # Test
    test_idea = "Kabir tries to sneak a puppy into class"
    print(generate_story(test_idea))