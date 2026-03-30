import pytest
from unittest.mock import AsyncMock
from app.providers.api.weatherapi_api import Weather
from app.schemas.api_schemas import WeatherRequest
from app.schemas.api_schemas import WeatherResponse
from datetime import date, timedelta
import app.tools as tls

pytestmark = pytest.mark.asyncio


@pytest.fixture
def weather_service():
    weather_service = Weather('api_key')
    Weather._FORECAST_MAX_COUNT_DAYS = 3
    Weather._HISTORY_MAX_COUNT_DAYS = 1

    return weather_service


@pytest.fixture
def dates():
    return {
        'past': (date.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'current': date.today().strftime('%Y-%m-%d'),
        'future': (date.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
    }


# get_weather
async def test_get_weather_with_future_dates(weather_service, dates, mocker):
    mock_forecast = AsyncMock(return_value={})

    mocker.patch.object(Weather, '_forecast_weather', mock_forecast)

    future_date = date.today() + timedelta(days=1)
    mocker.patch.object(tls, 'str_to_date', return_value=future_date)

    request_data = WeatherRequest(
        city='Yekaterinburg',
        dates=[dates['current'], dates['future']]
    )

    await weather_service.get_weather([request_data])

    mock_forecast.assert_called_once_with(request_data.city, request_data.dates)


async def test_get_weather_with_current_dates(weather_service, dates, mocker):
    mock_forecast = AsyncMock(return_value={})

    mocker.patch.object(Weather, '_current_weather', mock_forecast)

    current_date = date.today()
    mocker.patch.object(tls, 'str_to_date', return_value=current_date)

    request_data = WeatherRequest(
        city='Yekaterinburg',
        dates=[dates['current']]
    )

    await weather_service.get_weather([request_data])

    mock_forecast.assert_called_once_with(request_data.city)


async def test_get_weather_with_past_dates(weather_service, dates, mocker):
    mock_forecast = AsyncMock(return_value={})

    mocker.patch.object(Weather, '_history_weather', mock_forecast)

    past_date = date.today() - timedelta(days=1)
    mocker.patch.object(tls, 'str_to_date', return_value=past_date)

    request_data = WeatherRequest(
        city='Yekaterinburg',
        dates=[dates['past']]
    )

    await weather_service.get_weather([request_data])

    mock_forecast.assert_called_once_with(request_data.city, dates['past'])


async def test_get_weather_with_past_dates_over_max_count_days(weather_service, dates, mocker):
    past_date = date.today() - timedelta(days=2)
    mocker.patch.object(tls, 'str_to_date', return_value=past_date)

    request_data = WeatherRequest(
        city='Yekaterinburg',
        dates=[dates['past']]
    )

    response_data = [WeatherResponse(
        city='Yekaterinburg',
        dates={dates['past']: None}
    )]

    result = await weather_service.get_weather([request_data])

    assert response_data == result


# _history_weather
async def test__history_weather(weather_service, dates, mocker):
    mock_forecast = AsyncMock(return_value={
        "location": {"name": "Yekaterinburg"},
        "forecast": {
            "forecastday": [
                {"day": {"avgtemp_c": 7.3, "condition": {"text": "Fog"}}}
            ]
        }}
    )

    mocker.patch.object(Weather, '_send_request', mock_forecast)

    expected_result = {"avgtemp_c": 7.3, "condition": {"text": "Fog"}}

    result = await weather_service._history_weather('Yekaterinburg', dates['past'])

    assert expected_result == result


# _current_weather
async def test__current_weather(weather_service, mocker):
    mock_forecast = AsyncMock(return_value={
        "location": {"name": "Yekaterinburg"},
        "current": {"temp_c": 6.0, "condition": {"text": "Cloudy"}}
    })

    expected_result = {"temp_c": 6.0, "condition": {"text": "Cloudy"}}

    mocker.patch.object(Weather, '_send_request', mock_forecast)

    result = await weather_service._current_weather('Yekaterinburg')

    assert expected_result == result


# _compare_date
def test__compare_date(mocker):
    user_forecast_dates = [(date.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 4)]

    api_forecat_days = [
        {"day": {"avgtemp_c": 8.7, "condition": {"text": "Patchy rain nearby"}}},
        {"day": {"avgtemp_c": 9.7, "condition": {"text": "Patchy rain nearby"}}},
        {"day": {"avgtemp_c": 10.0, "condition": {"text": "Moderate rain"}}},
    ]

    expected_result = {day: forecast['day'] for day, forecast in zip(user_forecast_dates, api_forecat_days)}

    mock_dates = mocker.patch.object(tls, 'date_to_str')
    mock_dates.side_effect = user_forecast_dates

    result = Weather._compare_date(user_forecast_dates, api_forecat_days)

    assert expected_result == result


def test__compare_date_none_forecast_on_date(mocker):
    user_forecast_dates = [(date.today() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 5)]

    api_forecat_days = [
        {"day": {"avgtemp_c": 8.7, "condition": {"text": "Patchy rain nearby", }}},
        {"day": {"avgtemp_c": 9.7, "condition": {"text": "Patchy rain nearby", }}},
        {"day": {"avgtemp_c": 10.0, "condition": {"text": "Moderate rain", }}},
    ]

    expected_result = {day: forecast['day'] for day, forecast in zip(user_forecast_dates, api_forecat_days)}
    expected_result.setdefault(user_forecast_dates[-1], None)

    mock_dates = mocker.patch.object(tls, 'date_to_str')
    mock_dates.side_effect = user_forecast_dates

    result = Weather._compare_date(user_forecast_dates, api_forecat_days)

    assert expected_result == result

# def _current_weather(self, city: str) -> dict:
#     url = f'{Weather._BASE_URL}current.json?key={self.api_key}&q={city}'
#
#     # response = self._send_request(url)
#
#     response = {
#         "location": {
#             "name": "London",
#             "region": "City of London, Greater London",
#             "country": "United Kingdom",
#             "lat": 51.5171,
#             "lon": -0.1062,
#             "tz_id": "Europe/London",
#             "localtime_epoch": 1770616816,
#             "localtime": "2026-02-09 06:00"
#         },
#         "current": {
#             "last_updated_epoch": 1770615900,
#             "last_updated": "2026-02-09 05:45",
#             "temp_c": 6.0,
#             "condition": {
#                 "text": "Cloudy",
#                 "icon": "//cdn.weatherapi.com/weather/64x64/night/119.png"
#             },
#             "wind_kph": 9.7,
#             "feelslike_c": 3.9,
#             "windchill_c": 5.8
#         }
#     }
#
#     return response.get('current')
#
#
# def _forecast_weather(self, city: str, dates: list) -> dict:
#     user_max_date_obj = tls.str_to_date(dates[-1])
#
#     forecast_count_days = min(
#         (user_max_date_obj - date.today()).days,
#         Weather._FORECAST_MAX_COUNT_DAYS
#     )
#
#     url = f'{Weather._BASE_URL}forecast.json?key={self.api_key}&q={city}&days={forecast_count_days}'
#
#     # response = self._send_request(url)
#
#     response = {
#         "location": {
#             "name": "London",
#             "region": "City of London, Greater London",
#             "country": "United Kingdom",
#             "lat": 51.5171,
#             "lon": -0.1062,
#             "tz_id": "Europe/London",
#             "localtime_epoch": 1770618199,
#             "localtime": "2026-02-09 06:23"
#         },
#         "current": {
#             "last_updated_epoch": 1770617700,
#             "last_updated": "2026-02-09 06:15",
#             "temp_c": 6.2,
#             "condition": {
#                 "text": "Overcast",
#                 "icon": "//cdn.weatherapi.com/weather/64x64/night/122.png"
#             },
#             "wind_kph": 9.0,
#             "feelslike_c": 4.3,
#             "windchill_c": 5.7
#         },
#         "forecast": {
#             "forecastday": [
#                 {
#                     "day": {
#                         "maxtemp_c": 11.0,
#                         "mintemp_c": 7.3,
#                         "avgtemp_c": 8.7,
#                         "maxwind_kph": 19.4,
#                         "totalprecip_mm": 0.62,
#                         "daily_will_it_rain": 1,
#                         "daily_chance_of_rain": 89,
#                         "daily_will_it_snow": 0,
#                         "daily_chance_of_snow": 0,
#                         "condition": {
#                             "text": "Patchy rain nearby",
#                             "icon": "//cdn.weatherapi.com/weather/64x64/day/176.png"
#                         }
#                     }
#                 },
#                 {
#                     "day": {
#                         "maxtemp_c": 12.1,
#                         "mintemp_c": 8.0,
#                         "avgtemp_c": 9.7,
#                         "maxwind_kph": 17.3,
#                         "totalprecip_mm": 3.66,
#                         "daily_will_it_rain": 1,
#                         "daily_chance_of_rain": 89,
#                         "daily_will_it_snow": 0,
#                         "daily_chance_of_snow": 0,
#                         "condition": {
#                             "text": "Patchy rain nearby",
#                             "icon": "//cdn.weatherapi.com/weather/64x64/day/176.png"
#                         }
#                     }
#                 },
#                 {
#                     "day": {
#                         "maxtemp_c": 10.7,
#                         "mintemp_c": 8.7,
#                         "avgtemp_c": 9.7,
#                         "maxwind_kph": 20.9,
#                         "totalprecip_mm": 9.48,
#                         "daily_will_it_rain": 1,
#                         "daily_chance_of_rain": 88,
#                         "daily_will_it_snow": 0,
#                         "daily_chance_of_snow": 0,
#                         "condition": {
#                             "text": "Moderate rain",
#                             "icon": "//cdn.weatherapi.com/weather/64x64/day/302.png"
#                         }
#                     }
#                 }
#             ]
#         }
#     }
#
#     str_today = tls.date_to_str(date.today())
#
#     result = {}
#
#     if str_today in dates:
#         result[str_today] = response.get('current')
#         dates = dates[dates.index(str_today) + 1:]
#
#     result.update(
#         Weather._compare_date(dates, response.get('forecast', {}).get('forecastday', []))
#     )
#
#     return result
#
#
# def _history_weather(self, city: str, history_date: str) -> dict:
#     url = f'{Weather._BASE_URL}history.json?key={self.api_key}&q={city}&dt={history_date}'
#
#     # return self._send_request(url)
#     response = {
#         "location": {
#             "name": "London",
#             "region": "City of London, Greater London",
#             "country": "United Kingdom",
#             "lat": 51.5171,
#             "lon": -0.1062,
#             "tz_id": "Europe/London",
#             "localtime_epoch": 1770637460,
#             "localtime": "2026-02-09 11:44"
#         },
#         "forecast": {
#             "forecastday": [
#                 {
#                     "day": {
#                         "maxtemp_c": 10.0,
#                         "mintemp_c": 5.8,
#                         "avgtemp_c": 7.3,
#                         "maxwind_kph": 12.2,
#                         "totalprecip_mm": 0.1,
#                         "daily_will_it_rain": 1,
#                         "daily_chance_of_rain": 100,
#                         "daily_will_it_snow": 0,
#                         "daily_chance_of_snow": 0,
#                         "condition": {
#                             "text": "Fog",
#                             "icon": "//cdn.weatherapi.com/weather/64x64/day/248.png"
#                         }
#                     }
#                 }
#             ]
#         }
#     }
#
#     return response.get('forecast', {}).get('forecastday', [{}])[0].get('day')
#
#
# [
#     {
#         'city': 'London',
#         'dates': ['2026-03-02', '2026-03-04']
#     },
#     {
#         'city': 'Kirov',
#         'dates': ['2026-03-05']
#     }
# ]
#
# data = [WeatherRequest(city='Kirov', dates=['2026-03-10'])]
#
# weather_res = [
#     WeatherResponse(city='Chelyabinsk', dates={
#         '2026-03-14': {'avgtemp_c': -20.2, 'maxwind_kph': 23.4, 'totalprecip_mm': 0.03, 'daily_will_it_rain': 0,
#                        'daily_will_it_snow': 0, 'condition': {'text': 'Overcast '}}}
#                     ),
#     # WeatherResponse(city='Yekaterinburg', dates={
#     #     '2026-03-11': {'avgtemp_c': -20.4, 'maxwind_kph': 19.1, 'totalprecip_mm': 0.1, 'daily_will_it_rain': 0,
#     #                    'daily_will_it_snow': 0, 'condition': {'text': 'Overcast '}}})
# ]
