import re

from discord.ext import commands


class CogExample(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @commands.command(aliases=['example'])
    async def example_command(self, ctx: commands.Context):
        """
        Example command
        """
        pass


def setup(bot):
    bot.add_cog(CogExample(bot))
