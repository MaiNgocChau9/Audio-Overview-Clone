from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"),)
files = [os.path.join("sources", f) for f in os.listdir("sources") if os.path.isfile(os.path.join("sources", f))]
uploaded_files = []

for file in files:
    sample_pdf = client.files.upload(file=file)
    uploaded_files.append(sample_pdf)
    print(f"Uploaded {file}: {sample_pdf}")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Give me a summary of these pdf file:\n1. <Name file>\n>Summary", uploaded_files],
)
print(response.text)