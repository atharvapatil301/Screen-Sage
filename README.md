
# ScreenSage - A testing assistant


ScreenSage is an AI test cases generator. Simply by uploading screenshots of your new app or software, it will generate a series of elaborate test cases for each functionality. It saves you the effort of manually describing test cases and prevents the risk of leaving any application component untested.
![Screenshot 2024-09-09 090720](https://github.com/user-attachments/assets/39a5a17f-f3ab-48fd-9522-108f462f57fe)


## Contents

+ [Multimodal Architecture](#Architecture)
+ [Tools and Framework](#ToolsAndFramework)
+ [Features and Prompting](#FeaturesAndPrompting)
+ [Screenshots](#Screenshots)
+ [Run Locally](##RunLocally)
## Architecture

In the development of ScreenSage, chosing the right kind of Multimodal architecture was of extreme importance, including selecting the appropiate Language Models.
ScreenSage consists of two LLMs: [LLaVA 1.5 7B Vision Language Model](https://huggingface.co/liuhaotian/llava-v1.5-7b) and any of these Large Language Models:

[Gemma2-9b-it](https://huggingface.co/google/gemma-2-9b-it),
[Gemma-7b-it](https://huggingface.co/google/gemma-1.1-7b-it),
[LLaMA3-70b-8192](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md),
[LLaMA3-8b-8192](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md),
[Mixtral-8x7b-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)

This is how the architecture or the flow of ScreenSage looks like:


![ScreenSage](https://github.com/user-attachments/assets/231ff876-55d6-4b4d-836a-15b1659fd35a)


The Image + Text is fed into the LlaVA Model which generates the image description and that is fed an input to the Language Models to generate test cases. Image to image descriptions and image descriptions to test cases. 

## ToolsAndFramework

+ [Streamlit](https://docs.streamlit.io/get-started): For hosting ScreenSage and API management.

+ [Groq](https://console.groq.com/playground): It is an AI console that gives access to all the cutting-edge models. It is simple, free of cost and yet provides quality soution (API response speed is very fast)

+ [base64](https://docs.python.org/3/library/base64.html): A python library used for encoding Image bytes to printable characters.

## FeaturesAndPrompting

- **Uploading Multipal Images:** ScreenSage can process multiple images and will generate test cases that each of the images represent.
- **Chat History:** ScreenSage maintains a chat history for each session so that you go back and refer incase if you missed out on any test case.
- **Context:** You can additionally provide context for generating your test cases.
- **Model Selection:** ScreenSage provides a range of model selection to choose from with the latest cutting edge models present. 
- **Token Size Selection:** ScreenSage provides a functionality of changing the size of the token for each model. This is to determine how elaborate you want your test cases to be. 
 - **Comprehensive Test Cases:** ScreenSage provides coherent and easy to understand test cases and also attempts to cover all the bases of a given functionality. 


There are three prompts given to the multimodal. Two of the prompts are static (fixed prompts everytime the model is run) and one prompt added in realtime.

The prompt given to the LlaVA Vision Model is (prompt1):
```bash
  "Describe contents of this screenshot from an app User Interface."
```

This is so that the vision model has a superficial understanding of the contents of the images. The second prompt is given to the Large Language Model for test case generation and that is (prompt2):
```bash
"You are a helpful assistant that describes test cases for any app features, based on the descriptions of the screenshots of the app. 

Each test case should include:

+ Test Case ID -  Assign a unique identifier to the test case.
+ Description - Describe the test case, outlining what it is designed to do.
+ Pre-conditions - Document any pre-conditions that need to be in place for the test case to run properly. It may include initial configuration settings or manually executing some previous tests.
+ Testing Steps - Document the detailed steps necessary to execute the test case. This includes deciding which actions should be taken to perform the test.
+ Expected Result -  Provide the expected result of the test. This is the result the tester is looking to verify."
  
```

The third prompt (prompt3) is nothing but the context that you provide and that is also given to the LlaVa model. Prompt3 is just appended to prompt1 in real time as and when you run the solution

## Screenshots
+ Home Screen
![Screenshot 2024-09-09 090720](https://github.com/user-attachments/assets/faa9f1fb-b79a-4044-b613-b8978c4d7844)


+ Selectimg Image Files
![Screenshot 2024-09-09 090747](https://github.com/user-attachments/assets/0d8515e5-93cf-49a7-b0e4-b6c1aa1ab4a8)


+ Optionally Provide Context
![Screenshot 2024-09-09 090901](https://github.com/user-attachments/assets/626a62ee-a44e-4413-8956-22ca352beffc)


+ Select Model
![Screenshot 2024-09-09 090920](https://github.com/user-attachments/assets/7a1de29e-4423-413c-9fb2-eafd45844684)


+ Adjust Token Size
![Screenshot 2024-09-09 090948](https://github.com/user-attachments/assets/49d236ae-7129-41c5-bc7e-c1a0873a6547)


+ Describe Testing Intstructions
![Screenshot 2024-09-09 091106](https://github.com/user-attachments/assets/593e2c04-8e86-40eb-95cc-6dcce5e63db7)
## RunLocally

Clone the project

```bash
  git clone https://github.com/Progpr/myracle
```

Go to the project directory

```bash
  cd ignite5
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```

