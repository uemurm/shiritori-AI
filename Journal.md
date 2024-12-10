- OpenAIの無料のモデルの方が、ずっとまともな答えを返してくれる。Google Gemini はどうしてもよく喋ってしまうので、回答を「」で囲って答えさせよう。
- AI の返答は再現性が低いので、テストのフレームワークを導入した方が良さそう。
- デバグ出力にIceCreamを使ってみよう。

# 2024-12-10 Tue
`UnconnectedException` のエラー・メッセージが読みにくいので、キューの最後と現在の単語を表示させた。
Private method は名前が `__` で始まる筈なので修正した。

# 2024-11-28 Thu
デバグオプションが無いときに何も出力がないので、それまでの言葉のリストを表示した。
しりとりクラスは明示的にOrderedDictを使うべき、とも思ったが、巡り巡ってリストに落ち着いた。

# 2024-10-26 Sat
しりとりのルール判定ロジックを書き始めた。
Debug オプションを追加した。

# 2024-10-19 Sat
試用期間内で切られたので、時間が出来てしまった。
しりとりの指示とともに AI が返した答えをオウム返しに渡して、AI の一人しりとりにした。
しりとりクラスを定義した。ここにルールを書きましょう。

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
