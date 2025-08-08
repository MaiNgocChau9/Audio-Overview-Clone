import mimetypes
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)

def generate(content=None, customize="", name_file="AUDIO_OVERVIEW"):
    if not content:
        print("[ERROR] No content provided for audio generation.")
        return None

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-preview-tts"
    
    # Đọc prompt
    try:
        with open("prompt_audio.txt", "r", encoding="utf-8") as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print("[ERROR] prompt_audio.txt not found.")
        return None
    
    # Tạo nội dung đầy đủ
    full_text = f"{prompt_text}\n{content}"
    if customize:
        full_text += f"\n[User_Customization]: {customize}"
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=full_text)],
        ),
    ]
    
    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
            )
        ),
    )

    audio_file_name = None
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config,
        ):
            if (
                chunk.candidates 
                and chunk.candidates[0].content 
                and chunk.candidates[0].content.parts 
                and chunk.candidates[0].content.parts[0].inline_data
            ):
                part = chunk.candidates[0].content.parts[0].inline_data
                if part.data:
                    ext = mimetypes.guess_extension(part.mime_type) or ".wav"
                    audio_file_name = f"{name_file}{ext}"
                    save_binary_file(audio_file_name, part.data)
    except Exception as e:
        print(f"[ERROR] Audio generation failed: {e}")

    return audio_file_name
