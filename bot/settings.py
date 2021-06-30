import json
import sys
from typing import TypedDict

from rich import print


class Settings(TypedDict):
    token: str
    prefix: str


def load_settings() -> Settings:
    """
    Loads bot settings from 'settings.json' file

    Example settings file at 'settings.example.json'
    """
    try:
        with open('bot/settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            '[red]Error: No settings file found. '
            "Create a '/bot/settings.json' file from '/bot/settings.example.json'[/red]"
        )
        sys.exit(1)
