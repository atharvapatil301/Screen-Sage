from groq import Groq
import base64
import os
# from langchain.memory import ConversationBufferWindowMemeory
# from langchain.prompts import PromptTemplate
# from prompt_templates import memory_prompt_template


client = Groq(api_key = os.environ.get("GROQ_API_KEY"))
llava_model = 'llava-v1.5-7b-4096-preview'
llama31_model = 'llama-3.1-70b-versatile'

# def create_chat_memory(chat_history):
#     return ConversationBufferWindowMemeory(memory_key = "history", chat_memory = chat_history, k=3)

# def create_prompt_from_template(template):
#     return PromptTemplate.from_template(template)


#encode the image
# image_path = "353db0e2-6aed-4995-8d98-2ed9cc76012e.JPG"
def encode_image(image_path):
    with open(image_path,"rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
# base64_image = encode_image(image_path)
    
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

# prompt = "Describe this image"
# print(image_to_text(client, llava_model, base64_image, prompt))



#Text to story/instructions
def instructions_generation(client, image_description):
    response = client.chat.completions.create(
        model = llama31_model,
        messages = [
            {"role": "system", "content": "You are a helpful assistant that describes testing instructions for any digital product's features, based on the descriptions of single or multiple images. Each test case should include: Description- What the test case is about. Pre-conditions - What needs to be set up or ensured before testing. Testing Steps- Clear, step-by-step instructions on how to perform the test.- Expected Result: What should happen if the feature works correctly"},
            {"role": "user", "content": image_description}
        ]
    )
    return response.choices[0].message.content


# the whole pipeline
# prompt = "Describe contents of this screenshot from an app"

# image_description = image_to_text(client, base64_image, prompt)

# print("\n---Image Description----")
# print(image_description)

# print("\n--- Instructions---")
# print(instructions_generation(client, image_description))


# class chatChain:
#     def __init__(self, chat_history, client, base64_image, prompt):
#         self.memory = create_chat_memory(chat_history)
#         self.to_text = image_to_text(client, base64_image, prompt)
#         chat_prompt = create_prompt_from_template(memory_prompt_template)
