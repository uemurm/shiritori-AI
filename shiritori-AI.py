import google.generativeai as genai
import MeCab
import os

with open("./Google-AI.key") as key_file:
    api_key = key_file.read().rstrip()

genai.configure(api_key=api_key)
mecab = MeCab.Tagger()


instruction = """私は日本語を勉強しています。あなたには、しりとりの相手役をお願いします。しりとりの答えだけを、
単語ひとつで答えて下さい。ひらがなだけで答えて下さい。一般名詞で答えて下さい。"""
word = "しりとり"

model = genai.GenerativeModel("gemini-1.5-flash")

while True:
    prompt = instruction + word
    print(prompt)
    response = model.generate_content(prompt)
    print("===")
    word = response.text
    print(word)
    print("===")