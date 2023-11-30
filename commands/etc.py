from __future__ import annotations

import asyncio
import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from discord import Interaction

    from bot import WakscordBot


class Etc(commands.Cog):
    def __init__(self, bot: WakscordBot):
        self.bot = bot

    @app_commands.command(name="저메추")
    async def refresh(self, interaction: Interaction[WakscordBot]) -> None:
        """
        저녁 메뉴를 추천해줍니다.
        """

        with open("./dinner.txt", "r", encoding="utf-8") as f:
            dinner = f.read().split("\n")

        await interaction.response.send_message(random.choice(dinner))

    @app_commands.command(name="결정장애")
    @app_commands.describe(option1="첫번째", option2="두번째")
    async def random_choice(
        self, interaction: Interaction[WakscordBot], option1: str, option2: str
    ) -> None:
        """
        두 가지 중 하나를 랜덤으로 골라줍니다.
        """

        await interaction.response.defer()

        msg = await interaction.followup.send("두구두구...")  # type: ignore

        await asyncio.sleep(1)

        await msg.edit(content=random.choice([option1, option2]))  # type: ignore


async def setup(bot: WakscordBot) -> None:
    await bot.add_cog(Etc(bot))
