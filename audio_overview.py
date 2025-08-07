from generate_audio import generate as generate_audio
from generate_text import generate as generate_text
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

# Upload documents
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
documents = [os.path.join("sources", f) for f in os.listdir("sources") if os.path.isfile(os.path.join("sources", f))]
uploaded_documents = []

for document in documents:
    uploaded_doc = client.files.upload(file=document)
    uploaded_documents.append(uploaded_doc)
    print(f"Uploaded {document}")

# Generate text overview
text_overview = generate_text(uploaded_documents)
print(f"Text overview generated successfully:\n{text_overview}\n")

# Generate audio overview
audio_overview = generate_audio(text_overview)
print(f"Audio overview generated successfully.\nName: {audio_overview}")