FROM python:3.13

# アプリケーションディレクトリを作成する
WORKDIR /usr/src/flask_sample
# アプリケーションコードをコンテナにコピー
COPY . /usr/src/flask_sample

RUN apt-get update && \ 
    apt-get install -y libgl1-mesa-dev && \
     pip install --upgrade pip && \ 
     pip install pipenv && \
     pipenv install --system

# コンテナのポート5000を公開
EXPOSE 5000
CMD flask run --port=5000 --host=0.0.0.0 --debug
