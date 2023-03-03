import discord
import openai
import random
import os

openai.api_key = os.environ.get("OPENAI_KEY")

# We can later change this to inject more interesting prompts into the places where we use this
questionTypes = ["Funny", "Witty", "Charming", "Creative"]

async def chat_truth() -> str:
    prompt = f"We are playing truth or dare over text chat, I choose truth give me a very {random.choice(questionTypes)} question."
    return chat_prompt(prompt)

async def chat_dare() -> str:
    prompt = f"We are playing truth or dare over text chat, I choose dare give me a very creative dare."
    return chat_prompt(prompt)

async def chat_joke() -> str:
    prompt = f"Give me a creative {random.choice(questionTypes)} joke."
    return chat_prompt(prompt)

async def chat_fanfic(message) -> str:
    topic = message.content.replace('$fanfic ','')
    prompt = f"Write a {random.choice(questionTypes)} fan fiction about {topic}."
    return chat_prompt(prompt)

async def chat_question(message) -> str:
    prompt = f"Answer the following question like an Scholar: \n{message.content.replace('$question ','')}"
    if prompt[-1] != '?':
        prompt += '?'
    return chat_prompt(prompt, 1000)

async def chat_prompt(prompt:str, max_tokens:int=2000) -> str:
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=max_tokens)
    return completion.choices[0].text
