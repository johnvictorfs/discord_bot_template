import asyncio
import datetime
from pathlib import Path

import discord
from discord.ext import commands
from rich import print
from rich.table import Table

from bot.orm.models import db
from bot.settings import Settings


class Bot(commands.Bot):
    def __init__(self, settings: Settings, loop: asyncio.AbstractEventLoop = None):
        super().__init__(
            command_prefix=settings['prefix'],
            case_insensitive=True,
            intents=discord.Intents.default()
        )

        if loop:
            self.loop = loop

        self.settings = settings
        self.start_time = None
        self.app_info = None

        self.db_setup()
        self.remove_command('help')
        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

    def print_success(self, stdout: str):
        print(f'[green bold]•[/green bold] {stdout}')

    def print_error(self, stdout: str):
        print(f'[red bold]•[/red bold] {stdout}')

    async def track_start(self):
        """
        Waits for the bot to connect to discord and records when it happened
        """

        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    @staticmethod
    def get_cogs():
        """Gets cog names from /cogs/ folder"""

        not_extensions = ['__init__']

        return [x.stem for x in Path('bot/cogs').glob('*.py') if x.stem not in not_extensions]

    async def unload_all_extensions(self) -> bool:
        """Unloads all cog extensions"""

        errored = False

        for extension in self.get_cogs():
            try:
                self.unload_extension(f'bot.cogs.{extension}')
                self.print_success(f'Unloaded extension [cyan]{extension}[/cyan]')
            except Exception as e:
                error = f'{extension}:\n {type(e).__name__} : {e}'
                self.print_error(f'Failed to unload extension [cyan]{extension}[/cyan]\n[red]{error}[/red]')
                errored = True

        return errored

    async def load_all_extensions(self) -> bool:
        """Attempts to load all .py files in /cogs/ as cog extensions"""

        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing

        errored = False

        for extension in self.get_cogs():
            try:
                self.load_extension(f'bot.cogs.{extension}')
                self.print_success(f'Loaded extension [cyan]{extension}[/cyan]')
            except Exception as e:
                error = f'{extension}:\n {type(e).__name__} : {e}'
                self.print_error(f'Failed to load extension [cyan]{extension}[/cyan].\n[red]{error}[/red]')
                errored = True

        print('[green bold]Finished loading all extensions.[/green bold]')

        return errored

    async def reload_all_extensions(self) -> bool:
        """Attempts to reload all .py files in /cogs/ as cog extensions"""

        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing

        errored = False

        for extension in self.get_cogs():
            try:
                self.reload_extension(f'bot.cogs.{extension}')
                self.success_success(f'Reloaded Extension [cyan]{extension}[/cyan].')

            except Exception as e:
                error = f'{extension}:\n {type(e).__name__} : {e}'
                self.print_error(f'Failed to reload extension [cyan]{extension}[/cyan].\n[red]{error}[/red]')
                errored = True

        return errored

    async def on_ready(self):
        """
        This event is called every time the bot connects or resumes connection.
        """

        self.app_info = await self.application_info()

        table = Table(title=None)

        table.add_column('', style='bold')
        table.add_column('Bot has successfully logged in')

        table.add_row('Bot User', self.user.name)
        table.add_row('discord.py', discord.__version__)
        table.add_row('Owner', str(self.app_info.owner))
        table.add_row('Prefix', self.settings['prefix'])
        table.add_row('Template URL', 'https://github.com/johnvictorfs/discord_bot_template')

        print(table)

    async def on_message(self, message: discord.Message):
        """
        This event triggers on every message received by the bot
        """

        if message.author.bot:
            return  # Ignore all bot messages

        await self.process_commands(message)

    @staticmethod
    def db_setup():
        """
        Setup the bot's database, creates necessary tables if not yet created
        """

        db.connect()
        models = []  # Add bot.orm.models Models here
        db.create_tables(models)
        db.close()
