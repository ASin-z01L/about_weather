from app.contracts import AiProvider
from openai import AsyncOpenAI
import app.tools as tls


class OpenRouter(AiProvider):
    _BASE_URL = 'https://openrouter.ai/api/v1'

    __slots__ = '_client'

    def __init__(self, api_key: str):
        self._client = AsyncOpenAI(
            base_url=OpenRouter._BASE_URL,
            api_key=api_key,
        )

    def __str__(self):
        api_key_hidden = '***' + self._client.api_key[-3:] if len(self._client.api_key) > 3 else '*' * 6

        return f'base_url={OpenRouter._BASE_URL}, api_key_hidden={api_key_hidden}'

    def __repr__(self):
        return f'{__class__.__name__}({self.__str__()})'

    async def send_prompt(self, messages: dict | list[dict]) -> str:
        """
        Send prompt via the AI API

        :param messages:
        :return: str
        """

        if type(messages) is dict:
            messages = [messages]

        response = await self._client.chat.completions.create(
            model=tls.get_env('AI_MODEL'),
            messages=messages,
            temperature=0.5,
        )

        return response.choices[0].message.content
