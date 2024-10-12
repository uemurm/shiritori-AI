- Cannot `git push` on VS Code. Need to do that on WSL, instead.

# 2024-10-12 Sat
Open-AI が無料では使えないので、Python で書いて Google Gemini にアクセスすることにした。
`poetry install` で生成されるファイル `poetry.lock` を何故コミットするのか疑問だったが、
https://stackoverflow.com/questions/39990017/should-i-commit-the-yarn-lock-file-and-what-is-it-for
によると依存関係を non-deterministically にインストールするかららしい…

Python-3.9 をインストールしたのだが、正しいバージョンのライブラリを import 出来ず、結局 `pyenv`/`poetry` を導入した。

# 2023-05-30 Tue
ssh-agent に秘密鍵を登録して、`config.fish`で自動的に起動させた。

# 2023-05-28 Sun
@Itamar, @Daniel のアドバイスを反映させた。

# 2023-05-25 Thu
会社をお休みしてしまったが、こちらを書き進めてみた。
- お金が足りないので、モックを作りましょう。
    => require 'optparse' しつつ、ローカルファイルから仮の返答を読み込むようにした。
- todo: Create a file 'system_prompt.txt' => Done
- 「ん」で終わる単語を連続で返されると、「ん」で始まる別の単語で答えて下さい。と出力してしまう。=> Done
- todo: Create a file 'open-ai.key' then read it instead. => Done

# 2023-05-23 Tue
Did `git init`, finally..
