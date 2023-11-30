import os
from typing import Any, Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.context import Context

GUILD = discord.Object(id=os.getenv("TEST_GUILD_ID"))


class WakscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
            allowed_mentions=discord.AllowedMentions.none(),
        )

        self.session: aiohttp.ClientSession = None

    async def setup_hook(self):
        await self.load_extension("commands.chat")
        await self.load_extension("commands.etc")
        await self.load_extension("commands.settings")
        await self.load_extension("commands.speed_setup")
        await self.load_extension("commands.subscribe")

        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync()  # guild=GUILD)

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        print(event_method, args, kwargs)
        return await super().on_error(event_method, *args, **kwargs)

    async def on_command_error(self, context, exception) -> None:
        print(context, exception)
        return await super().on_command_error(context, exception)
