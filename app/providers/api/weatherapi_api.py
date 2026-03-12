import httpx
from app.contracts import WeatherProvider
from datetime import date, timedelta
import app.tools as tls
from app.schemas.api_schemas import WeatherRequest
from app.schemas.api_schemas import WeatherResponse


class Weather(WeatherProvider):
    _BASE_URL = 'https://api.weatherapi.com/v1/'
    _FORECAST_MAX_COUNT_DAYS = 3  # from api tariff plan
    _HISTORY_MAX_COUNT_DAYS = 1  # from api tariff plan

    __slots__ = '_api_key'

    def __init__(self, api_key: str):
        self._api_key = api_key

    def __str__(self):
        api_key_hidden = '***' + self._api_key[-3:] if len(self._api_key) > 3 else '*' * 6

        return (f'base_url={Weather._BASE_URL}, forecast_max_count_days={Weather._FORECAST_MAX_COUNT_DAYS}, '
                f'history_max_count_days={Weather._HISTORY_MAX_COUNT_DAYS}, api_key_hidden={api_key_hidden}')

    def __repr__(self):
        return f'{__class__.__name__}({self.__str__()})'

    async def _current_weather(self, city: str) -> dict:
        """
        Get current weather

        :param city:
        :return: dict
        """

        url = f'{Weather._BASE_URL}current.json?key={self._api_key}&q={city}'

        response = await self._send_request(url)

        return response.get('current')

    async def _forecast_weather(self, city: str, dates: list) -> dict:
        """
        Get weather forecast

        :param city:
        :param dates:
        :return: dict
        """

        user_max_date_obj = tls.str_to_date(dates[-1])

        forecast_count_days = min(
            (user_max_date_obj - date.today()).days,
            Weather._FORECAST_MAX_COUNT_DAYS
        )

        url = f'{Weather._BASE_URL}forecast.json?key={self._api_key}&q={city}&days={forecast_count_days}'

        response = await self._send_request(url)

        str_today = tls.date_to_str(date.today())

        result = {}

        if str_today in dates:
            result[str_today] = response.get('current')
            dates = dates[dates.index(str_today) + 1:]

        result.update(
            Weather._compare_date(dates, response.get('forecast', {}).get('forecastday', []))
        )

        return result

    async def _history_weather(self, city: str, history_date: str) -> dict:
        """
        Get history heather

        :param city:
        :param history_date:
        :return: dict
        """

        url = f'{Weather._BASE_URL}history.json?key={self._api_key}&q={city}&dt={history_date}'

        response = await self._send_request(url)

        return response.get('forecast', {}).get('forecastday', [{}])[0].get('day')

    @classmethod
    def _compare_date(cls, user_forecast_dates: list, forecast_days: list) -> dict:
        """
        Compares the list of dates requested by the user with the response from the API

        :param user_forecast_dates:
        :param forecast_days:
        :return: dict
        """

        result = dict.fromkeys(user_forecast_dates, None)

        for day_count, forecast in enumerate(forecast_days, start=1):
            next_day = tls.date_to_str(date.today() + timedelta(days=day_count))

            if next_day in user_forecast_dates:
                result[next_day] = forecast.get('day')

        return result

    async def get_weather(self, items: list[WeatherRequest], *args, **kwargs) -> list[WeatherResponse]:
        """
        Get weather for location

        :param items:
        :return: list[WeatherResponse]
        """

        result = []

        for item in items:
            dates = {}

            for str_date in item.dates:

                obj_date = tls.str_to_date(str_date)

                if obj_date > date.today():
                    dates.update(await self._forecast_weather(item.city, item.dates))
                    break

                elif obj_date == date.today() and str_date == item.dates[-1]:
                    dates[str_date] = await self._current_weather(item.city)

                elif obj_date < date.today():
                    if obj_date >= (date.today() - timedelta(days=Weather._HISTORY_MAX_COUNT_DAYS)):
                        dates[str_date] = await self._history_weather(item.city, str_date)
                    else:
                        dates[str_date] = None

            result.append(WeatherResponse(
                city=item.city,
                dates=dates
            ))

        return result

    @staticmethod
    async def _send_request(url: str) -> dict:
        """
        Makes a request to the weather API

        :param url:
        :return: dict
        """

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()

            return response.json()
