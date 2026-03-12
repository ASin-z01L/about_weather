from pydantic import BaseModel, field_validator
import app.tools as tls


class WeatherRequest(BaseModel):
    city: str | None
    dates: list[str]

    @field_validator('city')
    @classmethod
    def validate_city(cls, val: str | None):
        if not val:
            raise ValueError(tls.lc('base.city_null'))

        return val

    @field_validator('dates')
    @classmethod
    def validate_date(cls, val: list[str]) -> list[str]:
        for date_str in val:
            try:
                tls.str_to_date(date_str)
            except ValueError:
                raise ValueError(tls.lc('base.date_error_format'))

        return val


class WeatherResponse(BaseModel):
    city: str
    dates: dict[str, dict | None]
