import datetime
import logging

import discord
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def bot_check(ctx: commands.Context, **kwargs):
        """
        This runs at the start of every command
        """

        await ctx.trigger_typing()
        time = datetime.datetime.utcnow()
        msg = f"'{ctx.command}' ran by '{ctx.author}' as '{ctx.invoked_with}' at {time}. with '{ctx.message.content}'"
        logging.info(msg)

        return True

    # flake8: noqa: C901
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """
        Runs on every uncaught exception that happens in a Cog at Runtime

        Tries to deal with most of actual discord.py errors, otherwise sends a
        default error message and error traceback to some specific error tracker
        """

        if hasattr(ctx.command, 'on_error'):
            # Command already has local error handler, it's not necessary to handle it here
            return

        # Use original error caught instead of the one caught by the Error Handler if it exists
        error = getattr(error, 'original', error)

        prefix = self.bot.settings['prefix']
        arguments_error = [
            commands.MissingRequiredArgument,
            commands.BadArgument,
            commands.TooManyArguments,
        ]

        if any([isinstance(error, arg_error) for arg_error in arguments_error]):
            embed = discord.Embed(
                title=f"Command '{prefix}{ctx.command}' arguments:",
                description='',
                color=discord.Colour.red()
            )
            for param, param_type in ctx.command.clean_params.items():
                try:
                    default_name = param_type.default.__name__
                except AttributeError:
                    default_name = param_type.default
                default = f'(Optional, Default: {default_name})' if default_name != '_empty' else '(Required)'

                p_type = param_type.annotation.__name__

                if p_type == 'str':
                    p_type = 'Text'
                elif p_type == 'bool':
                    p_type = '[True, False]'
                elif p_type == 'Member':
                    p_type = 'Member'
                elif p_type == 'int':
                    p_type = 'Number'

                embed.add_field(name=param, value=f'**Type:** *{p_type}*\n*{default}*', inline=False)
            try:
                await ctx.send(embed=embed)
            except discord.errors.Forbidden:
                await ctx.send('Error. Missing permissions to send an embed with error info.')

        elif isinstance(error, commands.CommandNotFound):
            # Command does not exist, ignore
            pass

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('This command is disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command can not be used in private messages.')

        elif isinstance(error, commands.NotOwner):
            await ctx.send("This command can only be used by the bot's owner.")

        elif isinstance(error, commands.MissingPermissions):
            permissions = [
                f"***{perm.title().replace('_', ' ')}***" for perm in error.missing_perms]
            await ctx.send(f"You need the following permissions to do that: {', '.join(permissions)}")

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'You already used this comman recently. '
                f'Wait another {error.retry_after:.1f}s to use it again'
            )

        elif isinstance(error, commands.BotMissingPermissions):
            permissions = [
                f"***{perm.title().replace('_', ' ')}***" for perm in error.missing_perms]
            await ctx.send(f"I need the following permissions to do that: {', '.join(permissions)}")

        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You don't have permission to do that.")

        else:
            await ctx.send('Unknown error. The logs of this error have been sent to a Dev and will be fixed shortly.')
            # Send error information to an error tracker here
            # Example with Sentry commented below:

            # sentry_sdk.set_user({
            #     'id': ctx.author and ctx.author.id,
            #     'username': str(ctx.author) if ctx.author else None,
            # })

            # sentry_sdk.set_context('discord', {
            #     'guild': ctx.guild,
            #     'channel': ctx.channel and (hasattr(ctx.channel, 'name') or None) and ctx.channel,
            #     'message': ctx.message and ctx.message.content,
            #     'message_id': ctx.message and ctx.message.id,
            #     'cog': ctx.cog and ctx.cog.qualified_name,
            #     'command': ctx.command and ctx.command.name
            # })

            # sentry_sdk.capture_exception(error)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
