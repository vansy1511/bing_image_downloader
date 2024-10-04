import mimetypes
import re
from bing_image_downloader import downloader
import os, sys
print(f"Current working directory: {os.getcwd()}")
print(f"Current Python interpreter: {sys.executable}")
import pandas as pd
import google.generativeai as genai
import dotenv
dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def find_best_image(query_string, folder):

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    files = [
        upload_to_gemini(
            f"dataset/{folder}/{filename}", mimetypes.guess_type(filename)[0] or "application/octet-stream"
        )
        for filename in os.listdir(f"dataset/{folder}") if filename.lower().endswith(('.jpg', '.png'))
    ]
    # upload all image files in "dataset/{query_string}"" to Gemini
    

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": files,
            }
        ]
    )

    response = chat_session.send_message(
        f'Choose an image that is best fit for "{query_string}". Give me the number only. If none of the images are suitable, give me "0"',
    )

    print(response.text)
    group = re.match(r"^(\d+)", response.text)
    if group:
        index = int(group.group())
        if index > 0 and index <= len(files):
            print(f"Selected file: {files[index - 1].display_name} - {query_string}")
            return files[index - 1].display_name;
        else:
            print("No file selected")
            return None
    else:
        print("Invalid input")
        return None
    

query_string = "A person shouting into a microphone at a concert."
folder = re.sub(r'[\\/*?:"<>|]', '', query_string).replace(' ', '_')
downloader.download(
    query_string,
    limit=5,
    output_dir="dataset",
    sub_dir=folder,
    adult_filter_off=True,
    force_replace=True,
    filter="custom_filter",
    timeout=60,
    verbose=True,
)
find_best_image(query_string, folder)