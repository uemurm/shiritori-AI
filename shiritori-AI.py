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


class LessThanTwoLettersException(Exception):
    def __str__(self):
        return "The word consists of less than two letters"


class Shiritori(dict):
    def __init__(self, initial_word):
        self[initial_word] = ""

    def add(self, w):
        if self._is_legit(w):
            self[w] = ""

        if args.debug:
            print(f"DEBUG: {self=}")

    def _is_legit(self, w):
        if len(w) < 2:
            raise LessThanTwoLettersException()
        if not self._is_noun(w):
            raise NotNounException()
        return True

    def _is_noun(self, w):
        node = mecab.parseToNode(w)
        while node:
            if node.feature.split(",")[0] == "名詞":
                return True
            node = node.next
        return False


instruction = """あなたには、しりとりの相手役をお願いします。しりとりの答えだけを、単語ひとつで答えて下さい。
ひらがなもしくはカタカナだけで答えて下さい。二文字以上の一般名詞で答えて下さい。"""
word = "しりとり"
prompt = instruction + word

model = genai.GenerativeModel("gemini-1.5-flash")
shiritori = Shiritori(word)

while True:
    print(list(shiritori.keys()))
    response = model.generate_content(prompt)
    word = response.text.rstrip()
    if args.debug:
        print(f"DEBUG: {word=}")
    try:
        shiritori.add(word)
    except LessThanTwoLettersException:
        prompt = "二文字以上の単語だけで答えてください。"
    except NotNounException:
        prompt = "答えが一般名詞ではありません。"
    else:
        prompt = instruction + word
