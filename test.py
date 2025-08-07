import os
from dotenv import load_dotenv
load_dotenv()
print(open("prompt_content.txt", "r").read().replace("[Language]", str(os.environ.get("LANGUAGE"))))