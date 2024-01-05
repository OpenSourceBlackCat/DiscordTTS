FROM python:3.10
WORKDIR /DiscordTTS
COPY . /DiscordTTS/
RUN pip3 install --no-cache-dir -r requirements.txt && apt update -y && apt install ffmpeg -y
CMD python3 -u ./main.py