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


class NotNounException(Exception):
    def __str__(self):
        return "not a noun"


class Shiritori(dict):
    def __init__(self, initial_word):
        self[initial_word] = ""

    def add(self, w):
        if self._is_noun(w):
            self[w] = ""
        else:
            raise NotNounException()

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
単語ひとつで答えて下さい。ひらがなもしくはカタカナだけで答えて下さい。二文字以上の一般名詞で答えて下さい。"""
word = "しりとり"
prompt = instruction + word

model = genai.GenerativeModel("gemini-1.5-flash")
shiritori = Shiritori(word)

while True:
    if args.debug:
        print(f"DEBUG: {prompt=}")
    response = model.generate_content(prompt)
    word = response.text.rstrip()
    if args.debug:
        print(f"DEBUG: {word=}")
    try:
        shiritori.add(word)
    except NotNounException:
        prompt = "一般名詞で答えて下さい。"
    else:
        prompt = instruction + word
