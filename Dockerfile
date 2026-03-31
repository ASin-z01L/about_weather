FROM python:3.14-slim

WORKDIR /about_weather
COPY . /about_weather

RUN apt-get update && apt-get upgrade -y && \
    pip install uv && \
    uv pip install --system -e .

EXPOSE 8000

CMD ["python", "run.py"]