# Gandhinagar Comic AI

An intelligent AI-powered comic generation platform that leverages **Multi-RAG (Retrieval Augmented Generation)** architecture to create consistent, character-driven comic strips. Built for Gandhinagar School, this application combines the power of vector databases, large language models, and generative AI to provide a complete end-to-end comic creation workflow.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Multi-RAG Architecture](#multi-rag-architecture)
- [Features](#features)
- [How It Works](#how-it-works)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Use Cases](#use-cases)
- [Contributing](#contributing)

---

## Overview

**Gandhinagar Comic AI** is a revolutionary tool designed to help comic book creators, storytellers, and educators create professional-quality comic strips with AI assistance. The platform uses a **Multi-RAG (Multi-Modal Retrieval Augmented Generation)** system that maintains character consistency, retrieves relevant visual assets, and generates contextually accurate stories and images.

### Why Multi-RAG?

Traditional AI image generators struggle with **character consistency** across multiple panels. Our Multi-RAG approach solves this by:

1. **Storing character data** (descriptions, personalities, visual references) in a vector database
2. **Retrieving relevant character information** when generating new scenes
3. **Augmenting AI prompts** with retrieved context to ensure consistency
4. **Supporting multi-modal retrieval** (text, images, and metadata)

This ensures that your characters look the same across all comic panels and stories!

---

## Multi-RAG Architecture

### What is Multi-RAG?

**Multi-RAG** (Multi-Modal Retrieval Augmented Generation) is an advanced AI architecture that combines:

- **Vector Database (ChromaDB)**: Stores character descriptions, visual features, personalities, and story archives
- **Semantic Search**: Uses HuggingFace embeddings to find relevant characters based on natural language queries
- **Context Augmentation**: Retrieves character data and injects it into AI prompts for consistent generation
- **Multi-Modal Support**: Handles both text (descriptions, stories) and images (character references, generated panels)

### How Multi-RAG Benefits Comic Creators

#### 1. **Character Consistency**
Traditional AI generators create different-looking characters each time. With Multi-RAG:
- Character descriptions are stored in the vector database
- When generating a new panel, the system retrieves the exact character details
- AI uses these details to maintain visual consistency across all panels

#### 2. **Intelligent Character Retrieval**
Ask questions like "Who is Kabir?" and the system:
- Searches the vector database for relevant character information
- Retrieves character metadata, descriptions, and reference images
- Provides comprehensive answers with visual references

#### 3. **Story Continuity**
- Approved stories are automatically indexed in the RAG database
- Future story generation can reference past events and characters
- Creates a persistent, evolving comic universe

#### 4. **Smart Image Generation**
When you request "Show me Priya helping Kabir with homework":
- System identifies characters "Priya" and "Kabir" from the vector database
- Retrieves their visual descriptions and reference images
- Generates a scene with both characters looking exactly as defined

### RAG Workflow

```
User Query → Vector Search → Retrieve Character Data → Augment Prompt → Generate Image/Text → Display Result
```

**Example:**
```
Query: "Create a scene with Kabir running late to school"
↓
Vector DB Search: Finds "Kabir" character data
↓
Retrieved Context: "Kabir - Male student, messy hair, school uniform, backpack, worried expression"
↓
Augmented Prompt: "Comic panel showing Kabir (male student with messy hair, school uniform, backpack, worried expression) running late to school, morning setting, dynamic action pose"
↓
Generated Image: Consistent character appearance matching stored description
```

---

## Features

### 1. Character Studio
**Create and manage your comic universe's characters**

- **Upload Reference Images**: Add 1-3 reference images of your character
- **Generate from Description**: Describe your character and let AI create their reference image
- **Automatic Indexing**: Characters are automatically added to the RAG vector database
- **Rich Metadata**: Store name, role, age, visual description, personality, and tags

**How it works:**
1. User provides character details (name, role, visual description)
2. System generates or stores reference images
3. Character data is embedded using HuggingFace embeddings
4. Vector representation is stored in ChromaDB for fast retrieval
5. Character becomes available for all future story and image generation

**Benefits for Comic Creators:**
- Build a persistent character library
- Maintain visual consistency across all comics
- Quickly search and retrieve character information
- Generate new characters with AI assistance

---

### 2. Story Lab
**Generate AI-powered stories or write your own**

- **AI Story Generation**: Provide a simple idea, get a full narrative
- **Story Editing**: Review and modify AI-generated stories
- **6-Panel Breakdown**: Automatically converts stories into 6 comic panels
- **RAG-Enhanced Prompts**: Each panel prompt includes retrieved character details
- **Story Archiving**: Approved stories are saved to the vector database

**How it works:**
1. User enters a story idea (e.g., "Kabir wakes up late for school")
2. Google Gemini LLM generates a complete story narrative
3. User reviews and can edit the story
4. Upon approval, the story is broken down into 6 scenes
5. For each scene, the system:
   - Identifies mentioned characters
   - Retrieves character data from RAG database
   - Generates detailed image prompts with character descriptions
   - Specifies camera angles, emotions, and dialogue
6. Story is indexed in the vector database for future reference

**Benefits for Comic Creators:**
- Rapid story ideation and development
- Consistent character usage across panels
- Automatic scene breakdown and composition
- Story archive for continuity and reference

---

### 3. Comic Factory
**Transform stories into visual 6-panel comic strips**

- **Automated Image Generation**: Creates 6 comic panels from approved prompts
- **Character-Consistent Rendering**: Uses RAG-retrieved character data
- **Dialogue Overlay**: Automatically adds speech bubbles with dialogue
- **Progress Tracking**: Real-time generation status for each panel
- **Download Options**: Export individual panels or complete strips

**How it works:**
1. System takes the 6 approved prompts from Story Lab
2. For each panel:
   - Retrieves character visual descriptions from RAG database
   - Constructs a detailed image prompt with character details
   - Sends prompt to Pollinations.ai API for image generation
   - Receives generated image
   - Overlays dialogue text with proper formatting
   - Saves panel to local storage
3. Displays all 6 panels in a grid layout
4. Provides download buttons for each panel

**Benefits for Comic Creators:**
- Automated panel generation saves hours of manual work
- Consistent character appearance across all panels
- Professional dialogue overlay
- Easy export for printing or digital distribution

---

### 4. Ask the Universe (RAG Q&A)
**Chat with your comic universe using intelligent retrieval**

- **Natural Language Queries**: Ask questions in plain English
- **Character Information Retrieval**: Get detailed character bios
- **Visual References**: Automatically displays character images
- **Story Context**: Retrieves information from archived stories
- **Image Generation on Demand**: Request character images in specific scenarios

**How it works:**
1. User asks a question (e.g., "Who is Priya?")
2. Question is embedded using HuggingFace embeddings
3. Vector similarity search finds relevant documents in ChromaDB
4. Top 5 most relevant character/story documents are retrieved
5. Retrieved context is sent to Google Gemini LLM
6. LLM generates a comprehensive answer using the context
7. If character images are mentioned, they're automatically displayed
8. If user requests a new image, system generates it using character descriptions

**Benefits for Comic Creators:**
- Quick character reference lookup
- Maintain story continuity by checking past events
- Generate character images in new scenarios
- Build a knowledge base of your comic universe

---

### 5. Story Archive
**Manage and browse your story collection**

- **Persistent Storage**: All approved stories are saved
- **RAG Integration**: Stories are indexed for future retrieval
- **Search and Browse**: View all created stories
- **Story Management**: Delete unwanted stories
- **Continuity Reference**: Use past stories to inform new creations

**How it works:**
1. When a story is approved in Story Lab, it's saved with metadata
2. Story text is embedded and stored in ChromaDB
3. Story ID is generated for tracking and deletion
4. Stories can be retrieved by semantic search
5. Users can view all stories in chronological order
6. Deletion removes story from both file system and vector database

**Benefits for Comic Creators:**
- Build a persistent comic universe
- Reference past stories for continuity
- Track character development over time
- Maintain a portfolio of your work

---

### 6. Image Magic
**Advanced AI image manipulation and generation**

#### Tab 1: Text to Image
- **Custom Scene Generation**: Describe any scene and generate it
- **Character Integration**: Select characters from your library
- **Style Options**: Choose from Comic Book, Cinematic, Anime, Watercolor, Pixel Art
- **RAG-Enhanced**: Automatically includes character descriptions

**How it works:**
1. User selects characters from their library
2. User describes the desired scene
3. System retrieves visual descriptions for selected characters
4. Constructs prompt: Scene description + Character details + Style + Safety filters
5. Sends to Pollinations.ai for generation
6. Returns high-quality image

#### Tab 2: Reimagine Image
- **Image-to-Image with Characters**: Upload any image and recreate it with your characters
- **Google Gemini Vision**: Analyzes uploaded image to understand composition
- **Character Substitution**: Replaces generic characters with your defined ones
- **Scene Preservation**: Maintains original setting and composition

**How it works:**
1. User uploads a reference image
2. User selects which characters to use
3. Image is sent to Google Gemini Vision API
4. Gemini analyzes the image and generates a detailed description
5. System retrieves selected character descriptions from RAG database
6. Constructs new prompt: Original scene + Character substitutions
7. Generates new image with your characters in the original scene

#### Tab 3: Image to Story
- **Reverse Engineering**: Upload an image and get a story
- **Vision-to-Text**: Google Gemini Vision describes the image
- **Story Generation**: Creates a narrative based on the image
- **Story Lab Integration**: Send generated story directly to Story Lab

**How it works:**
1. User uploads an image
2. Image is analyzed by Google Gemini Vision
3. Gemini generates a detailed narrative based on the image
4. Story is displayed for user review
5. User can send story to Story Lab for comic generation

**Benefits for Comic Creators:**
- Unlimited creative possibilities
- Remix existing artwork with your characters
- Generate inspiration from images
- Maintain character consistency in any scenario

---

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Krisha2000/Gandhinagar-Comic-AI.git
   cd Gandhinagar-Comic-AI
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   
   Open `.env` and add your API key:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application:**
   Open your browser and navigate to `http://localhost:8501`

---

## Project Structure

```
Gandhinagar_Comic_AI/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration and constants
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── character_manager.py        # Character creation and management
├── story_generator.py          # AI story generation (Gemini)
├── prompt_generator.py         # Comic prompt generation
├── comic_renderer.py           # Image generation (Pollinations API)
├── image_analyzer.py           # Image analysis (Gemini Vision)
│
├── rag_index.py               # RAG vector database management
├── qa_engine.py               # RAG-based Q&A system
├── story_manager.py           # Story archiving and retrieval
│
└── gandhinagar_school_project/ # Data directory
    ├── characters/            # Character JSON and images
    ├── comics/                # Generated comic strips
    ├── stories/               # Archived stories
    └── chroma_db/             # ChromaDB vector database
```

### Key Modules

#### `rag_index.py` - Vector Database Management
- Initializes ChromaDB with HuggingFace embeddings
- Adds characters and stories to the vector database
- Performs semantic similarity search
- Manages document deletion and updates

#### `qa_engine.py` - RAG Q&A Engine
- Handles natural language queries
- Retrieves relevant context from vector database
- Generates answers using Google Gemini
- Returns character images and information

#### `character_manager.py` - Character Management
- Creates characters from images or descriptions
- Stores character metadata and references
- Integrates with RAG index for searchability

#### `comic_renderer.py` - Image Generation
- Interfaces with Pollinations.ai API
- Generates images from text prompts
- Adds dialogue overlays to panels
- Handles image caching and storage

#### `image_analyzer.py` - Vision AI
- Analyzes images using Google Gemini Vision
- Generates descriptions and stories from images
- Recreates images with character substitution

---

## Technologies

### AI & Machine Learning
- **Google Gemini 1.5 Flash**: Large Language Model for story generation and Q&A
- **Google Gemini Vision**: Multi-modal AI for image analysis
- **HuggingFace Embeddings**: Sentence transformers for vector embeddings (`all-MiniLM-L6-v2`)
- **ChromaDB**: Vector database for semantic search and retrieval

### Image Generation
- **Pollinations.ai**: Free, high-quality AI image generation API
- **PIL (Pillow)**: Image processing and manipulation

### Web Framework
- **Streamlit**: Interactive web application framework
- **Python 3.8+**: Core programming language

### Data Storage
- **JSON**: Character and story metadata
- **ChromaDB**: Persistent vector storage
- **Local File System**: Image and comic storage

---

## Use Cases

### For Comic Book Creators
- **Rapid Prototyping**: Quickly visualize story ideas before committing to manual drawing
- **Character Consistency**: Maintain consistent character designs across issues
- **Story Planning**: Generate and archive story arcs with full continuity
- **Reference Library**: Build a searchable database of characters and stories

### For Educators
- **Creative Writing**: Students can visualize their stories as comics
- **Character Development**: Teach character design and consistency
- **Storytelling**: Practice narrative structure with immediate visual feedback
- **Digital Literacy**: Learn about AI, databases, and modern technology

### For Content Creators
- **Social Media Content**: Generate comic strips for Instagram, Twitter, etc.
- **Storyboarding**: Create visual storyboards for videos or animations
- **Concept Art**: Explore different visual styles and compositions
- **Portfolio Building**: Create a diverse portfolio of comic work

---

## How Multi-RAG Makes This Possible

Traditional AI image generators treat each request independently, leading to inconsistent results. Our Multi-RAG architecture creates a **persistent memory** for your comic universe:

1. **Character Memory**: Once a character is created, they're never forgotten
2. **Visual Consistency**: Character descriptions are retrieved and used in every generation
3. **Story Continuity**: Past stories inform future creations
4. **Intelligent Search**: Find characters and stories using natural language
5. **Context-Aware Generation**: Every image and story is generated with full knowledge of your comic universe

This transforms AI from a random generator into an **intelligent creative assistant** that understands and maintains your unique comic world.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is open source and available for educational and creative purposes.

---

## Acknowledgments

- **Google Gemini**: For powerful LLM and Vision AI capabilities
- **Pollinations.ai**: For free, high-quality image generation
- **ChromaDB**: For efficient vector storage and retrieval
- **HuggingFace**: For state-of-the-art embedding models
- **Streamlit**: For making web app development simple and beautiful

---

## Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.


