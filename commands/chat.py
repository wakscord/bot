import traceback

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import check_manage_permission, fetch_subscribe_info, get_webhook


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.members: list[str] = None

    group = app_commands.Group(name="채팅", description="트위치 채팅 멤버 필터링")

    async def member_autocomplete(self, _: discord.Interaction, input: str):
        try:
            if self.members is None:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        "https://api.wakscord.xyz/members"
                    ) as response:
                        self.members = await response.json()

            return [
                app_commands.Choice(name=member, value=member)
                for member in filter(
                    lambda member: input == "" or input in member, self.members
                )
            ][:25]
        except Exception as e:
            traceback.print_exc()

    async def edit_subscribe(
        self, webhook: discord.Webhook, streamer: str, member: str, add: bool
    ):
        subs = await fetch_subscribe_info(webhook)

        if add:
            subs[streamer].append(member)
        else:
            subs[streamer].remove(member)

        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://api.wakscord.xyz/subscribe",
                json={
                    "url": webhook.url,
                    "subs": subs,
                },
            )

    @group.command(name="추가")
    @app_commands.rename(streamer="스트리머", member="멤버")
    @app_commands.autocomplete(member=member_autocomplete)
    @app_commands.choices(
        streamer=[
            app_commands.Choice(name="우왁굳", value="우왁굳"),
            app_commands.Choice(name="아이네", value="아이네"),
            app_commands.Choice(name="징버거", value="징버거"),
            app_commands.Choice(name="릴파", value="릴파"),
            app_commands.Choice(name="주르르", value="주르르"),
            app_commands.Choice(name="고세구", value="고세구"),
            app_commands.Choice(name="비챤", value="비챤"),
            app_commands.Choice(name="뢴트게늄", value="뢴트게늄"),
            app_commands.Choice(name="천양", value="천양"),
        ]
    )
    @app_commands.describe(
        streamer="왁타버스 스트리머",
        member="왁타버스 멤버",
    )
    async def chat_add_member(
        self, interaction: discord.Interaction, streamer: str, member: str
    ):
        """특정 멤버가 입력한 트위치 채팅을 디스코드로 전달 받습니다."""

        if not await check_manage_permission(interaction):
            return

        webhook = await get_webhook(interaction.channel)

        if webhook is None:
            return await interaction.response.send_message(
                "이 채널은 왁스코드에 구독 되어있지 않아요.", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True, thinking=True)

        await self.edit_subscribe(webhook, streamer, member, True)

        await interaction.followup.send(
            f"`{member} -> {streamer}` (이)가 추가되었습니다.", ephemeral=True
        )

    @group.command(name="제거")
    @app_commands.rename(streamer="스트리머", member="멤버")
    @app_commands.autocomplete(member=member_autocomplete)
    @app_commands.choices(
        streamer=[
            app_commands.Choice(name="우왁굳", value="우왁굳"),
            app_commands.Choice(name="아이네", value="아이네"),
            app_commands.Choice(name="징버거", value="징버거"),
            app_commands.Choice(name="릴파", value="릴파"),
            app_commands.Choice(name="주르르", value="주르르"),
            app_commands.Choice(name="고세구", value="고세구"),
            app_commands.Choice(name="비챤", value="비챤"),
            app_commands.Choice(name="뢴트게늄", value="뢴트게늄"),
            app_commands.Choice(name="천양", value="천양"),
        ]
    )
    @app_commands.describe(
        streamer="왁타버스 스트리머",
        member="왁타버스 멤버",
    )
    async def chat_remove_member(
        self, interaction: discord.Interaction, streamer: str, member: str
    ):
        """특정 멤버가 입력한 트위치 채팅을 디스코드로 전달 받지 않습니다."""

        if not await check_manage_permission(interaction):
            return

        webhook = await get_webhook(interaction.channel)

        if webhook is None:
            return await interaction.response.send_message(
                "이 채널은 왁스코드에 구독 되어있지 않아요.", ephemeral=True
            )

        await interaction.response.defer(ephemeral=True, thinking=True)

        await self.edit_subscribe(webhook, streamer, member, False)

        await interaction.followup.send(
            f"`{member} -> {streamer}` (이)가 제거되었습니다.", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Chat(bot))
