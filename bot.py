from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.context import Context

if TYPE_CHECKING:
    from typing import Any

    from discord import Interaction
    from typing_extensions import Self

GUILD = discord.Object(id=os.getenv("TEST_GUILD_ID") or "")


class WakscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.default(),
            allowed_mentions=discord.AllowedMentions.none(),
        )

        # self.session: aiohttp.ClientSession = None

    async def setup_hook(self) -> None:
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

    async def on_command_error(
        self, context: commands.Context[Self], exception: commands.CommandError  # type: ignore[override]
    ) -> None:
        print(context, exception)
        return await super().on_command_error(context, exception)
