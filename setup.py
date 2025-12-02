import os
import json
import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def create_gandhinagar_project():
    # 1. Define the Root Directory
    root_dir = "gandhinagar_school_project"

    # 2. Define the Folder Structure (Nested)
    directories = [
        f"{root_dir}/data/1_characters/students",
        f"{root_dir}/data/1_characters/teachers",
        f"{root_dir}/data/2_families",
        f"{root_dir}/data/3_locations",
        f"{root_dir}/data/4_images",
        f"{root_dir}/src",
        f"{root_dir}/vector_db"
    ]

    # 3. Create Directories
    print(f"[*] Starting Project Setup: {root_dir}...\n")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   [+] Created Folder: {directory}")

    # ---------------------------------------------------------
    # 4. Define Data for Files (The "Brain")
    # ---------------------------------------------------------

    # -- STUDENT: Rohan --
    rohan_data = {
        "id": "student_01",
        "name": "Rohan Patel",
        "role": "The Anxious Techie",
        "visual_features": {
            "hair": "Neatly parted, oiled",
            "accessories": "Thick black rectangular glasses, digital watch",
            "uniform": "Shirt tucked in tightly, ID card always visible"
        },
        "personality": {
            "traits": ["Logical", "Anxious", "Secretly rebellious"],
            "likes": ["Coding", "Sci-fi movies", "Thepla"],
            "catchphrase": "But madam, logically this is not possible."
        }
    }

    # -- STUDENT: Kabir --
    kabir_data = {
        "id": "student_02",
        "name": "Kabir Khan",
        "role": "The Charismatic Backbencher",
        "visual_features": {
            "hair": "Messy, windblown style",
            "accessories": "Loose tie, sleeves rolled up, friendship bands",
            "uniform": "Untucked shirt when teachers aren't looking"
        },
        "personality": {
            "traits": ["Charming", "Lazy", "Street-smart"],
            "likes": ["Cricket", "Pranks", "Sleeping in History class"],
            "catchphrase": "Relax yaar, sab set hai."
        }
    }

    # -- TEACHER: Ms. Mehta --
    mehta_data = {
        "id": "teacher_01",
        "name": "Ms. Mehta",
        "role": "Class Teacher (10-B) & English",
        "visual_features": {
            "clothing": "Cotton Saree (pastel colors)",
            "accessories": "Reading glasses on a chain, red pen"
        },
        "personality": {
            "traits": ["Strict but motherly", "Sharp observer"],
            "dialogue_style": "Mixes English with Gujarati scolding ('Beta, behave yourself')"
        }
    }

    # -- FAMILY: Patels --
    patel_family_text = """Family: The Patels (Rohan's Family)
Address: Sector 21, Government Quarters, Gandhinagar.
Father: Mr. Suresh Patel - Section Officer at Sachivalaya. Strict.
Mother: Anjali Ben - Housewife. Worries Rohan is too thin.
Context: High pressure for academic performance."""

    # -- LOCATION: School --
    school_text = """Location: Green Valley High School
City: Gandhinagar (The Green City)
Details: Huge iron gate guarded by Bahadur Kaka. Surrounded by Neem trees.
Canteen: Famous for 'Veg Puff' and 'Masala Thumbs Up'."""

    # -- PYTHON CODE: ingest_data.py (Template) --
    ingest_code = """import os
# This script will eventually load your JSON/TXT files into ChromaDB
print("Ready to ingest Gandhinagar School Data...")
"""

    # -- REQUIREMENTS.TXT --
    req_txt = """langchain
langchain-community
chromadb
openai
tiktoken
"""

    # ---------------------------------------------------------
    # 5. Write Files to Disk
    # ---------------------------------------------------------
    
    files_to_create = [
        (f"{root_dir}/data/1_characters/students/student_01_rohan.json", rohan_data, "json"),
        (f"{root_dir}/data/1_characters/students/student_02_kabir.json", kabir_data, "json"),
        (f"{root_dir}/data/1_characters/teachers/teacher_01_ms_mehta.json", mehta_data, "json"),
        (f"{root_dir}/data/2_families/patel_family.txt", patel_family_text, "text"),
        (f"{root_dir}/data/3_locations/school_campus.txt", school_text, "text"),
        (f"{root_dir}/src/ingest_data.py", ingest_code, "text"),
        (f"{root_dir}/requirements.txt", req_txt, "text"),
    ]

    print("\n[*] Writing Data Files...")
    for filepath, content, ftype in files_to_create:
        with open(filepath, 'w', encoding='utf-8') as f:
            if ftype == "json":
                json.dump(content, f, indent=2)
            else:
                f.write(content)
        print(f"   [+] Created File: {filepath}")

    # 6. Create Placeholder Images (Empty files just to hold the spot)
    image_files = [
        f"{root_dir}/data/4_images/rohan_ref.png",
        f"{root_dir}/data/4_images/kabir_ref.png",
        f"{root_dir}/data/4_images/school_gate.png"
    ]
    
    print("\n[*] Creating Image Placeholders...")
    for img_path in image_files:
        with open(img_path, 'wb') as f:
            pass # Create empty file
        print(f"   [+] Created Placeholder Image: {img_path}")

    print("\n[SUCCESS] Project Structure Created Successfully!")
    print(f"[INFO] Go to the folder '{root_dir}' to see your database.")

if __name__ == "__main__":
    create_gandhinagar_project()