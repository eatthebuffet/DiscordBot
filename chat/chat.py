import logging
import os
import random
from typing import List

import openai
from dotenv import load_dotenv

from chat.chat_types import ChatCompletion

load_dotenv()

openai.api_key = os.environ.get("OPENAI_KEY")

questionTypes = ["funny","thought provoking"]

def chat_truth() -> str:
    prompt = "We are playing truth or dare over text chat, I choose truth give me a "\
            f"{random.choice(questionTypes)} question.\nQUESTION:"
    return chat_prompt(prompt, temperature=1.5)

def chat_dare() -> str:
    prompt = "We are playing truth or dare over text chat,"\
             " I choose dare give me a dare.\nDARE:"
    return chat_prompt(prompt, temperature=1.5)

def chat_joke() -> str:
    prompt = "Give me a joke."
    return chat_prompt(prompt)

def chat_fanfic(message:str) -> str:
    prompt = "Do the following in the style of a FanFiction in less than 200 words:"\
            f" {message}"
    return chat_prompt(prompt)

def chat_question(message:str) -> str:
    prompt = "Answer the following question like an Scholar: "\
            f"\n{message}"
    if prompt[-1] != '?':
        prompt += '?'
    return chat_prompt(prompt)

def chat_prompt(prompt:str, max_tokens:int=300, model:str = 'gpt-3.5-turbo',
temperature:float=1) -> str:

    messages: List[dict] = [
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
        completion = ChatCompletion(**openai.ChatCompletion.create(model=model,
        messages=messages, max_tokens=max_tokens, temperature=temperature))
        content = completion.choices[0].message.content
        print(completion.json())
        print(content)
        trys = 0
        if all(s in content.lower() for s in ['model', 'language']):
            if trys > 3:
                raise Exception("triggered chatgpt")
            else:
                completion = ChatCompletion(**openai.ChatCompletion.create(model=model,
                messages=messages, max_tokens=max_tokens, temperature=temperature))
                content = completion.choices[0].message.content
                print(content)
                trys += 1
        return content
    except Exception as err:
        logging.error(f"Failed to complete prompt {prompt}, Error: {err}")
        if err == "triggered chatgpt":
            return "Chatgpt doens't want to answer this prompt. Try another question."
        return "Prompt failed to complete, Ask admin to review the logs."
