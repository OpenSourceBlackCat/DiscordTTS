from discord.ext.commands import Bot
from discord import Intents, FFmpegPCMAudio
from dotenv import load_dotenv
from queue import Queue
load_dotenv()
from gtts import gTTS
from os import getenv
AmeyaBot = Bot(intents=Intents.all())
_GUILD=getenv("GUILD")
_OWNER=getenv("OWNER")
_LAST_SPOKEN_USER = ""
_AUDIO_QUEUE = Queue()
_AUDIO_FILE = "meow.mp3"
class TTS:
    async def talk(text):
        textClient = gTTS(text=text, lang="hi")
        textClient.save("meow.mp3")
        for voiceClient in AmeyaBot.voice_clients:
            _AUDIO_QUEUE.put(FFmpegPCMAudio(_AUDIO_FILE))
            voiceClient.play(_AUDIO_QUEUE.get())
    @AmeyaBot.slash_command(guild_ids=[_GUILD], description="Connect To The Channel.")
    async def meow(ctx):
        Auth_User = await ctx.guild.fetch_member(_OWNER)
        if(Auth_User.voice):
            if(Auth_User.voice.channel.id==ctx.channel.id):
                meow = await Auth_User.voice.channel.connect()
                await ctx.respond("Connected Meow!")
    @AmeyaBot.slash_command(guild_ids=[_GUILD], description="Disconnect From The Channel.")
    async def miaw(ctx):
        Auth_User = await ctx.guild.fetch_member(_OWNER)
        if(Auth_User.voice):
            if(Auth_User.voice.channel.id==ctx.channel.id):
                for voiceClient in AmeyaBot.voice_clients:
                    await voiceClient.disconnect()
                await ctx.respond("Disconnected Miaw!")
    @AmeyaBot.event
    async def on_read():
        print("BlackCat's TTS BOT Running.")
    @AmeyaBot.event
    async def on_message(ctx):
        global _LAST_SPOKEN_USER
        if (not ctx.author.bot and AmeyaBot.voice_clients):
            Auth_User = await ctx.guild.fetch_member(_OWNER)
            if(Auth_User.voice):
                if(Auth_User.voice.channel.id==ctx.channel.id):
                    for mention in ctx.mentions:
                        ctx.content = ctx.content.replace(f"<@{mention.id}>", mention.name)
                    if(_LAST_SPOKEN_USER==ctx.author.name):
                        await TTS.talk(ctx.content)
                    else:
                        await TTS.talk(f"{ctx.author.name} Says {ctx.content}")
                    _LAST_SPOKEN_USER = ctx.author.name