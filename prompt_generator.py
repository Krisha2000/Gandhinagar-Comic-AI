"""
Prompt Generator Module
Converts stories into 6 detailed scene prompts with safety controls
"""
import json
import google.generativeai as genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config

genai.configure(api_key=config.GOOGLE_API_KEY)

def load_retriever():
    """Load ChromaDB retriever"""
    try:
        embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
        vectorstore = Chroma(
            persist_directory=config.VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="gandhinagar_school"
        )
        return vectorstore.as_retriever(search_kwargs={"k": 6})
    except Exception as e:
        print(f"[WARN] RAG failed: {e}")
        return None

def generate_comic_prompts(story_text: str) -> list:
    """
    Generate 6 detailed scene prompts from a story.
    
    Args:
        story_text: Complete story text
    
    Returns:
        List of 6 prompt dictionaries with scene details
    """
    retriever = load_retriever()
    context = ""
    
    # Get character visual details from RAG
    if retriever:
        try:
            docs = retriever.invoke(story_text)
            context = "\n\n".join([d.page_content for d in docs])
        except Exception:
            pass
    
    system_prompt = f"""You are an expert comic book art director.

CHARACTER/SETTING CONTEXT (use for visual consistency):
{context if context else "Use generic school characters and settings."}

STORY:
{story_text}

TASK: Convert this story into exactly 6 comic panel prompts.

For EACH panel, provide:
1. **scene**: What's happening (action, setting)
2. **characters**: Who appears + their visual details (clothing, hair, expressions, poses)
3. **dialogue**: Exact dialogue text (if any)
4. **camera_angle**: Shot type (close-up, wide, over-shoulder, etc.)
5. **emotion**: Mood/feeling of the scene
6. **image_prompt**: Detailed visual description for image generation

CRITICAL SAFETY REQUIREMENTS:
- All-ages appropriate content only
- No violence, gore, or scary imagery
- No real people or copyrighted characters
- Original characters based on descriptions only

OUTPUT FORMAT (strict JSON):
[
  {{
    "panel": 1,
    "scene": "...",
    "characters": "...",
    "dialogue": "...",
    "camera_angle": "...",
    "emotion": "...",
    "image_prompt": "..."
  }},
  ...
]"""

    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        response = model.generate_content(
            contents=[{"role": "user", "parts": [system_prompt]}],
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompts = json.loads(response.text)
        
        # Add safety suffix to each image_prompt
        for prompt in prompts:
            if "image_prompt" in prompt:
                prompt["image_prompt"] = f"{prompt['image_prompt']}. {config.SAFETY_SUFFIX}"
        
        return prompts
        
    except Exception as e:
        raise Exception(f"Prompt generation failed: {e}")

if __name__ == "__main__":
    # Test
    test_story = "Kabir woke up late. He rushed to school. His teacher was angry."
    prompts = generate_comic_prompts(test_story)
    print(json.dumps(prompts, indent=2))
