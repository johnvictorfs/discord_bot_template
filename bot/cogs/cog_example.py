from discord.ext import commands

from bot.bot_client import Bot


class CogExample(commands.Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=['example'])
    async def example_command(self, ctx: commands.Context, *, args: str):
        """
        Example command
        """

        await ctx.send(args)


def setup(bot):
    bot.add_cog(CogExample(bot))
