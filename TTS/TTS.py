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
_GUILD=getenv("GUILD").split(",")
_AUTH_PERSON=getenv("AUTH_PERSON").split(",")
_SOUND_LIB = "https://gitlab.com/OpenSourceBlackCat/MeowBotAssets/-/raw/main/audio/"
_LAST_SPOKEN_USER = ""
_AUDIO_FILE = "meow.mp3"
_REGEX_EMOJI = r"<(\w+)?:(\w+):(\d+)>"
_REGEX_LINK = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
_TRANSLATOR = Translator()
class TTS:
    async def talk(text=None, URL=None):
        AUDIO_FILE = ""
        if(text):
            textClient = gTTS(text=text, lang="hi")
            AUDIO_FILE = "meow.mp3"
            textClient.save(AUDIO_FILE)
        elif(URL):
            AUDIO_FILE = URL
        for voiceClient in AmeyaBot.voice_clients:
            if voiceClient.is_playing():
                try:
                    voiceClient.play(FFmpegPCMAudio(AUDIO_FILE))
                except: pass
            else:
                voiceClient.play(FFmpegPCMAudio(AUDIO_FILE))
    @AmeyaBot.slash_command(guild_ids=_GUILD, description="Connect To The Channel.")
    async def meow(ctx):
        if(str(ctx.author.id) in _AUTH_PERSON):
            if(ctx.author.voice):
                if(ctx.author.voice.channel.id==ctx.channel.id):
                    meow = await ctx.author.voice.channel.connect()
                    await ctx.respond("Connected Meow!")
                else:
                    await ctx.respond("The Authorised Admin Is Not Connected To The Channel.")
        else:
            await ctx.respond("You're Not Authorised To Operate This Bot!")
    @AmeyaBot.slash_command(guild_ids=_GUILD, description="Disconnect From The Channel.")
    async def miaw(ctx):
        if(str(ctx.author.id) in _AUTH_PERSON):
            if(ctx.author.voice):
                if(ctx.author.voice.channel.id==ctx.channel.id):
                    for voiceClient in AmeyaBot.voice_clients:
                        await voiceClient.disconnect()
                    await ctx.respond("Disconnected Miaw!")
                else:
                    await ctx.respond("The Authorised Admin Is Not Connected To The Channel.")
        else:
            await ctx.respond("You're Not Authorised To Operate This Bot!")
    @AmeyaBot.slash_command(guild_ids=_GUILD, descriptiop="To Play Some Funny Sounds.")
    async def sounds(ctx, sound):
        if(str(ctx.author.id) in _AUTH_PERSON):
            if(ctx.author.voice):
                if(ctx.author.voice.channel.id==ctx.channel.id):
                    try:
                        await ctx.delete()
                        try:
                            full_sound = sound.split(" ", 1)
                            finalSound = full_sound[1].title().replace(" ", "")
                            full_sound = full_sound[0].lower()
                            await TTS.talk(URL=f"{_SOUND_LIB}/{full_sound}{finalSound}.mp3")
                        except:
                            await TTS.talk(URL=f"{_SOUND_LIB}/{sound}.mp3")

                    except Exception as e:
                        print("File Not Found", e)
    @AmeyaBot.event
    async def on_ready():
        print("BlackCat's TTS BOT Running.")
    @AmeyaBot.event
    async def on_message(ctx):
        global _LAST_SPOKEN_USER
        if (not ctx.author.bot and AmeyaBot.voice_clients[0].channel.id==ctx.channel.id):
            if(ctx.author.voice.channel.id==ctx.channel.id):
                for mention in ctx.mentions:
                    ctx.content = ctx.content.replace(f"<@{mention.id}>", mention.name)
                if(len(findall(_REGEX_LINK, ctx.content))):
                    ctx.content = sub(_REGEX_LINK, "Link", ctx.content)
                ctx.content = sub(_REGEX_EMOJI, "Emoji", ctx.content)
                for emoji in distinct_emoji_list(ctx.content):
                    ctx.content = ctx.content.replace(emoji, _TRANSLATOR.translate(text=str(demojize(emoji)).replace("_", " "), dest="hi").text)
                if(_LAST_SPOKEN_USER==ctx.author.name):
                    await TTS.talk(text=ctx.content)
                else:
                    if(ctx.author.nick):
                        await TTS.talk(text=f"{ctx.author.nick} Says {ctx.content}")
                    else:
                        await TTS.talk(text=f"{ctx.author.name} Says {ctx.content}")
                _LAST_SPOKEN_USER = ctx.author.name