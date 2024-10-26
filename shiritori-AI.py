import google.generativeai as genai
import MeCab
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="print debug output", action="store_true")
args = parser.parse_args()

with open("./Google-AI.key") as key_file:
    api_key = key_file.read().rstrip()

genai.configure(api_key=api_key)
mecab = MeCab.Tagger()


class Shiritori(dict):
    def __init__(self, initial_word):
        self[initial_word] = ""

    def add(self, w):
        if self._is_noun(w):
            self[w] = ""
        if args.debug:
            print(f"DEBUG: {self=}")

    def _is_noun(self, w):
        node = mecab.parseToNode(w)
        while node:
            if node.feature.split(",")[0] == "名詞":
                return True
            node = node.next
        return False


instruction = """私は日本語を勉強しています。あなたには、しりとりの相手役をお願いします。しりとりの答えだけを、
単語ひとつで答えて下さい。ひらがなだけで答えて下さい。一般名詞で答えて下さい。"""
word = "しりとり"

model = genai.GenerativeModel("gemini-1.5-flash")
shiritori = Shiritori(word)

while True:
    prompt = instruction + word
    if args.debug:
        print(f"DEBUG: {prompt=}")
    response = model.generate_content(prompt)
    word = response.text.rstrip()
    if args.debug:
        print(f"DEBUG: {word=}")
    shiritori.add(word)
