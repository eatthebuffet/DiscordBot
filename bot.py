#import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


from chat import chat
from music import music

load_dotenv()
# discord Token

TOKEN:str = str(os.environ.get("DISCORD_TOKEN"))
if TOKEN == "None":
    raise ValueError("Please set the DISCORD_TOKEN environment variable")
    





# required variables for the bot to function
intents = discord.Intents().all()
intents.typing = True
intents.voice_states = True
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} is ready.')


@client.event
async def on_message(message) -> None:
    if message.author == client.user:
        return
    
    #this checks if the message is mentioning the bot
    #then it removes the mention from the message if it is
    if client.user is not None:
        if not client.user.mentioned_in(message):
            return
        else:
            message.content = message.content.replace(client.user.mention, '').strip()

    if message.content.startswith('!truth'):
        await message.channel.send(chat.chat_truth())

    elif message.content.startswith('!dare'):
        await message.channel.send(chat.chat_dare())
    
    elif message.content.startswith('!joke'):
        await message.channel.send(chat.chat_joke())

    elif message.content.startswith('!fanfic'):
        await message.channel.send(chat.chat_fanfic(message.replace('!fanfic ','')))
    
    elif message.content.startswith('!question'):
        await message.channel.send(chat.chat_question(message.replace('!question ','')))
        
    elif message.content.startswith('!play'):
        await music.player_play(message)
    
    elif message.content.startswith('!skip'):
        await music.play_next_song(message)

    elif message.content.startswith('!pause'):
        await music.player_pause(message)
    
    elif message.content.startswith('!resume'):
        await music.player_resume(message)
        
    elif message.content.startswith('!stop'):
        await music.player_stop(message)

    elif message.content.startswith('!queue'):
        await music.player_queue(message)

    elif message.content.startswith('!chatprompt'):
        await message.channel.\
            send(chat.chat_prompt(message.replace('!chatprompt ', '')))

    elif message.content == '!help':
        await message.channel.send("""```
///Help Menu for the commands.///

Truth or Dare:

    !dare - gives a random dare.
    !truth - gives a random truth.

Chat:
    !chatprompt <prompt>
    !fanfic <topic>
    !joke
    !question <question>

Music:

    !play <URL> -- plays a youtube video.
    !stop  -- stops the video.
    !pause -- pauses the video.
    !resume -- resumes the video.
    !queue -- lists the queue (currently broken)
    !skip -- skips song in queue (currently broken)
        ```""")

client.run(TOKEN)
