import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands


class Etc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="저메추")
    async def refresh(self, interaction: discord.Interaction):
        """
        저녁 메뉴를 추천해줍니다.
        """

        with open("./dinner.txt", "r", encoding="utf-8") as f:
            dinner = f.read().split("\n")

        await interaction.response.send_message(random.choice(dinner))

    @app_commands.command(name="결정장애")
    @app_commands.describe(option1="첫번째", option2="두번째")
    async def random_choice(
        self, interaction: discord.Interaction, option1: str, option2: str
    ):
        """
        두 가지 중 하나를 랜덤으로 골라줍니다.
        """

        await interaction.response.defer()

        msg = await interaction.followup.send("두구두구...")

        await asyncio.sleep(1)

        await msg.edit(content=random.choice([option1, option2]))


async def setup(bot: commands.Bot):
    await bot.add_cog(Etc(bot))
