import streamlit as st
from groq import Groq
import os
import base64

client = Groq(api_key = os.environ.get("GROQ_API_KEY"))
llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

    
# Text to image
def image_to_text(client, base64_image, prompt):
    response = client.chat.completions.create(
        model=llava_model,
        messages = [
            {"role": "user", "content":[
                
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url":{
                    "url": f"data:image/jpg;base64,{base64_image}",
                    } 
                }
            ]}
        ]
    )

    return response.choices[0].message.content

def instructions_generation(client, image_description):
    response = client.chat.completions.create(
        model = llama31_model,
        messages = [
            {"role": "system", "content": "You are a helpful assistant that describes testing instructions for any digital product's features, based on the descriptions of single or multiple images. Each test case should include: Description- What the test case is about. Pre-conditions - What needs to be set up or ensured before testing. Testing Steps- Clear, step-by-step instructions on how to perform the test.- Expected Result: What should happen if the feature works correctly"},
            {"role": "user", "content": image_description}
        ]
    )
    return response.choices[0].message.content

# Streamlit App
st.title("AI Testing Instruction Chatbot")
st.write("Upload an image and enter a prompt to generate testing instructions.")

# Initialize or get chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input for prompt
prompt = st.text_input("Enter your prompt for the image description:")

# File uploader for images
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file and prompt:
    # Encode image
    base64_image = encode_image(uploaded_file)

    # Image to text description
    image_description = image_to_text(client, base64_image, prompt)
    st.session_state['chat_history'].append({"role": "user", "content": prompt})
    st.session_state['chat_history'].append({"role": "assistant", "content": image_description})

    # Display image description
    st.write("### Image Description")
    st.write(image_description)

    # Generate testing instructions
    instructions = instructions_generation(client, image_description)
    st.session_state['chat_history'].append({"role": "assistant", "content": instructions})

    # Display testing instructions
    st.write("### Testing Instructions")
    st.write(instructions)

# Display chat history
st.write("## Chat History")
for chat in st.session_state['chat_history']:
    if chat["role"] == "user":
        st.write(f"**User**: {chat['content']}")
    else:
        st.write(f"**Assistant**: {chat['content']}")


# def clear_input_field():
#     st.session_state.user_question = st.session_state.user_input
#     st.session_state.user_input = ""

# def set_send_input():
#     st.session_state.send_input = True
#     clear_input_field()

# def main():

#     st.title("ScreenSage")
#     st.write("Combines 'Screen' (for screenshots) and 'Sage' (wise guide), forming a knowledgeable assistant for testing ")

#     chat_container = st.container()

#     if "send_input" not in st.session_state:
#         st.session_state.send_input = False
#         st.session_state.user_question = ""

#     user_input = st.text_input("Message ScreenSage", key="user_input", on_change = set_send_input)

#     send_button = st.button("Send", key="send_button")

#     if send_button or st.session_state.send_input:
#         if st.session_state.user_question != "":
#             llm_response = "This is a response"

#             with chat_container:
#                 st.chat_message("human").write(st.session_state.user_question)
#                 st.chat_message("assistant").write("here is an answer")

# if __name__ == "__main__":
#     main()