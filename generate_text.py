import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def generate(document=[], customize=""):
    load_dotenv()
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    # Sửa tên model
    model = "gemini-2.5-flash-lite"
    
    # Đơn giản hóa contents
    prompt_text = f"""
{customize}
{open("prompt_content.txt", "r").read().replace("[Language]", str(os.environ.get("LANGUAGE")))}
{open("prompt_text.txt", "r").read().replace("[Language]", str(os.environ.get("LANGUAGE")))}
"""
    
    contents = [prompt_text] + document
    
    # Đơn giản hóa config
    tools = [types.Tool(googleSearch=types.GoogleSearch())]
    
    response = client.models.generate_content(
        model=model,
        contents=contents,
        # Loại bỏ config phức tạp hoặc đơn giản hóa
    )
    return response.text