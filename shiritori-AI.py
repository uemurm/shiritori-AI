import google.generativeai as genai
import MeCab
import argparse
import pykakasi

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


class UnconnectedException(Exception):
    def __init__(self, word, last):
        self.new_word = word
        self.last_word = last

    def __str__(self):
        return f"'{self.last_word}' の最後の文字と '{self.new_word}' の最初の文字が一致しません。"


class Shiritori(list):
    def __init__(self, word):
        self.add(word)

    def add(self, word):
        if self.__is_legit(word):
            self.append(word)

    def __last_word(self):
        if len(self) == 0:
            return None

        return self[-1]

    def __is_legit(self, word):
        if len(word) < 2:
            raise LessThanTwoLettersException()
        if not self.__is_noun(word):
            raise NotNounException()
        if not self.__is_connected(word):
            raise UnconnectedException(word, self.__last_word())
        return True

    def __is_noun(self, word):
        node = mecab.parseToNode(word)
        while node:
            if node.feature.split(",")[0] == "名詞":
                return True
            node = node.next
        return False

    def __is_connected(self, word):
        if len(self) <= 1:
            return True

        return self.__to_lower(self.__last_word()[-1]) == self.__to_lower(word[0])

    def __to_lower(self, word):
        # Convert Japanese characters to Hiragana characters.
        kakasi = pykakasi.kakasi()
        return kakasi.convert(word)[0]["hira"]


instruction = """あなたには、しりとりの相手役をお願いします。しりとりの答えだけを、単語ひとつで答えて下さい。
ひらがなもしくはカタカナだけで答えて下さい。二文字以上の一般名詞で答えて下さい。"""
initial_word = "しりとり"
prompt = instruction + initial_word

model = genai.GenerativeModel("gemini-1.5-flash")
shiritori = Shiritori(initial_word)

while True:
    print(shiritori)
    response = model.generate_content(prompt)
    returned_word = response.text.rstrip()
    if args.debug:
        print(f"DEBUG: {returned_word=}")
    try:
        shiritori.add(returned_word)
    except LessThanTwoLettersException:
        prompt = "二文字以上の単語だけで答えてください。"
    except NotNounException:
        prompt = "答えが一般名詞ではありません。"
    except UnconnectedException as e:
        prompt = str(e) + f"しりとりのルールに則って、改めて{e.last_word[-1]}で始まる単語のみを答えてください。"
    else:
        prompt = instruction + returned_word
    finally:
        if args.debug:
            print(prompt)
