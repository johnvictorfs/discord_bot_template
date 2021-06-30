import asyncio
import logging
import sys

import discord
from rich import print
from rich.logging import RichHandler
from rich.traceback import install

from bot.bot_client import Bot
from bot.settings import Settings, load_settings

install()


async def run(settings: Settings):
    bot = Bot(settings=settings)

    try:
        await bot.start(settings.get('token'))
    except KeyboardInterrupt:
        await bot.logout()
    except discord.errors.LoginFailure:
        print("[red]Error: Invalid Token. Please input a valid token in '/bot/settings.json' file.[/red]")
        sys.exit(1)


def setup_and_run():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(RichHandler())

    loop = asyncio.get_event_loop()
    settings = load_settings()
    loop.run_until_complete(run(settings))


if __name__ == '__main__':
    setup_and_run()
