import pydantic
from enum import Enum
from typing import List

class Role(str, Enum):
    system = "system"
    assistant = "assistant"
    user = "user"

class ChatMessage(pydantic.BaseModel):
    role: Role = pydantic.Field(Role.user, alias='role') 
    content:str = pydantic.Field(..., alias='content')

class Choice(pydantic.BaseModel):
    message:ChatMessage
    finish_reason:str
    index:int

class ChatCompletion(pydantic.BaseModel):
    id:str
    object:str = pydantic.Field(..., alias='object')
    choices: List[Choice]