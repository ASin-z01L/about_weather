from app.contracts import SessionProvider
from typing import Any
from cachetools import TTLCache
from collections.abc import MutableMapping
import app.tools as tls


class StorageManager:
    _storage = None

    @classmethod
    def get_storage(cls) -> TTLCache:
        if cls._storage is None:
            ttl = int(tls.get_env('SESSION_TTL'))
            cls._storage = TTLCache(maxsize=100, ttl=ttl)

        return cls._storage


class SessionTTLCache(SessionProvider):
    __slots__ = ('session_id', '_cache')

    def __init__(self, session_id: str, storage: MutableMapping = None):
        self.session_id = session_id
        self._cache = storage if storage is not None else StorageManager.get_storage()
        self._cache.setdefault(self.session_id, {})

    def __str__(self) -> str:
        return f'session_id={self.session_id}, data={self._cache[self.session_id]}'

    def __repr__(self) -> str:
        return f'{__class__.__name__}({self.__str__()})'

    def set(self, key: str, value: Any) -> None:
        """
        Sets a value in the session

        :param key:
        :param value:
        :return: None
        """

        self._cache[self.session_id][key] = value

    def get(self, key: str, default_value: Any = None) -> Any | None:
        """
        Gets the value from the session by key

        :param key:
        :param default_value:
        :return: Any | None
        """

        return self._cache[self.session_id].get(key, default_value)

    def delete(self, key: str) -> None:
        """
        Removes value from the session by key

        :param key:
        :return: None
        """

        if self._cache[self.session_id].get(key):
            del self._cache[self.session_id][key]
