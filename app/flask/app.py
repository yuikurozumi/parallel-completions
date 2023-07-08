# from flask import Flask
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random, time

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

@app.route('/api/endpoint', methods=['POST'])
# @limiter.limit("20/10seconds", error_message="Too many requests")
# @limiter.limit("100/10seconds", key_func=lambda: request.form.get('prompt', ''), error_message="Token limit exceeded")
@limiter.limit("350 per minute", error_message="Too many requests")
@limiter.limit("35000 per minute", key_func=lambda: request.form.get('prompt', ''), error_message="Token limit exceeded")
# @limit_content_length(20 * 60) # 1200 length
def mock_api():
    # random_wait = random.randint(1, 2)
    time.sleep(0.1)
    total_tokens = sum(len(v) for v in request.values.values())
    return jsonify({'total_tokens': total_tokens, 'text': 'yes'}), 200


# @app.route("/slow")
# @limiter.limit("1 per day")
# def slow():
#     return ":("


# @app.route("/medium")
# @limiter.limit("1/second", override_defaults=False)
# def medium():
#     return ":|"


# @app.route("/fast")
# def fast():
#     return ":)"


@app.route("/ping")
@limiter.exempt
def ping():
    return "PONG"
