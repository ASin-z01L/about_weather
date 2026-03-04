from abc import ABC, abstractmethod
from typing import Any


class AiProvider(ABC):
    __slots__ = ()

    @abstractmethod
    async def send_prompt(self, messages: dict | list[dict]) -> str:
        ...


class WeatherProvider(ABC):
    __slots__ = ()

    @abstractmethod
    async def get_weather(self, items: list[dict]) -> list:
        ...


class SessionProvider(ABC):
    __slots__ = ()

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    def get(self, key: str, default_value: Any = None) -> Any | None:
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        ...
