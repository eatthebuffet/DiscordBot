import yt_dlp as youtube_dl
import asyncio
import discord
import logging



# music bot variables
voice_clients:dict = {}
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)
ffmpeg_options = {'options': "-vn"}

queue:dict = {}

async def player_play(message) -> None:
    try:
        voice_client = await message.author.voice.channel.connect()
        voice_clients[voice_client.guild.id] = voice_client
    except Exception as err:
        logging.error("Failed to connect to voice channel "\
                     f"{message.author.voice.channel}, Error={err}")
        return

    try:
        url = message.content.split()[1]
        loop = asyncio.get_running_loop()
        data = await loop.\
            run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        options = "-vn"
        source = await discord.FFmpegOpusAudio.from_probe(data["url"], options=options)
        if message.guild.id in queue:
            queue[message.guild.id].append({"source":source, "title":data['title'], 
            "url":url})
            await message.channel.send(f"Added to queue: {data['title']}")
        else:
            queue[message.guild.id] = [{"source":source, "title":data['title'], 
            "url":url}]
            voice_clients[message.guild.id].play(source,\
                after=lambda e: asyncio.run_coroutine_threadsafe(
                play_next_song(message), loop))
            await message.channel.send(f"Now playing: {data['title']}")
    except Exception as err:
        logging.error(f"Failed to play song, Error={err}")
        return

async def player_pause(message):
    try:
        await voice_clients[message.guild.id].pause()

    except Exception as err:
        logging.error(f"Failed to pause song, Error={err}")

async def player_resume(message):
    try:
        await voice_clients[message.guild.id].resume()
    except Exception as err:
        logging.error(f"Failed to resume song, Error={err}")

async def player_stop(message):
    try:
        await voice_clients[message.guild.id].stop()
    except Exception as err:
        logging.error(f"Failed to stop song, Error={err}")

async def play_next_song(message) -> None:
    guild_id = message.guild.id
    loop = asyncio.get_event_loop()
    if guild_id in queue and len(queue[guild_id]) > 0:
        queueitem = queue[guild_id].pop(0)
        await voice_clients[guild_id].pause()
        await voice_clients[guild_id].\
            play(queueitem["source"],after=lambda e: asyncio.\
                run_coroutine_threadsafe(play_next_song(message),loop))
        data = await loop.\
            run_in_executor(
                None, lambda: ytdl.extract_info(queueitem["url"], download=False))
        await message.channel.send(f"Now playing: {data['title']}")
    else:
        await voice_clients[guild_id].disconnect()

async def player_queue(message):
    if message.guild.id in queue and len(queue[message.guild.id]) > 0:
        queue_strings = "\n".join\
            ([f'{i+1}. {queueitem["title"]}\n{queueitem["url"]}'\
             for i, queueitem in enumerate(queue[message.guild.id])])
        data = f"Current queue:\n{queue_strings}"
        await message.channel.send(data)
    else:
            await message.channel.send("The queue is currently empty.")
