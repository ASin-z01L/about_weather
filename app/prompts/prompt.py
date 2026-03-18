class Prompt:
    @staticmethod
    def _load_data() -> dict | None:
        """
        Loads module with prompt

        Format: key: {'role': 'system', 'content': 'prompt text'}

        :return: dict | None
        """
        try:
            module = __import__(
                'app.prompts.prompt_data',
                globals(),
                locals(),
                ['prompts']
            )
        except ModuleNotFoundError:
            return None

        return module.prompts

    @staticmethod
    def _token_replace(prompt: str, **kwargs) -> str:
        """
        Replaces tokens in prompt

        :param prompt:
        :param kwargs:
        :return: str
        """
        for key, val in kwargs.items():
            prompt = prompt.replace(f'{{{key}}}', str(val))

        return prompt

    @classmethod
    def prompt(cls, key: str, **kwargs) -> dict:
        """
        Get prompt by key

        Example calling: prompt('prefix', lang='en')
        will replace token ":lang" in prompt on "en"

        :param key:
        :param kwargs:
        :return: dict
        """
        prompt_data = cls._load_data()
        prompt_replace = prompt_data[key].copy()

        prompt_replace['content'] = cls._token_replace(
            prompt_replace['content'], **kwargs
        )

        return prompt_replace
