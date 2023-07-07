import os
import csv
import time
import openai
import concurrent.futures
import random
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI APIキーを設定
MODEL = os.getenv("OPENAI_MODEL")  # GPT-3のモデルIDを設定
RATE_LIMIT = 340 # 1分あたりのリクエスト数の上限
SLEEP_TIME = 60  # Sleepする最大秒数。（60秒）
LEN_TOKENS_RATE_LIMIT = 35000  # 1分あたりのトークン数の上限
STOP = ["\n"]
MAX_TOKENS = 100
CSV_FILE_NAME = "prompts.csv" # input directoryにあるCSVファイルの名前を指定
RESULT_CSV_FILE_NAME = "result.csv"
MAX_WORKERS = 10 # 並列処理のためのワーカー数を設定

start_time = time.time()
count_requests = 0
len_tokens = 0
sleep_to = 0

def query_completion(prompt):
    global start_time
    global count_requests
    global len_tokens
    global sleep_to

    elapsed_time = time.time() - start_time
    count_requests += 1

    if (
        count_requests >= RATE_LIMIT - MAX_WORKERS
        and elapsed_time < SLEEP_TIME
    ):
        sleep_time = SLEEP_TIME - elapsed_time
        start_time = time.time() + sleep_time
        print(f"Reached rate limit of {RATE_LIMIT} requests per minute. Sleeping for {sleep_time} seconds...")
        # 初期化
        count_requests = 0
        len_tokens = 0
        print(f"updated start_time {start_time}")

    elif (
        len_tokens >= LEN_TOKENS_RATE_LIMIT - (MAX_TOKENS * MAX_WORKERS)
        and elapsed_time < SLEEP_TIME
    ):
        sleep_time = SLEEP_TIME - elapsed_time
        start_time = time.time() + sleep_time
        print(f"Reached rate limit of {LEN_TOKENS_RATE_LIMIT} tokens per minute. Sleeping for {sleep_time} seconds...")
        # 初期化
        count_requests = 0
        len_tokens = 0
        print(f"updated start_time {start_time}")

    if time.time() <= start_time:
        print("waiting for other thread...")
        while time.time() <= start_time:
            time.sleep(1)

    # response = openai.Completion.create(
    #     model=MODEL,
    #     prompt=prompt,
    #     max_tokens=MAX_TOKENS,
    #     stop=STOP
    # )
    # return {
    #     "text": response.choices[0].text.strip(),
    #     "total_tokens": response.usage.total_tokens,
    # }
    req_start = time.time()
    url = 'http://parallel-completions:5000/api/endpoint'
    payload = {'prompt': prompt}

    # print(f"Send Request {req_start} count_requests : {count_requests} start_time: {start_time}")

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        diff = time.time() - req_start
        len_tokens += data['total_tokens']
        return {'time_takes': diff, 'text': data['text'], 'total_tokens': data['total_tokens']}

    else:
        raise Exception(response.status_code)

def process_prompts(prompts):
    # 並列処理のためのワーカー数を設定
    num_workers = min(len(prompts), MAX_WORKERS)
    completed_count = 0
    total_time_takes = 0

    output_dir = os.path.join(os.path.dirname(__file__)) + '/output/'
    output_file_path = output_dir + RESULT_CSV_FILE_NAME

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # プロンプトごとにCompletion APIを非同期で呼び出す
        future_to_prompt = {executor.submit(query_completion, prompt): prompt for prompt in prompts}

        with open(output_file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            for future in concurrent.futures.as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    completion = future.result()
                    writer.writerow([prompt, completion["text"]])  # 結果をCSVファイルに書き込む
                    total_time_takes += completion["time_takes"]
                    completed_count += 1
                except Exception as exc:
                    # エラーハンドリング
                    print(f"Error processing prompt: {prompt}, {exc}")
    print("Total threads execution time:", total_time_takes)


# CSVファイルからプロンプトを読み込む
def load_prompts_from_csv(file_path):
    prompts = []
    for i in range(8):
        # 100文字のプロンプトを生成
        for j in range(100):
            prompts.append("Hello World_" + "." * (99 - j) + str(j))
    # with open(file_path, "r") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         if row:
    #             prompts.append(row[0])  # CSVの各行の最初の要素をプロンプトとして追加
    return prompts

if __name__ == "__main__":
    # CSVファイルのパスを指定してプロンプトをロードして実行
    input_dir = os.path.join(os.path.dirname(__file__)) + '/input/'
    csv_file_path = input_dir + CSV_FILE_NAME  # CSVファイルのパスを適宜変更
    prompts = load_prompts_from_csv(csv_file_path)
    start = time.time()
    process_prompts(prompts)
    total = time.time() - start
    print("Execution time:", total, "seconds")
