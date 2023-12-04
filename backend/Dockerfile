FROM python:3.8
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP main
ENV FLASK_RUN_HOST 0.0.0.0
COPY . .
RUN apt update && pip install -r requirements.txt
CMD [ "python", "main.py" ]