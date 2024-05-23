import asyncio
import random

import aiohttp
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

    @app_commands.command(name="점메추")
    async def refresh(self, interaction: discord.Interaction):
        """
        점심 메뉴를 추천해줍니다.
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

    @app_commands.command(name="뱅온정보")
    async def bangon_info(self, interaction: discord.Interaction):
        """
        이세돌 뱅온정보를 보여줍니다.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.wakscord.com/bangon") as resp:
                data = await resp.json()

        embed = discord.Embed(
            title=f"{data['info']['date']} 이세돌 뱅온정보",
            url=f"https://cafe.naver.com/steamindiegame/{data['info']['idx']}",
            color=0xEC528B,
        )

        for name, value in data["members"].items():
            info = "\n\n".join(value["info"]).strip()
            info = info if info else "\u200b"

            embed.add_field(name=f"{name}: {value['status']}", value=info)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Etc(bot))
