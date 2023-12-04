import os

from flask import Flask, jsonify, render_template
from tasks import generate_response, generate_text
import json

app = Flask(__name__)
app.config.from_mapping(
    CELERY=dict(
        broker_url=os.getenv("CELERY_BROKER_URL"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND"),
        task_ignore_result=True,
    ),
)


def on_raw_message(body):
    print(body)


@app.route("/")
def main():
    msg = {
        "model": "llama2",
        "prompt": "What is the speed of light",
        "stream": False,
    }
    task = generate_response.delay(json.dumps(msg))
    result_msg = task.get()
    response = {
        "state": task.state,
        "msg": result_msg,
    }
    return f"{response}"


@app.route("/result/")
def result():
    pass


@app.route("/text_gen")
def text_gen():
    task = generate_text.delay()
    result_msg, test = task.get()
    response = {"state": task.state, "msg": result_msg, "addit_msg": test}
    return f"{response}"


if __name__ == "__main__":
    app.debug = True
    app.run()
