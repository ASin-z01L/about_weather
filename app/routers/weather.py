from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from pydantic import ValidationError
from app.dependencies import aiClient
from app.dependencies import weatherClient
from app.dependencies import sessionClient
from datetime import date
from app.schemas.api_schemas import WeatherRequest
import json
import httpx
import openai
import logging
import app.tools as tls

router = APIRouter()


@router.post('/get_weather')
async def get_weather_controller(
        ai: aiClient,
        weather: weatherClient,
        session: sessionClient,
        prompt: str = Body(embed=True)
):
    context_mess = session.get('context', [])
    day_of_week = tls.lc('days.' + date.today().strftime("%a"))

    try:
        context_mess.append({'role': 'user', 'content': f'{prompt}'})

        messages = [tls.prmt('prefix_system', date=date.today(), day=day_of_week)]
        messages.extend(context_mess)

        weather_param = json.loads(
            tls.trim_json(
                await ai.send_prompt(messages)
            )
        )

        weather_param_valid = [WeatherRequest.model_validate(item) for item in weather_param]

        weather_res = await weather.get_weather(weather_param_valid)

        weather_res_valid_json = json.dumps([item.model_dump() for item in weather_res])

        result = await ai.send_prompt(
            tls.prmt(
                'answer_system',
                user_prompt=prompt,
                date=date.today(),
                day=day_of_week,
                weather_res=weather_res_valid_json
            )
        )

        context_mess.append({'role': 'assistant', 'content': f'{result}'})
        context_mess = tls.trim_context(context_mess)

        session.set('context', context_mess)
    except (openai.APIError, httpx.HTTPStatusError, httpx.TimeoutException, httpx.NetworkError) as e:
        logging.error(e)

        raise HTTPException(
            status_code=503,
            detail=tls.lc('base.service_not_available'),
            headers={'Cache-Control': 'no-cache'}
        )
    except ValidationError as e:
        error_message = e.errors()[0]['msg']
        logging.warning(error_message)

        raise HTTPException(
            status_code=422,
            detail=error_message,
            headers={'Cache-Control': 'no-cache'}
        )

    return {
        'success': context_mess
    }
