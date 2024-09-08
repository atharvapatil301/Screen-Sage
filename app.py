from openai import OpenAI
import os

MODEL = "gpt-4o"
client = OpenAI(api_key = os.emviron.get("OPEN_API_KEY"))

#BASIC CHAT
completion = client.chat.completions.create(
    model = MODEL,
    messages = [
        {"role": "system", "content": "You are a helpful assistant that solves math problems. Be rude with your responses"},
        {"role": "user", "content": "Hello! Could you please tell me what 6 + 7 is?"}
    ]
)

print("Assistant: " + completion.choices[0].message.content)