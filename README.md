# Gandhinagar Comic AI

An AI-powered comic generation platform for Gandhinagar School. This application allows users to create characters, generate stories, and produce comic strips using RAG (Retrieval Augmented Generation) and Generative AI.

## Features

- **Character Studio**: Create and manage characters with visual descriptions and reference images.
- **Story Lab**: Generate stories using AI or write your own.
- **Comic Factory**: Turn stories into 6-panel comic strips with consistent characters.
- **Ask the Universe**: Chat with your characters and ask questions about the world.
- **Image Magic**: Generate custom images, reimagine existing images with your characters, and turn images into stories.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd Gandhinagar_Comic_AI
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Copy `.env.example` to `.env` and add your API keys.
    ```bash
    cp .env.example .env
    ```
    Open `.env` and fill in:
    - `GOOGLE_API_KEY`: Your Google Gemini API Key.

4.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

## Project Structure

- `app.py`: Main Streamlit application.
- `qa_engine.py`: Handles RAG-based Q&A and image retrieval.
- `comic_renderer.py`: Generates images using Pollinations API.
- `image_analyzer.py`: Handles image analysis and recreation using Gemini Vision.
- `character_manager.py`: Manages character data and storage.
- `story_generator.py`: Generates stories using Gemini.
- `rag_index.py`: Manages the vector database for RAG.
- `gandhinagar_school_project/`: Directory containing the vector database and character data.

## Technologies

- **Frontend**: Streamlit
- **LLM**: Google Gemini
- **Image Generation**: Pollinations.ai
- **Vector DB**: ChromaDB
- **Embeddings**: HuggingFace Embeddings
