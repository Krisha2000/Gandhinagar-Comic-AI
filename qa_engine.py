"""
QA Engine Module
Handles RAG-based Q&A with character image retrieval
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
        # Fetch more documents to ensure we get relevant images
        return vectorstore.as_retriever(search_kwargs={"k": 4})
    except Exception as e:
        print(f"[WARN] RAG failed: {e}")
        return None

def answer_question(query: str) -> dict:
    """
    Answer a user question using RAG and return answer + images.
    
    Args:
        query: User question
    
    Returns:
        Dictionary with 'answer' (str) and 'images' (list of paths)
    """
    import os
    import comic_renderer
    
    retriever = load_retriever()
    context = ""
    relevant_images = []
    character_data_list = []
    
    if retriever:
        try:
            docs = retriever.invoke(query)
            
            # Extract text context and images
            context_parts = []
            seen_images = set()
            
            for doc in docs:
                context_parts.append(doc.page_content)
                
                # Try to parse metadata from page_content or use doc.metadata
                try:
                    char_data = None
                    
                    # New format: has "Full Data:" marker
                    if "Full Data:" in doc.page_content:
                        json_str = doc.page_content.split("Full Data:", 1)[1].strip()
                        char_data = json.loads(json_str)
                    # Old format or truncated: use source file from metadata
                    elif doc.metadata.get("type") == "character" and "source" in doc.metadata:
                        source_file = doc.metadata["source"]
                        if os.path.exists(source_file) and source_file.endswith('.json'):
                            with open(source_file, 'r', encoding='utf-8') as f:
                                char_data = json.load(f)
                    
                    if char_data:
                        character_data_list.append(char_data)
                        
                        # Get images if they exist in the data
                        if "image_paths" in char_data and char_data["image_paths"]:
                            for img_path in char_data["image_paths"]:
                                # Convert relative paths to absolute
                                if not os.path.isabs(img_path):
                                    img_path = os.path.abspath(img_path)
                                
                                if img_path not in seen_images and os.path.exists(img_path):
                                    relevant_images.append(img_path)
                                    seen_images.add(img_path)
                except Exception as e:
                    pass
            
            context = "\n\n".join(context_parts)
            
        except Exception as e:
            print(f"[WARN] Retrieval failed: {e}")
            context = "No specific context found."

    # Check if user is asking for an image/picture
    image_request_keywords = ["picture", "image", "photo", "show me", "give me a picture", "what does", "look like", "give image", "show image"]
    is_image_request = any(keyword in query.lower() for keyword in image_request_keywords)
    
    # Generate images on-demand if user requests them
    if is_image_request and character_data_list:
        try:
            print(f"[*] Generating image for query: {query}")
            
            # Build visual description from retrieved character data
            character_descriptions = []
            character_names = []
            
            for char_data in character_data_list[:3]:  # Max 3 characters
                char_name = char_data.get("name", "character")
                character_names.append(char_name)
                
                # Build visual description
                visual_desc = ""
                if "visual_description" in char_data:
                    visual_desc = char_data["visual_description"]
                elif "visual_features" in char_data:
                    # Old format - build description from features
                    features = char_data["visual_features"]
                    parts = []
                    if isinstance(features, dict):
                        for key, value in features.items():
                            if isinstance(value, str):
                                parts.append(value)
                    visual_desc = ", ".join(parts)
                
                role = char_data.get("role", "student")
                
                if visual_desc:
                    character_descriptions.append(f"{char_name} ({role}): {visual_desc}")
            
            if character_descriptions:
                # Create image prompt based on query context
                if len(character_names) > 1:
                    # Multiple characters - group scene
                    names_str = ", ".join(character_names)
                    image_prompt = f"""Group scene with {names_str} from Gandhinagar School. {'; '.join(character_descriptions)}. Indian school setting, all wearing school uniforms. {config.SAFETY_SUFFIX}"""
                else:
                    # Single character portrait
                    char_name = character_names[0]
                    image_prompt = f"""Character portrait: {character_descriptions[0]}. Indian school student in school uniform. Upper body shot, clear face, friendly expression. {config.SAFETY_SUFFIX}"""
                
                # Generate image using Pollinations
                img = comic_renderer.generate_image_from_prompt(image_prompt, panel_num=0)
                
                if img:
                    # Save generated image
                    import tempfile
                    import uuid
                    temp_dir = tempfile.gettempdir()
                    img_filename = f"qa_generated_{uuid.uuid4().hex[:8]}.png"
                    img_path = os.path.join(temp_dir, img_filename)
                    img.save(img_path)
                    relevant_images.append(img_path)
                    print(f"[✓] Generated image saved to {img_path}")
        except Exception as e:
            print(f"[WARN] Failed to generate image: {e}")

    # Generate Answer
    # Add info about generated images to the prompt
    image_info = ""
    if relevant_images:
        image_info = f"\n\n[SYSTEM NOTE: {len(relevant_images)} image(s) have been generated and will be shown to the user below your response.]"
    
    prompt = f"""You are the chronicler of the Gandhinagar School Universe.
    
CONTEXT FROM DATABASE:
{context}{image_info}

USER QUESTION: {query}

INSTRUCTIONS:
1. Answer the question based ONLY on the context provided.
2. If the user asks for a picture/image/photo and images are being provided (see SYSTEM NOTE), acknowledge this enthusiastically (e.g., "Here is [Name]!" or "Here are your requested characters!").
3. If the answer is not in the context, say you don't know but suggest creating a character.
4. Be helpful, fun, and engaging.
5. Keep the answer concise (2-3 sentences).

ANSWER:"""

    try:
        model = genai.GenerativeModel(config.GEMINI_MODEL)
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        return {
            "answer": answer,
            "images": relevant_images[:3]  # Return top 3 images
        }
        
    except Exception as e:
        return {
            "answer": f"I encountered an error consulting the archives: {e}",
            "images": []
        }


if __name__ == "__main__":
    # Test
    print(answer_question("Who is Kabir?"))
