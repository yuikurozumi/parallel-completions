import os
import csv
import time
import openai
import concurrent.futures

openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI APIキーを設定
MODEL = os.getenv("OPENAI_MODEL")  # GPT-3のモデルIDを設定
RATE_LIMIT = 15 # 1分あたりのリクエスト数の上限
SLEEP_TIME = 4  # スリープする秒数（60秒 = 1分）
LEN_TOKENS_RATE_LIMIT = 200  # 1分あたりのトークン数の上限
STOP = ["\n"]
MAX_TOKENS = 20
CSV_FILE_NAME = "prompts.csv" # input directoryにあるCSVファイルの名前を指定
RESULT_CSV_FILE_NAME = "result.csv"
MAX_WORKERS = 7 # 並列処理のためのワーカー数を設定

def query_completion(prompt):
    time.sleep(1)
    return prompt + "completion"
    # response = openai.Completion.create(
    #     model=MODEL,
    #     prompt=prompt,
    #     max_tokens=MAX_TOKENS,
    #     stop=STOP
    # )
    # return response.choices[0].text.strip()

def process_prompts(prompts):
    # 並列処理のためのワーカー数を設定
    num_workers = min(len(prompts), MAX_WORKERS)

    start_time = time.time()
    start_time4token = time.time()
    completed_count = 0
    sum_len_tokens = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # プロンプトごとにCompletion APIを非同期で呼び出す
        future_to_prompt = {executor.submit(query_completion, prompt): prompt for prompt in prompts}

        output_dir = os.path.join(os.path.dirname(__file__)) + '/output/'
        output_file_path = output_dir + RESULT_CSV_FILE_NAME

        with open(output_file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            for future in concurrent.futures.as_completed(future_to_prompt):
                prompt = future_to_prompt[future]
                try:
                    completion = future.result()
                    # 完了した結果の処理
                    print("Completion for prompt:", prompt)
                    print("Result:", completion)
                    print("completed_count:", completed_count)
                    # writer.writerow([prompt, completion])  # 結果をCSVファイルに書き込む
                except Exception as exc:
                    # エラーハンドリング
                    print(f"Error processing prompt: {prompt}, {exc}")

                completed_count += 1
                # print("completion:", completion)
                # print("len_token:", len(completion))
                sum_len_tokens += len(completion)
                # print("sum_len_tokens:", sum_len_tokens)
                elapsed_time = time.time() - start_time
                elapsed_time4token = time.time() - start_time4token

                writer.writerow([elapsed_time, elapsed_time4token, completed_count])

                if completed_count % RATE_LIMIT == 0 and elapsed_time < SLEEP_TIME:
                    # Rate limitを考慮してスリープする
                    sleep_time = SLEEP_TIME - elapsed_time
                    msg = f"Sleeping for {sleep_time} seconds to respect rate limit... now completed_count: {completed_count}"
                    print(msg)
                    time.sleep(sleep_time)
                    start_time = time.time()
                    writer.writerow(['sleep by request', msg])  # 結果をCSVファイルに書き込む
                elif (
                    sum_len_tokens + MAX_TOKENS >= LEN_TOKENS_RATE_LIMIT
                    and elapsed_time4token < SLEEP_TIME
                ):
                    # トークン数の上限に達したらスリープする
                    sleep_time = SLEEP_TIME - elapsed_time4token
                    msg = f"Reached token rate limit of {LEN_TOKENS_RATE_LIMIT} tokens per minute. Sleeping for {sleep_time} seconds..."
                    print(msg)
                    time.sleep(sleep_time)
                    start_time4token = time.time()
                    sum_len_tokens = 0
                    writer.writerow(['sleep by token', msg])  # 結果をCSVファイルに書き込む


# CSVファイルからプロンプトを読み込む
def load_prompts_from_csv():
    prompts = []
    for i in range(30):
        prompts.append("prompt" + str(i))
    # with open(file_path, "r") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         if row:
    #             prompts.append(row[0])  # CSVの各行の最初の要素をプロンプトとして追加
    return prompts

if __name__ == "__main__":
    # CSVファイルのパスを指定してプロンプトをロードして実行
    # input_dir = os.path.join(os.path.dirname(__file__)) + '/input/'
    # csv_file_path = input_dir + CSV_FILE_NAME  # CSVファイルのパスを適宜変更
    prompts = load_prompts_from_csv()
    start = time.time()
    process_prompts(prompts)
    total = time.time() - start
    print("Total execution time:", total, "seconds")
