from discord.ext import commands


class CogExample(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(manage_channels=True)
    @commands.command(aliases=['example'])
    async def pinto(self, ctx: commands.Context, *, args: str):
        """
        Example command
        """
        await ctx.send(args)


def setup(bot):
    bot.add_cog(CogExample(bot))
