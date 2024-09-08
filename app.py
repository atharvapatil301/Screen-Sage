from openai import OpenAI
import os

MODEL = "gpt-4"
client = OpenAI(api_key = os.environ.get("OPEN_API_KEY"))

#BASIC CHAT
completion = client.chat.completions.create(
    model = MODEL,
    messages = [
        {"role": "system", "content": "You are a helpful assistant that solves math problems. Be rude with your responses"},
        {"role": "user", "content": "Hello! Could you please tell me what 6 + 7 is?"}
    ]
)

# print("Assistant: " + completion.choices[0].message.content)

# 2  - Image processing with Base64
import base64

IMAGE_PATH = "yellowsub.png"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.base64.encode(image_file.read()).decode("utf-8")

 
base64_image = encode_image(IMAGE_PATH)

completion = client.chat.completions.create(
    model = MODEL,
    messages = [
        {"role": "system", "content": "You are a helpful assistant which analyses the image to answer user questions about the image"},
        {"role": "user", "content": [
            {"type":"text", "text": "What colour is the submarine in the image?"},
            {"type": "image_url", "image_url": {"url":f"data:image/png;base64,{base64_image}"}}
        ]}

    ],
    temperature = 0.0
)
print(completion.choices[0].message.content)