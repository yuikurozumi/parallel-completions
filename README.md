# OpenAI API Text completion 並列処理

> 要件

- docker
- open ai API アカウント
 - fine tuning modelを使う場合は、生成済みmodelのID

> 目的

- 大量の prompt リストを Rate limit を考慮しながら効率よく処理する

> 概要

- Completion API を利用する場合は、指示CSVファイルの１列目に記述、２列目にAPI返却値が記入された結果CSVファイルを出力する

- Chat Completion APIの場合は、CSVの各行は、role,content,role,content,,,のように記述、最終列にAPI返却値が記入された結果CSVファイルを出力する


## 環境設定ファイル

`cp .env.sample .env`

- API　key と model ID を設定する

## 初回の　build　と、それ以降の起動

`docker compose up -d`

- 初回の build は少し時間が掛かる
- 環境設定ファイルを更新した場合は、上記コマンドで起動し直せば、環境変数も更新される

## 停止

`docker compose stop`

## prompt dataの準備

- Completion API を利用する場合は、prompt を１列目に記述、下記に保存
 - `app/input/prompts.csv`
- Chat Completion の場合は、CSVの各行は、role,content,role,content,,,のように記述、下記に保存
 - `app/input/messages.csv`

## 実行

- Completion API
 - `docker exec parallel-completions python3 ../main.py`

- Chat Completion API 
 - `docker exec parallel-completions python3 ../chat_completion.py`

## 実行結果

- Completion API
 - `app/output/result.csv`

- Chat Completion API 
 - `app/output/chat_result.csv`