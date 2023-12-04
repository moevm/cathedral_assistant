from __future__ import absolute_import, unicode_literals

from celery import shared_task
import json
import requests
import os
from celery import Celery
from typing import Dict
from flask import Response


app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),
)


@shared_task
def generate_response(msg):
    request_url = "http://127.0.0.1:11434/api/generate"
    llama_response = requests.post(request_url, data=msg)
    print(f"RESPONSE - {llama_response}")
    return json.dumps(llama_response.text)


@shared_task
def generate_text():
    files = {"file": open("/app/testing_data/say_my_name.mp3", "rb")}
    request_url = "http://localhost:9000/asr?encode=true&task=transcribe&language=en&word_timestamps=false&output=json"
    whisper_response = requests.post(request_url, files=files)
    print(f"RESPONSE - {whisper_response}")
    return json.dumps(whisper_response.text)
