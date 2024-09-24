import streamlit as st
from groq import Groq
import os
import base64
import re

if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    st.error("key missing")

client = Groq(api_key = api_key)
llava_model = 'llava-v1.5-7b-4096-preview'


models = {
    "gemma2-9b-it": {"name": "Gemma2-9b-it", "tokens": 8192, "developer": "Google"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}

st.title("ScreenSage")
st.subheader("Combines 'Screen' (for screenshots) and 'Sage' (wise guide), forming a knowledgeable assistant for testing ")


uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

col1, col2 = st.columns(2)
with col1:
    model_option = st.selectbox(
        "Choose a model for generating test cases:",
        options=list(models.keys()),
        format_func = lambda x: models[x]["name"],
        index=0 #deafult is set to llama 3 model
    )
    max_tokens_range = models[model_option]["tokens"]
    max_tokens = st.slider(
        "Max Tokens:",
        min_value = 512,
        max_value = max_tokens_range,
        value = min(32768, max_tokens_range),
        step = 512,
        help = f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )


with col2:

    prompt2 = st.chat_message("human").text_input("Provide context (optional)", key="context")

send_button = st.button("Describe Testing Instructions")

def encode_image(image_bytes):
    if image_bytes is not None:
        encoded_string = base64.b64encode(image_bytes).decode("utf-8")
        return "data:image/jpeg;base64,"+ encoded_string
    else:
        return None

    
prompt = "Describe contents of this screenshot from an app User Interface."

# text to image
def image_to_text(client, base64_image, prompt):
    messages = [
        {"role": "user", "content":[
            
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url":{
                "url": base64_image,
                } 
            }
        ]}
    ]

    response = client.chat.completions.create(
        model=llava_model,
        messages = messages
    )

    return response.choices[0].message.content

prompt_to_model = '''You are a helpful assistant that describes test cases for any app features, based on the descriptions of the screenshots of the app. 
Each test case should include:
    Test Case ID -  Assign a unique identifier to the test case.
    Description - Describe the test case, outlining what it is designed to do.
    Pre-conditions - Document any pre-conditions that need to be in place for the test case to run properly. It may include initial configuration settings or manually executing some previous tests.
    Testing Steps - Document the detailed steps necessary to execute the test case. This includes deciding which actions should be taken to perform the test.
    Expected Result -  Provide the expected result of the test. This is the result the tester is looking to verify.
'''
def instructions_generation(client, image_description):
    response = client.chat.completions.create(
        model = model_option,
        messages = [
            {"role": "system", "content": prompt_to_model},
            {"role": "user", "content": image_description}
        ],
        max_tokens = max_tokens
    )
    return response.choices[0].message.content

# initialize history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


if send_button:
    if prompt2 is None:
        prompt += ""
    else:
        #context appended to exisiting prompt
        prompt += prompt2

    for file in uploaded_files:
        if file:
            image_bytes = file.read()
            with st.spinner("Processing Image...."):
                base64_image = encode_image(image_bytes)
                # image to text 
                image_description = image_to_text(client, base64_image, prompt)
                st.session_state['chat_history'].append({"role": "user", "content": prompt})
                st.session_state['chat_history'].append({"role": "assistant", "content": image_description})

                # st.write(f"### Description")
                # st.write(image_description)

                # generate testing instructions
                instructions = instructions_generation(client, image_description)
                st.session_state['chat_history'].append({"role": "assistant", "content": instructions})

                col1, col2 = st.columns(2)

                with col1:
                    # display screenshot
                    st.image(file, caption = file.name, width = 300)

                with col2:
                    st.chat_message("ai").write(f"### Testing Instructions for {file.name}")
                    st.write(instructions)


st.sidebar.write("## Chat History")
for chat in st.session_state['chat_history']:
    chat_options = []
    if chat["role"] == "user":
        st.sidebar.write(f"**User**: {chat['content']}")
    else:
        st.sidebar.write(f"**Assistant**: {chat['content']}")