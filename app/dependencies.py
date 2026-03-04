from fastapi import Depends
from fastapi import Cookie
from fastapi import Response
from typing import Annotated
import uuid
from app.contracts import AiProvider
from app.contracts import WeatherProvider
from app.contracts import SessionProvider
from app.providers.api.openrouter_api import OpenRouter
from app.providers.api.weatherapi_api import Weather
from app.providers.ttl_cache import SessionTTLCache
import app.tools as tls


def get_ai_provider() -> AiProvider:
    return OpenRouter(tls.get_env('OPENROUTER_APY_KEY'))


def get_weather_provider() -> WeatherProvider:
    return Weather(tls.get_env('WEATHER_API_KEY'))


def get_session(
        response: Response,
        session_id: Annotated[str | None, Cookie()] = None) -> SessionProvider:
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key='session_id',
            value=session_id,
            max_age=int(tls.get_env('SESSION_TTL'))
        )

    return SessionTTLCache(session_id)


aiClient = Annotated[AiProvider, Depends(get_ai_provider)]
weatherClient = Annotated[WeatherProvider, Depends(get_weather_provider)]
sessionClient = Annotated[SessionProvider, Depends(get_session)]
