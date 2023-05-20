# OpenAI API Text completion 並列処理

> 要件

- docker
- open ai APIアカウント
- 生成済みのfine tuning model

> 目的・概要

- 大量のpromptリスト（CSVファイル）を高速に処理する
- 生成済みのfine tuning modelを指定
- Ratelimit 考慮あり

## 環境設定ファイル

`cp .env.sample .env`

## build

docker compose up -d

## prompt dataの準備

１列目に記述、下記に保存

`app/input/prompts.csv`

## 実行

docker exec parallel-completions python3 ./main.py

## 実行結果

`app/output/result.csv`
