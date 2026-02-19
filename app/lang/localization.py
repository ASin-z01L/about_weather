import app.tools as tls


class Localization:
    @staticmethod
    def _load_translate_module(module_name, locale) -> dict | None:
        """
        Loads localization modules

        :param module_name:
        :param locale:
        :return: dict[str: str] | None
        """
        lang_path = 'app.lang'

        try:
            module = __import__(f"{lang_path}.{locale}.{module_name}",
                                globals(),
                                locals(),
                                ['translation'])

        except ModuleNotFoundError:
            return None

        return module.translation

    @staticmethod
    def _token_replace(string: str, **kwargs) -> str:
        """
        Replaces tokens in text

        :param string:
        :param kwargs:
        :return: str:
        """

        for key, val in kwargs.items():
            string = string.replace(f"{{{key}}}", val)

        return string

    @classmethod
    def translate(cls, key: str, locale: str | None = None, **kwargs) -> str:
        """
        Text localization

        :param key:
        :param locale:
        :param kwargs:
        :return: str:
        """

        key_parse = key.rsplit('.', 1)

        if len(key_parse) == 1:
            return key_parse[0]

        module_name, translation_key = key_parse
        locale = locale if locale else tls.get_env('LOCALE')
        translation = cls._load_translate_module(module_name, locale)

        if not (translation and translation.get(translation_key)):
            return translation_key

        translation_str = cls._token_replace(translation[translation_key], **kwargs)

        return translation_str
