FROM python:3.9.5-slim-buster

RUN pip install --upgrade pip

COPY requirement.txt /tmp
RUN cd /tmp && pip install -r requirement.txt

# Flask環境変数: Dockerコンテナ内で、Flaskがアプリケーションを正しく検出し、起動できるようになります。
ENV FLASK_APP=app

WORKDIR /app/flask
