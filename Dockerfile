FROM python:3.11.3
WORKDIR /bot
COPY requirements.txt /bot/
RUN apt-get update && apt-get -y install cmake protobuf-compiler
RUN pip install -r requirements.txt
COPY . /bot
CMD python bot.py