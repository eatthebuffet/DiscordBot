import yt_dlp as youtube_dl
import asyncio
import discord



# music bot variables
voice_clients = {}
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': "-vn"}

queue = {}

async def player_play(message):
    try:
        voice_client = await message.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except:
        print("error")

    try:
        url = message.content.split()[1]
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        options = "-vn"
        source = await discord.FFmpegOpusAudio.from_probe(data["url"], options=options)
        if message.guild.id in queue:
            queue[message.guild.id].append(source)
            await message.channel.send(f"Added to queue: {data['title']}")
        else:
            queue[message.guild.id] = [source]
            player = voice_clients[message.guild.id].play(source, after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next_song(message.guild.id), loop))
            await message.channel.send(f"Now playing: {data['title']}")
    except Exception as err:
        print(err)

async def player_pause(message):
    try:
        voice_clients[message.guild.id].pause()

    except Exception as err:
        print(err)

async def player_resume(message):
    try:
        voice_clients[message.guild.id].resume()
    except Exception as err:
        print(err)

async def player_stop(message):
    try:
        voice_clients[message.guild.id].stop()
        await voice_clients[message.guild.id].disconnect()
    except Exception as err:
        print(err)

async def play_next_song(guild_id):
    if guild_id in queue and len(queue[guild_id]) > 0:
        source = queue[guild_id].pop(0)
        voice_clients[guild_id].play(source,
                                        after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(guild_id),
                                                                                        loop))
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(source._args[0], download=False))
        await message.channel.send(f"Now playing: {data['title']}")
    else:
        await voice_clients[guild_id].disconnect()

async def player_queue(message):
        if message.guild.id in queue and len(queue[message.guild.id]) > 0:
            await message.channel.send("Current queue:")
            for i, source in enumerate(queue[message.guild.id]):
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(source._args[0], download=False))
                await message.channel.send(f"{i + 1}. {data['title']}")
        else:
            await message.channel.send("The queue is currently empty.")

async def music_player(message):
    if message.content.startswith('!play'):
        pass
    if message.content.startswith("!pause"):
        pass

    # This resumes the current song playing if it's been paused
    if message.content.startswith("!resume"):
        pass
    # This stops the current playing song
    if message.content.startswith("!stop"):
        pass


    if message.content.startswith('!queue'):
        pass