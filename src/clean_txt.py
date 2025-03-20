import os
import re
import spacy
import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required resources
nltk.download("stopwords")
nltk.download("punkt")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Folder paths
input_folder = "output_texts/"  # Folder containing extracted .txt files
output_folder = "structured_data/"  # Folder to save structured JSON files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Sample list of skills for matching (you can expand this list)
skill_keywords = {"python", "django", "java", "machine learning", "deep learning", "sql", "react"}

def extract_skills(text):
    """Extract skills by matching predefined keywords."""
    words = set(word_tokenize(text.lower()))
    return list(words.intersection(skill_keywords))

def extract_job_title(text):
    """Extract job title by checking first few words (simple approach)."""
    sentences = text.split(".")
    if sentences:
        first_sentence = sentences[0]
        words = first_sentence.split()
        if len(words) > 2:
            return " ".join(words[:3])  # Assuming job titles are short
    return "Unknown"

def clean_and_normalize(text):
    """Clean, normalize text, and extract structured data."""
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower()
    words = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    # Perform lemmatization using spaCy
    doc = nlp(" ".join(words))
    lemmatized_words = [token.lemma_ for token in doc]

    cleaned_text = " ".join(lemmatized_words)
    
    # Extract structured data
    skills = extract_skills(cleaned_text)
    job_title = extract_job_title(text)

    return cleaned_text, skills, job_title

# List to store all resume data
resume_data = []

# Process all .txt files in the input folder
for index, file in enumerate(os.listdir(input_folder), start=1):
    if file.endswith(".txt"):  # Process only .txt files
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file.replace(".txt", ".json"))

        # Read text file
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Clean and normalize text
        cleaned_text, skills, job_title = clean_and_normalize(text)

        # Create structured data
        resume_entry = {
            "resume_id": index,
            "text": cleaned_text,
            "skills": skills,
            "job_title": job_title
        }

        # Save JSON file
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(resume_entry, json_file, indent=4)

        # Append to dataset
        resume_data.append(resume_entry)

        print(f"Structured data saved to {output_path}")

# Save all data to a single JSON file
with open(os.path.join(output_folder, "all_resumes.json"), "w", encoding="utf-8") as json_file:
    json.dump(resume_data, json_file, indent=4)

print(f"All structured resume data saved in {output_folder}/all_resumes.json")
