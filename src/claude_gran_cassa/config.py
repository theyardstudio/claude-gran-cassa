import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("ANTHROPIC_API_KEY")

    @property
    def api_key(self):
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        return self._api_key


config = Config()
