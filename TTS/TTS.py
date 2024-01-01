from discord.ext.commands import Bot
from discord import Intents, FFmpegPCMAudio
from emoji import distinct_emoji_list, demojize
from googletrans import Translator
from dotenv import load_dotenv
from re import sub, findall
from gtts import gTTS
from os import getenv
load_dotenv()
AmeyaBot = Bot(intents=Intents.all())
_GUILD=getenv("GUILD")
_OWNER=getenv("OWNER")
_LAST_SPOKEN_USER = ""
_AUDIO_FILE = "meow.mp3"
_REGEX_EMOJI = r"<(\w+)?:(\w+):(\d+)>"
_REGEX_LINK = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
_TRANSLATOR = Translator()
class TTS:
    async def talk(text):
        textClient = gTTS(text=text, lang="hi")
        textClient.save("meow.mp3")
        for voiceClient in AmeyaBot.voice_clients:
            if voiceClient.is_playing():
                try:
                    voiceClient.play(FFmpegPCMAudio(_AUDIO_FILE))
                except: pass
            else:
                voiceClient.play(FFmpegPCMAudio(_AUDIO_FILE))
    @AmeyaBot.slash_command(guild_ids=[_GUILD], description="Connect To The Channel.")
    async def meow(ctx):
        Auth_User = await ctx.guild.fetch_member(_OWNER)
        if(Auth_User.voice):
            if(Auth_User.voice.channel.id==ctx.channel.id):
                meow = await Auth_User.voice.channel.connect()
                await ctx.respond("Connected Meow!")
            else:
                await ctx.respond("The Authorised Admin Is Not Connected To The Channel.")
    @AmeyaBot.slash_command(guild_ids=[_GUILD], description="Disconnect From The Channel.")
    async def miaw(ctx):
        Auth_User = await ctx.guild.fetch_member(_OWNER)
        if(Auth_User.voice):
            if(Auth_User.voice.channel.id==ctx.channel.id):
                for voiceClient in AmeyaBot.voice_clients:
                    await voiceClient.disconnect()
                await ctx.respond("Disconnected Miaw!")
    @AmeyaBot.event
    async def on_ready():
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
                    if(len(findall(_REGEX_LINK, ctx.content))):
                        ctx.content = sub(_REGEX_LINK, "Link", ctx.content)
                    ctx.content = sub(_REGEX_EMOJI, "Emoji", ctx.content)
                    for emoji in distinct_emoji_list(ctx.content):
                        ctx.content = ctx.content.replace(emoji, _TRANSLATOR.translate(text=str(demojize(emoji)).replace("_", " "), dest="hi").text)
                    if(_LAST_SPOKEN_USER==ctx.author.name):
                        await TTS.talk(ctx.content)
                    else:
                        if(ctx.author.nick):
                            await TTS.talk(f"{ctx.author.nick} Says {ctx.content}")
                        else:
                            await TTS.talk(f"{ctx.author.name} Says {ctx.content}")
                    _LAST_SPOKEN_USER = ctx.author.name