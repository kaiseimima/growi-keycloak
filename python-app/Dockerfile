FROM python:3

# Dockerコンテナ内での作業ディレクトリの指定
WORKDIR /app

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get install -y vim less
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja_JP
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm


# コンテナ内にPythonコードを追加
COPY . /app
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt


# # コンテナの実行コマンド
# # CMD [ "python3", "setting.py" ]
