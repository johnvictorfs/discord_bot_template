import json
from typing import TypedDict


class Settings(TypedDict):
    token: str
    prefix: str


def load_settings() -> Settings:
    """
    Loads bot settings from 'settings.json' file

    Example settings file at 'settings.example.json'
    """
    with open('bot/settings.json', 'r') as f:
        return json.load(f)
