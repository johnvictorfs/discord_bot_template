import discord.ext.test as dpytest
import pytest


@pytest.mark.asyncio
async def test_example_command(bot):
    await dpytest.message('!example some example arg')
    assert dpytest.verify().message().contains().content('some example arg')
