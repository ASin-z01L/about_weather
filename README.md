## AI Weather Assistant
- An intelligent weather forecast assistant with natural language support. Allows you to get weather forecasts for different cities and dates with a single query.

## Features
- **Natural Language:** ask "What's the weather like in Moscow on Friday?" or "What about St. Petersburg this weekend?" — the bot will understand. You can request forecasts for multiple cities in one prompt, for example "What's the weather like in Yekaterinburg and Sochi this weekend" if you have a flight planned from one city to another.

- **Dialogue Context:** the assistant remembers the last 10 messages, allowing you to refine queries without repeating the city.

- **Flexible Dates:** understands relative dates ("tomorrow", "in 3 days") and absolute dates ("July 15").

- **Docker Ready:** easily deployable in any environment.

- **Locale Configuration:** ability to use different languages for error messages.

## Quick Start
### Clone the repository
*bash*

```
git clone https://github.com/ASin-z01L/about_weather.git
cd <project-folder>
```

### Get API Keys
**The project requires two keys:**

- WeatherAPI.com API key, a service for obtaining weather data.

- API key for the AI model (OpenAI or compatible provider).

### Build Docker Image

*bash*
```
sudo docker build -t weather-assistant .
```

###  Run Container
Replace <your_...> values with your actual keys.

*bash*
```
sudo docker run -it -d -p 8000:8000 \
  --env WEATHER_API_KEY=<your_weather_api_key> \
  --env AI_API_KEY=<your_ai_api_key> \
  --env AI_MODEL=<gpt-3.5-turbo or other> \
  --env SESSION_TTL=3600 \
  --env LOCALE=ru \
  weather-assistant
```

**Environment Variables:**
- **WEATHER_API_KEY** - WeatherAPI.com API key
- **AI_API_KEY** - API key for AI provider
- **AI_MODEL** - Model name gpt-3.5-turbo, gpt-4, etc.
- **SESSION_TTL** - Session time-to-live in seconds (default 3600)
- **LOCALE** - Language for system messages (default ru)

## Architecture
- The project is built on Dependency Inversion Principle (DIP) and Strategy pattern, allowing easy replacement of external service implementations without changing business logic. By using abstractions, you can easily swap implementations for external services:

**AI Provider, (current implementation):**
- OpenAI-compatible API

**Alternatives:**
- Anthropic Claude
- YandexGPT
- GigaChat
- Local models (Ollama, LM Studio)
- Azure OpenAI

**Weather Service, (current implementation):**
- WeatherAPI.com

**Alternatives:**
- OpenWeatherMap
- AccuWeather
- Tomorrow.io
- Yandex Weather
- Custom weather service

**Session Storage, (current implementation):**
- In-memory (TTL)

**Alternatives:**
- Redis
- Memcached
- PostgreSQL
- MongoDB
- File system

This architecture allows changing any external dependencies without code modification, making the project:

- More flexible for different environments
- Testable (mocks for unit tests)
- Scalable (horizontal scaling with Redis)
- Cost-effective (can switch between paid and free APIs)

## Technologies
- Backend: **Python 3.10+, FastAPI**
- AI Integration: **OpenAI SDK**
- Validation: **Pydantic v2**
- HTTP Client: **httpx**
- Logging: **Python logging**
- Cache: **TTLCache**
- Container: **Docker**

## TODO / Roadmap
- Add Redis support for distributed session storage
- Implement weather data caching
- Expand list of weather providers
- Complete full localization
- Externalize current implementation selection for external services to configuration

## License
MIT


=======================


## ИИ Ассистент прогноза погоды
- Интеллектуальный ассистент для прогноза погоды, с поддержкой естественного языка. Позволяет получить прогноз погоды для разных городов и дат одним запросом. 


## Возможности
- **Естественный язык:** спрашивайте "Какая погода в Москве в пятницу?" или "А что в Питере на выходных?" — бот поймет. Есть возможность запросить прогноз в нескольких городах за один промт, например "Какая погода в Екатеринбурге и Сочи на выходных", если вы запланировали перелет из одного города в другой.

- **Контекст диалога:** ассистент помнит последние 10 сообщений, что позволяет уточнять запросы без повторения города.

- **Гибкие даты:** понимает относительные даты ("завтра", "через 3 дня") и абсолютные ("15 июля").

- **Docker Ready:** легко разворачивается в любой среде.

- **Настройка локали:** возможность использования разных языков для вывода информации об ошибках.

## Быстрый старт
### Клонируйте репозиторий

*bash*
```
git clone https://github.com/ASin-z01L/about_weather.git
cd <project-folder>
```

### Получите API ключи
**Для работы проекта необходимо два ключа:**

- API ключ WeatherAPI.com, сервис для получения данных о погоде.

- API ключ для AI-модели (OpenAI или совместимый провайдер).

### Сборка Docker образа

*bash*
```
sudo docker build -t weather-assistant .
```


### Запуск контейнера
Замените значения <your_...> на ваши реальные ключи.

*bash*
```
sudo docker run -it -d -p 8000:8000 \
  --env WEATHER_API_KEY=<your_weather_api_key> \
  --env AI_API_KEY=<your_ai_api_key> \
  --env AI_MODEL=<gpt-3.5-turbo или другое> \
  --env SESSION_TTL=3600 \
  --env LOCALE=ru \
  weather-assistant
  ```

**Переменные окружения:**
- **WEATHER_API_KEY** - API ключ WeatherAPI.com
- **AI_API_KEY** - API ключ для AI провайдера
- **AI_MODEL** - Название модели	gpt-3.5-turbo, gpt-4 и пр.
- **SESSION_TTL** - Время жизни сессии в секундах (по умолчанию 3600)
- **LOCALE** - Язык системных сообщений (по умолчанию ru)


## Архитектура
- Проект построен на принципах инверсии зависимостей (DIP) и стратегии, что позволяет легко заменять реализации внешних сервисов без изменения бизнес-логики. Благодаря использованию абстракций, вы можете легко заменить имплементации для внешних сервисов:

**AI провайдер, (текущая реализация):**
- OpenAI-совместимый API

**Альтернативы:**
- Anthropic Claude
- YandexGPT
- GigaChat
- Локальные модели (Ollama, LM Studio)
- Azure OpenAI

**Сервис погоды, (текущая реализация):**
- WeatherAPI.com

**Альтернативы:**
- OpenWeatherMap
- AccuWeather
- Tomorrow.io
- Яндекс Погода
- Собственный метео-сервис

**Хранилище сессий, (текущая реализация):**
- In-memory (TTL)	

**Альтернативы:**
- Redis
- Memcached
- PostgreSQL
- MongoDB
- Файловая система

Эта архитектура позволяет менять любые внешние зависимости без модификации кода, что делает проект:

- Более гибким для разных окружений
- Тестируемым (моки для юнит-тестов)
- Масштабируемым (горизонтальное масштабирование с Redis)
- Экономичным (можно переключаться между платными и бесплатными API)


## Технологии
- Backend: **Python 3.10+, FastAPI**
- AI Integration: **OpenAI SDK**
- Validation: **Pydantic v2**
- HTTP Client: **httpx**
- Logging: **Python logging**
- Cache: **TTLCache**
- Container: **Docker**


## TODO / Планы по развитию
- Добавить поддержку Redis для распределенного хранения сессий
- Реализовать кэширование погодных данных
- Расширить список провайдеров погоды
- Сделать полную локализацию
- Вынести выбор текущей имплементации внешнего сервиса в настройки


## Лицензия
MIT