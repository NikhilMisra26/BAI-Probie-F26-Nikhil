from openai import OpenAI
from typing import List

from src.settings import Settings, settings
from src.chatbot.constants import SYSTEM_PROMPT
from src.chatbot.models import ChatMessage


def create_client(settings: Settings = settings) -> OpenAI:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return client


def get_chat_response(
    client: OpenAI, messages: List[ChatMessage], model: str
) -> ChatMessage:
    try:
        message_dicts = [message.model_dump() for message in messages]
        response = client.chat.completions.create(
            model=model,
            messages=message_dicts,
        )
        assistant_message = response.choices[0].message
        if assistant_message.content is None:
            raise ValueError("The assistant returned no text. Please try again.")
        return ChatMessage(
            role=assistant_message.role,
            content=assistant_message.content,
        )
    except Exception as error:
        raise RuntimeError(f"Could not get a response: {error}") from error


def create_system_message() -> ChatMessage:
    return ChatMessage(role="system", content=SYSTEM_PROMPT)
