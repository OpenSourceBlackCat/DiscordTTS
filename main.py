from dotenv import load_dotenv
load_dotenv()
from os import getenv
from TTS import TTS
TTS.AmeyaBot.run(getenv("TOKEN"))