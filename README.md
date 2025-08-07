# Audio-Overview-Clone

A Python application that uses Google's Gemini API to generate audio content from text documents. This project can process multiple source documents (now only pdf) and create natural-sounding audio summaries.

This project is inspired by **Google's NotebookLM Audio Overview** feature, which allows users to convert document summaries into spoken audio. Our implementation provides similar functionality using the Gemini API, making it accessible for developers to create their own audio summary solutions.

## ⚠️ **Warning**
If you're using Google's Gemini API on the *free plan*, please be aware that your content *might* be used to help improve their models and services.

**Disclaimer:** The developer is not liable for any data leaks or issues that may arise.

## Features

- Text-to-Speech generation using Gemini API
- Support for multiple languages (configurable)
- Document processing and summarization
- Customizable voice settings
- WAV audio output format
- Environment-based configuration

## Prerequisites

- Python 3.x
- Google Gemini API key (Get it from https://aistudio.google.com/apikey)
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MaiNgocChau9/Audio-Overview-Clone.git
cd Audio-Overview-Clone
```

2. Install required packages:
```bash
pip install google-generativeai python-dotenv
```

3. Create a `.env` file in the project root and add your configuration:
```env
GEMINI_API_KEY="your_api_key_here"
LANGUAGE="your_preferred_language"
```

## Usage

1. Place your source documents in the `sources/` directory

2. Run the Audio Overview:
```bash
python audio_overview.py
```


The generated audio file will be saved in the project root directory.

## Customization

You can customize the behavior by:
- Modifying `prompt_audio.txt` for audio generation prompts
- Adjusting `prompt_text.txt` to refine the tone and naturalness of the generated audio summaries
- Editing `prompt_content.txt` to influence the AI's writing style and content structure
- Changing the voice settings in `generate_audio.py`

## Project Structure

```
├── generate_audio.py     # Audio generation script
├── generate_text.py      # Text processing script
├── prompt_audio.txt      # Audio generation prompts
├── prompt_content.txt    # Content processing prompts
├── prompt_text.txt       # Text generation prompts
└── sources/             # Source documents directory
```

## License

This is an open-source recreation of Audio Overview. You are free to modify and use the code according to your needs.

## Privacy Note

If you have privacy concerns, you can:
- Use a different API
- Run the model locally
- Modify the code to use alternative text-to-speech services

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.