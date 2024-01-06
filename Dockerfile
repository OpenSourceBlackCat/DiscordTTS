FROM python:3.10
WORKDIR /DiscordTTS
COPY . /DiscordTTS/
RUN pip3 install --no-cache-dir -r requirements.txt && apt-get update -y --no-install-recommends git && apt-get clean && apt-get install ffmpeg -y
CMD python3 -u ./main.py