import os
from datetime import datetime, date
from app.lang.localization import Localization
from app.prompts.prompt import Prompt


def get_env(key: str) -> str | None:
    """
    Loads env variables

    :param key:
    :return: str | None
    """
    return os.environ.get(key)


def trim_context(lst: list, max_message: int = 10) -> list:
    """
    Trims the message list

    :param lst:
    :param max_message:
    :return: list
    """
    if len(lst) <= max_message:
        return lst

    return lst[-max_message:]


def lc(key: str, locale: str | None = None, **kwargs) -> str:
    """
    Gets localized text by key

    :param key:
    :param locale:
    :param kwargs:
    :return: str
    """
    return Localization.translate(key, locale, **kwargs)


def prmt(key: str, **kwargs) -> dict:
    """
    Gets prompt by key

    :param key:
    :param kwargs:
    :return: dict
    """
    return Prompt.prompt(key, **kwargs)


def trim_json(str_json: str) -> str:
    """
    Trims JSON

    :param str_json:
    :return: str
    """
    begin_list = str_json.find('[')
    begin_obj = str_json.find('{')

    if begin_list < begin_obj:
        end = str_json.rfind(']')
        return str_json[begin_list:end + 1]
    else:
        end = str_json.rfind('}')
        return str_json[begin_obj:end + 1]


def date_to_str(date_obj: date, date_format: str = '%Y-%m-%d') -> str:
    """
    Converts a date to a string

    :param date_obj:
    :param date_format:
    :return: str
    """
    return date_obj.strftime(date_format)


def str_to_date(date_str: str, date_format: str = '%Y-%m-%d') -> date:
    """
    Converts a strint to a date

    :param date_str:
    :param date_format:
    :return: date
    """
    return datetime.strptime(date_str, date_format).date()
