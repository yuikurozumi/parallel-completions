# OpenAI API Text completion 並列処理

> 要件

- docker
- open ai API アカウント
- fine tuning model が生成済みであること

> 目的

- 大量の prompt リストを Rate limit を考慮して効率よく処理する

> 概要

- 生成済みの fine tuning model, 各リクエストパラメタ を指定
- prompt は指示CSVファイルの１列目に記述、２列目にAPI返却値が記入された結果CSVファイルを出力する

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
