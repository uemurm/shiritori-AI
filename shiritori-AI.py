import google.generativeai as genai
import os

with open("./Google-AI.key") as key_file:
    api_key = key_file.read().rstrip()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello world!")
print(response.text)
