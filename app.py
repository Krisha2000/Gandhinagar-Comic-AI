"""
Gandhinagar Comic AI - Streamlit Application
Complete end-to-end comic generation system with RAG and safety controls
"""
import streamlit as st
import os
import json
from PIL import Image
import uuid
from datetime import datetime

# Import our modules
import config
import story_generator
import prompt_generator
import comic_renderer
import character_manager
import rag_index
import qa_engine
import story_manager
import image_analyzer

# Page Configuration
st.set_page_config(
    page_title="Gandhinagar Comic AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_story' not in st.session_state:
    st.session_state.current_story = None
if 'current_prompts' not in st.session_state:
    st.session_state.current_prompts = None
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = None

# Sidebar Navigation
st.sidebar.title("Gandhinagar Comic AI")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["Character Studio", "Story Lab", "Comic Factory", "Ask the Universe", "Story Archive", "Image Magic"],
    label_visibility="collapsed"
)

# ============================================================================
# PAGE 1: CHARACTER STUDIO
# ============================================================================
if page == "Character Studio":
    st.title("Character Studio")
    st.markdown("Add new characters to your comic universe")
    
    # Display existing characters
    with st.expander("Existing Characters", expanded=False):
        characters = character_manager.list_all_characters()
        if characters:
            cols = st.columns(4)
            for i, char in enumerate(characters):
                with cols[i % 4]:
                    st.markdown(f"**{char.get('name', 'Unknown')}**")
                    st.caption(char.get('role', ''))
                    
                    # Show first image if available
                    img_paths = char.get('image_paths', [])
                    if img_paths and os.path.exists(img_paths[0]):
                        st.image(img_paths[0], use_container_width=True)
                    
                    tags = char.get('tags', [])
                    if tags:
                        st.caption(f"Tags: {', '.join(tags)}")
        else:
            st.info("No characters yet. Add your first character below!")
    
    st.markdown("---")
    
    # Add new character
    st.subheader("Add New Character")
    
    add_method = st.radio(
        "How would you like to add the character?",
        ["Upload Images", "Generate from Description"],
        horizontal=True
    )
    
    with st.form("add_character_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            char_name = st.text_input("Character Name*", placeholder="e.g., Priya Sharma")
            char_role = st.text_input("Role/Archetype*", placeholder="e.g., The Class Topper")
            char_age = st.text_input("Age (optional)", placeholder="e.g., 16")
        
        with col2:
            char_visual = st.text_area(
                "Visual Description*",
                placeholder="e.g., Long black hair in ponytail, round glasses, school uniform with badge, energetic expression",
                height=100
            )
            char_personality = st.text_area(
                "Personality (optional)",
                placeholder="e.g., Competitive, helpful, loves science",
                height=100
            )
        
        char_tags = st.text_input(
            "Tags (comma-separated)",
            placeholder="e.g., student, school, female, teenager"
        )
        
        # Image upload (only shown if method is "Upload Images")
        uploaded_files = None
        if add_method == "Upload Images":
            uploaded_files = st.file_uploader(
                "Upload Reference Images",
                type=["png", "jpg", "jpeg"],
                accept_multiple_files=True,
                help="Upload 1-3 reference images of the character"
            )
        
        submitted = st.form_submit_button("Create Character", use_container_width=True)
        
        if submitted:
            if not char_name or not char_role or not char_visual:
                st.error("Please fill in all required fields (marked with *)")
            elif add_method == "Upload Images" and not uploaded_files:
                st.error("Please upload at least one image")
            else:
                try:
                    tags_list = [t.strip() for t in char_tags.split(",")] if char_tags else ["student", "school"]
                    
                    with st.spinner(f"Creating {char_name}..."):
                        if add_method == "Upload Images":
                            char_data = character_manager.add_character_from_images(
                                name=char_name,
                                role=char_role,
                                description=char_visual,
                                image_files=uploaded_files,
                                age=char_age,
                                personality=char_personality,
                                tags=tags_list
                            )
                        else:
                            char_data = character_manager.add_character_from_description(
                                name=char_name,
                                role=char_role,
                                description=char_visual,
                                age=char_age,
                                personality=char_personality,
                                tags=tags_list
                            )
                    
                    st.success(f"Successfully created {char_name}!")
                    st.balloons()
                    
                    # Show created character
                    if char_data.get('image_paths'):
                        st.image(char_data['image_paths'][0], caption=f"{char_name} - {char_role}", width=300)
                    
                    st.info("Character added to the RAG database. You can now use them in stories!")
                    # Refresh the page to reload the character list
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to create character: {e}")

# ============================================================================
# PAGE 2: STORY LAB
# ============================================================================
elif page == "Story Lab":
    st.title("Story Lab")
    st.markdown("Generate and approve stories for your comics")
    
    # Step 1: Story Idea Input
    st.subheader("Step 1: Enter Story Idea")
    story_idea = st.text_area(
        "What's your story about?",
        placeholder="e.g., Kabir woke up late for school and panicked\ne.g., Rohan tries to help Kabir with homework but Kabir falls asleep\ne.g., A cricket match goes hilariously wrong",
        height=100,
        help="Enter a short story concept. The AI will expand it into a full story."
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("Generate Story", use_container_width=True, type="primary")
    
    if generate_btn and story_idea:
        with st.spinner("Writing your story..."):
            try:
                story_text = story_generator.generate_story(story_idea)
                st.session_state.current_story = story_text
                st.session_state.current_prompts = None  # Reset prompts
                st.session_state.generated_images = None  # Reset images
            except Exception as e:
                st.error(f"Story generation failed: {e}")
    
    # Step 2: Review and Edit Story
    if st.session_state.current_story:
        st.markdown("---")
        st.subheader("Step 2: Review & Edit Story")
        
        edited_story = st.text_area(
            "Generated Story (you can edit it)",
            value=st.session_state.current_story,
            height=250,
            help="Feel free to modify the story before generating comic prompts"
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            approve_btn = st.button("Approve & Generate Prompts", use_container_width=True, type="primary")
        
        if approve_btn:
            st.session_state.current_story = edited_story
            
            with st.spinner("Creating 6-panel comic prompts..."):
                try:
                    prompts = prompt_generator.generate_comic_prompts(edited_story)
                    st.session_state.current_prompts = prompts
                    
                    # Save story using story_manager
                    story_manager.save_story(edited_story)
                    st.success("Comic prompts generated and story saved to archive!")
                except Exception as e:
                    st.error(f"Prompt generation failed: {e}")
    
    # Step 3: Review Prompts
    if st.session_state.current_prompts:
        st.markdown("---")
        st.subheader("Step 3: Review Comic Prompts")
        st.info("These are the 6 scenes that will be generated. Review them before creating the comic.")
        
        for prompt_data in st.session_state.current_prompts:
            with st.expander(f"Panel {prompt_data.get('panel', '?')} - {prompt_data.get('scene', 'Scene')}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Scene:** {prompt_data.get('scene', 'N/A')}")
                    st.markdown(f"**Characters:** {prompt_data.get('characters', 'N/A')}")
                    st.markdown(f"**Dialogue:** {prompt_data.get('dialogue', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Camera:** {prompt_data.get('camera_angle', 'N/A')}")
                    st.markdown(f"**Emotion:** {prompt_data.get('emotion', 'N/A')}")
                
                st.caption(f"**Image Prompt:** {prompt_data.get('image_prompt', 'N/A')[:200]}...")
        
        st.success("Prompts ready! Go to **Comic Factory** to generate images.")

# ============================================================================
# PAGE 3: COMIC FACTORY
# ============================================================================
elif page == "Comic Factory":
    st.title("Comic Factory")
    st.markdown("Generate your 6-panel comic strip")
    
    if not st.session_state.current_prompts:
        st.warning("No approved prompts found. Please complete the **Story Lab** workflow first.")
        st.info("Go to **Story Lab** → Enter idea → Generate story → Approve → Generate prompts")
    else:
        # Show story summary
        with st.expander("Story Summary", expanded=False):
            st.write(st.session_state.current_story)
        
        st.markdown("---")
        
        # Generate button
        if not st.session_state.generated_images:
            st.subheader("Ready to Generate Comic")
            st.info(f"Will generate {len(st.session_state.current_prompts)} panels using Pollinations AI")
            
            if st.button("Generate Comic Strip", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Create output directory
                    comic_id = str(uuid.uuid4())[:8]
                    output_dir = os.path.join(config.COMICS_DIR, comic_id)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Generate images
                    image_paths = []
                    total_panels = len(st.session_state.current_prompts)
                    
                    for i, prompt_data in enumerate(st.session_state.current_prompts):
                        status_text.text(f"Generating Panel {i+1}/{total_panels}...")
                        progress_bar.progress((i) / total_panels)
                        
                        panel_num = prompt_data.get('panel', i+1)
                        image_prompt = prompt_data.get('image_prompt', '')
                        dialogue = prompt_data.get('dialogue', '')
                        
                        # Generate image
                        img = comic_renderer.generate_image_from_prompt(image_prompt, panel_num)
                        
                        if img:
                            # Add dialogue
                            if dialogue:
                                img = comic_renderer.add_dialogue_overlay(img, dialogue)
                            
                            # Save
                            save_path = os.path.join(output_dir, f"panel_{panel_num}.png")
                            img.save(save_path)
                            image_paths.append(save_path)
                    
                    progress_bar.progress(1.0)
                    status_text.text("All panels generated!")
                    
                    # Save metadata
                    metadata = {
                        "id": comic_id,
                        "created_at": datetime.now().isoformat(),
                        "story": st.session_state.current_story,
                        "prompts": st.session_state.current_prompts,
                        "image_paths": image_paths
                    }
                    
                    with open(os.path.join(output_dir, "metadata.json"), 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    st.session_state.generated_images = image_paths
                    st.success("Comic strip generated successfully!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Comic generation failed: {e}")
        
        # Display generated comic
        if st.session_state.generated_images:
            st.markdown("---")
            st.subheader("Your Comic Strip")
            
            # Display in grid
            cols = st.columns(3)
            for i, img_path in enumerate(st.session_state.generated_images):
                with cols[i % 3]:
                    if os.path.exists(img_path):
                        st.image(img_path, caption=f"Panel {i+1}", use_container_width=True)
            
            # Download buttons
            st.markdown("---")
            st.subheader("Download")
            
            download_cols = st.columns(len(st.session_state.generated_images))
            for i, img_path in enumerate(st.session_state.generated_images):
                with download_cols[i]:
                    if os.path.exists(img_path):
                        with open(img_path, "rb") as f:
                            st.download_button(
                                f"Panel {i+1}",
                                f.read(),
                                file_name=f"panel_{i+1}.png",
                                mime="image/png",
                                use_container_width=True
                            )

# ============================================================================
# PAGE 4: ASK THE UNIVERSE (RAG Q&A)
# ============================================================================
elif page == "Ask the Universe":
    st.title("Ask the Universe")
    st.markdown("Ask questions about your characters and world!")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "images" in message and message["images"]:
                cols = st.columns(3)
                for i, img_path in enumerate(message["images"]):
                    with cols[i % 3]:
                        if os.path.exists(img_path):
                            st.image(img_path, width=200)

    # Chat input
    if prompt := st.chat_input("Who is Kabir?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Consulting the archives..."):
                response = qa_engine.answer_question(prompt)
                
                answer_text = response.get("answer", "I don't know.")
                images = response.get("images", [])
                
                st.markdown(answer_text)
                
                if images:
                    st.markdown("**Related Visuals:**")
                    cols = st.columns(3)
                    for i, img_path in enumerate(images):
                        with cols[i % 3]:
                            if os.path.exists(img_path):
                                st.image(img_path, width=200, caption=os.path.basename(img_path))
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer_text,
                    "images": images
                })

# ============================================================================
# PAGE 5: STORY ARCHIVE
# ============================================================================
elif page == "Story Archive":
    st.title("Story Archive")
    st.markdown("View and manage your comic stories.")
    
    stories = story_manager.get_all_stories()
    
    if not stories:
        st.info("No stories archived yet. Go to **Story Lab** to create one!")
    else:
        for story in stories:
            with st.expander(f"{story.get('title', 'Untitled')} ({story.get('created_at', '')[:10]})"):
                st.write(story.get('content', ''))
                
                if st.button("Delete Story", key=f"del_{story.get('id')}"):
                    if story_manager.delete_story(story.get('id')):
                        st.success("Story deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete story.")

# ============================================================================
# PAGE 6: IMAGE MAGIC
# ============================================================================
elif page == "Image Magic":
    st.title("Image Magic")
    st.markdown("Create, Remix, and Reimagine with AI")

    # Tabs for different modes
    tab1, tab2, tab3 = st.tabs(["Text to Image", "Reimagine Image", "Image to Story"])

    # TAB 1: TEXT TO IMAGE (Existing functionality)
    with tab1:
        st.subheader("Generate from Text")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            # Character Selection
            characters = character_manager.list_all_characters()
            char_names = [c.get('name') for c in characters]
            selected_chars = st.multiselect("Include Characters", char_names, key="t2i_chars")
            
            # Custom Prompt
            custom_prompt = st.text_area(
                "Describe the scene",
                placeholder="e.g., A futuristic classroom with holographic displays...",
                height=150,
                key="t2i_prompt"
            )
            
            # Style options
            style = st.selectbox(
                "Art Style",
                ["Comic Book", "Cinematic", "Anime", "Watercolor", "Pixel Art"],
                key="t2i_style"
            )
            
            generate_btn = st.button("Generate Magic", type="primary", use_container_width=True, key="t2i_btn")

        with col2:
            if generate_btn and custom_prompt:
                with st.spinner("Weaving magic..."):
                    try:
                        # Build full prompt
                        full_prompt = custom_prompt
                        
                        # Add character visuals
                        if selected_chars:
                            char_details = []
                            for char_name in selected_chars:
                                char_data = next((c for c in characters if c.get('name') == char_name), None)
                                if char_data:
                                    desc = char_data.get('visual_description', '')
                                    if desc:
                                        char_details.append(f"{char_name}: {desc}")
                            
                            if char_details:
                                full_prompt += f". Characters: {'; '.join(char_details)}"
                        
                        # Add style
                        full_prompt += f". Style: {style}. {config.SAFETY_SUFFIX}"
                        
                        # Generate
                        img = comic_renderer.generate_image_from_prompt(full_prompt, panel_num=999)
                        
                        if img:
                            st.image(img, caption="Generated Image", use_container_width=True)
                            
                            # Save to temp for download
                            import tempfile
                            temp_dir = tempfile.gettempdir()
                            img_path = os.path.join(temp_dir, f"magic_{uuid.uuid4().hex[:8]}.png")
                            img.save(img_path)
                            
                            with open(img_path, "rb") as f:
                                st.download_button(
                                    "Download Image",
                                    f.read(),
                                    file_name="magic_image.png",
                                    mime="image/png",
                                    use_container_width=True,
                                    key="t2i_dl"
                                )
                        else:
                            st.error("Failed to generate image.")
                            
                    except Exception as e:
                        st.error(f"Error: {e}")

    # TAB 2: REIMAGINE IMAGE (New functionality)
    with tab2:
        st.subheader("Reimagine with Characters")
        st.markdown("Upload an image and recreate it using your story characters!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            uploaded_file = st.file_uploader("Upload Reference Image", type=["png", "jpg", "jpeg"], key="i2i_upload")
            
            # Character Selection
            characters = character_manager.list_all_characters()
            char_names = [c.get('name') for c in characters]
            selected_chars_i2i = st.multiselect("Use Characters", char_names, key="i2i_chars")
            
            custom_instruction = st.text_area(
                "Additional Instructions (Optional)",
                placeholder="e.g., Make it look more dramatic, change the setting to night...",
                height=100,
                key="i2i_prompt"
            )
            
            reimagine_btn = st.button("Reimagine", type="primary", use_container_width=True, key="i2i_btn")

        with col2:
            if uploaded_file:
                st.image(uploaded_file, caption="Reference Image", width=200)
            
            if reimagine_btn and uploaded_file:
                if not selected_chars_i2i:
                    st.warning("Please select at least one character to use in the reimagined image.")
                else:
                    with st.spinner("Analyzing and Recreating..."):
                        try:
                            # Save uploaded file temporarily
                            import tempfile
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                tmp_path = tmp_file.name
                            
                            # Call image analyzer
                            result = image_analyzer.recreate_with_characters(
                                image_file=tmp_path,
                                character_names=selected_chars_i2i,
                                custom_prompt=custom_instruction
                            )
                            
                            if result.get("image_path"):
                                st.success("Image Reimagined!")
                                st.image(result["image_path"], caption="Reimagined Image", use_container_width=True)
                                st.info(result.get("description", ""))
                                
                                with open(result["image_path"], "rb") as f:
                                    st.download_button(
                                        "Download Reimagined Image",
                                        f.read(),
                                        file_name="reimagined_image.png",
                                        mime="image/png",
                                        use_container_width=True,
                                        key="i2i_dl"
                                    )
                            else:
                                st.error(result.get("description", "Failed to generate image."))
                                
                            # Cleanup
                            os.unlink(tmp_path)
                            
                        except Exception as e:
                            st.error(f"Error: {e}")

    # TAB 3: IMAGE TO STORY (New functionality)
    with tab3:
        st.subheader("Inspire Story from Image")
        st.markdown("Upload an image and let AI write a story based on it!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            story_image = st.file_uploader("Upload Image for Story", type=["png", "jpg", "jpeg"], key="i2s_upload")
            generate_story_btn = st.button("Write Story", type="primary", use_container_width=True, key="i2s_btn")

        with col2:
            if story_image:
                st.image(story_image, caption="Story Inspiration", width=200)
            
            if generate_story_btn and story_image:
                with st.spinner("Analyzing image and writing story..."):
                    try:
                        # Save uploaded file temporarily
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                            tmp_file.write(story_image.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Generate story
                        story_text = image_analyzer.generate_story_from_image(tmp_path)
                        
                        st.success("Story Generated!")
                        st.text_area("Generated Story", value=story_text, height=300)
                        
                        # Option to send to Story Lab
                        if st.button("Send to Story Lab", key="send_to_lab"):
                            st.session_state.current_story = story_text
                            st.session_state.current_prompts = None
                            st.session_state.generated_images = None
                            st.success("Story sent to Story Lab! Go to 'Story Lab' to create your comic.")
                        
                        # Cleanup
                        os.unlink(tmp_path)
                        
                    except Exception as e:
                        st.error(f"Error: {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Gandhinagar Comic AI")
st.sidebar.caption("Powered by Gemini & Pollinations")
st.sidebar.caption("All content is safe-for-work and all-ages friendly")
