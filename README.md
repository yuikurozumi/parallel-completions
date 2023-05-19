# open ai api への並行実行リクエスト

> 環境要件

- docker デスクトップなどをインストール

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