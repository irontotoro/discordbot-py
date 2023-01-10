import discord
import responses
import asyncio
import os
import youtube_dl
import random
from dotenv import load_dotenv
from discord.ext import commands,tasks


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    load_dotenv()
    TOKEN = 
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix='!',intents=intents)

    youtube_dl.utils.bug_reports_message = lambda: ''

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoteerrors': False,
        'logtostderr': False,
        'quiet':True,
        'no_warnings':True,
        'default_search': 'auto',
        'source_address':'0.0.0.0'
    }

    ffmeg_options = {
        'options': '-vn'
    }

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("공사장노동"))
        print(f'{bot.user} is now running!')

    
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)


        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            
            await send_message(message, user_message, is_private=True)
        else:
            await bot.process_commands(message)
            await send_message(message, user_message, is_private=False)
    

            
           
    

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = ""

        @classmethod
        async def from_url(cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda:ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                data = data['entries'][0]
            filename = data['title'] if stream else ytdl.prepare_filename(data)
            return filename
    
    @bot.command(name='join',help='Tells the bot to join the voice channel')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{}is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @bot.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @bot.command(name='play_song', help='To play song')
    async def play(ctx,url):
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")
    
    @bot.command(name='pause', help='This command pauses the song')
    async def pause(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command(name='resume', help='Resumes the song')
    async def resume(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send("The bot was not playing anything before this. Use play_song command")

    @bot.command(name='stop', help='Stops the song')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @bot.command(name='재웅아노래불러줘', help='재웅이가 랩을 합니다')
    async def 재웅아노래불러줘(ctx,url='https://www.youtube.com/watch?v=7eC5HMfzleQ'):
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client
            
            async with ctx.typing():
                filename = await YTDLSource.from_url(url='https://www.youtube.com/watch?v=7eC5HMfzleQ', loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
            await ctx.send('**재웅이가 부릅니다:** {}'.format(filename))
        except:
            await ctx.send("The bot is not connected to a voice channel.")

    
    @bot.command(name='die', help='turn off the bot')
    async def die(ctx):
        await ctx.send("전 이세계를 이만 떠납니다 모두들 안녕")
        await ctx.send("Please observe, however, that my Presence will remain incorrectly Online for about 110 seconds.")
        await ctx.send("잘있어라 인생아")
        await bot.close()

        
    bot.run(TOKEN)
