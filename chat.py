import discord
import openai
import random
import logging
from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key = os.environ.get("OPENAI_KEY")

# We can later change this to inject more interesting prompts into the places where we use this
questionTypes = ["funny","thought provoking"]

def chat_truth() -> str:
    prompt = f"We are playing truth or dare over text chat, I choose truth give me a {random.choice(questionTypes)} question.\nQUESTION:"
    return chat_prompt(prompt, temp=1.5)

def chat_dare() -> str:
    prompt = f"We are playing truth or dare over text chat, I choose dare give me a dare.\nDARE:"
    return chat_prompt(prompt, temp=1.5)

def chat_joke() -> str:
    prompt = f"Give me a joke."
    return chat_prompt(prompt)

def chat_fanfic(message) -> str:
    topic = message.content.replace('$fanfic ','')
    prompt = f"Do the following in the style of a FanFiction in less than 200 words: {topic} "
    return chat_prompt(prompt)

def chat_question(message) -> str:
    prompt = f"Answer the following question like an Scholar: \n{message.content.replace('$question ','')}"
    if prompt[-1] != '?':
        prompt += '?'
    return chat_prompt(prompt)

def chat_prompt(prompt:str, max_tokens:int=300, model:str = 'gpt-3.5-turbo', temp=1) -> str:
    messages = [
        {
            "role": "system", 
            "content": "You are a edgy assistant."
        },
        {
            "role": "user",
            "content":prompt
        }
    ]
    try:
        completion = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temp)
        content = completion.choices[0].message.content
        print(content)
        trys = 0
        if all(s in content.lower() for s in ['model', 'language']):
            if trys > 3:
                raise Exception("triggered chatgpt")
            else:
                completion = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=max_tokens, temperature=temp)
                content = completion.choices[0].message.content
                print(content)
                trys += 1
        return content
    except Exception as err:
        logging.error(f"Failed to complete prompt {prompt}, Error: {err}")
        if err == "triggered chatgpt":
            return "Chatgpt doens't want to answer this prompt. Try another question."
        return "Prompt failed to complete, Ask admin to review the logs."
