import glob
import os

import discord.ext.test as dpytest
import pytest
from rich import print

from bot.bot_client import Bot
from bot.settings import Settings


@pytest.fixture
def bot(request, event_loop):
    """
    https://dpytest.readthedocs.io/en/latest/tutorials/using_pytest.html#starting-with-pytest
    """

    settings: Settings = {'token': 'abc', 'prefix': '!'}
    bot = Bot(settings=settings, loop=event_loop)

    print()
    for extension in bot.get_cogs():
        try:
            bot.load_extension(f'bot.cogs.{extension}')
            bot.print_success(f'Loaded extension [cyan]{extension}[/cyan]')
        except Exception as e:
            error = f'{extension}:\n {type(e).__name__} : {e}'
            bot.print_error(f'Failed to load extension [cyan]{extension}[/cyan].\n[red]{error}[/red]')

    print('[green bold]Finished loading all extensions.[/green bold]')

    dpytest.configure(bot)

    return bot


def pytest_sessionfinish():
    # Clean up attachment files
    files = glob.glob('./dpytest_*.dat')

    for path in files:
        try:
            os.remove(path)
        except Exception as e:
            print(f'Error while deleting file {path}: {e}')


@pytest.fixture(autouse=True)
async def cleanup():
    yield
    await dpytest.empty_queue()
