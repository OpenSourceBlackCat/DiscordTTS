FROM python:3.10
WORKDIR /DiscordTTS
COPY . /DiscordTTS/
RUN pip3 install -r requirements.txt
CMD python3 ./main.py