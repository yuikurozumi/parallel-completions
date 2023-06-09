# OpenAI API Text completion 並列処理

> 要件

- docker
- open ai API アカウント
- fine tuning model が生成済みであること

> 目的

- 大量の prompt リストを Rate limit を考慮しながら効率よく処理する

> 概要

- 生成済みの fine tuning model, 各リクエストパラメタ を指定
- prompt は指示CSVファイルの１列目に記述、２列目にAPI返却値が記入された結果CSVファイルを出力する

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

１列目に記述、下記に保存

`app/input/prompts.csv`

## 実行

`docker exec parallel-completions python3 ../main.py`

## 実行結果

`app/output/result.csv`
