FROM python:3.10
WORKDIR /DiscordTTS
COPY . /DiscordTTS/
RUN pip3 install --no-cache-dir -r requirements.txt && apt install ffpmeg -y
CMD python3 -u ./main.py