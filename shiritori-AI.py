import google.generativeai as genai
import MeCab
import os

with open("./Google-AI.key") as key_file:
    api_key = key_file.read().rstrip()

genai.configure(api_key=api_key)
mecab = MeCab.Tagger()


def is_noun(w):
    node = mecab.parseToNode(w)
    while node:
        if node.feature.split(",")[0] == '名詞':
            return True
        node = node.next
    return False


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello world!")
print(response.text)
