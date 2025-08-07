from generate_audio import generate as generate_audio
from generate_text import generate as generate_text
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

print("===== Audio Overview Generation =====")
print("WARNING: If you're using Google's Gemini API on the *free plan*, please be aware that your content *might* be used to help improve their models and services.\nIf you prefer not to share your content, consider using a different API or service that respects your privacy.\n\nDo you want to continue? (yes/no)")
user_input = input().strip().lower()
if user_input != "yes":
    print("Exiting the program as per user request.")
    exit()

print("Continuing with the audio overview generation...\n")
print("Uploading files...")
# Upload documents
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
documents = [os.path.join("sources", f) for f in os.listdir("sources") if os.path.isfile(os.path.join("sources", f))]
uploaded_documents = []

for document in documents:
    uploaded_doc = client.files.upload(file=document)
    uploaded_documents.append(uploaded_doc)
    print(f"Uploaded {document}")

print("\nFiles uploaded successfully.")
# Generate text overview
text_overview, name = generate_text(uploaded_documents, str(input("Enter customization text (optional): ").strip()))
print(f"Text overview generated successfully:\n{name}.txt\n")

# Generate audio overview
audio_overview = generate_audio(text_overview, str(input("Enter customization audio (optional): ")), name)
print(f"Audio overview generated successfully.\nName: {name}.wav")