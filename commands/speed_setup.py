from enum import Enum
from typing import Optional

import aiohttp
import discord
from discord.ext import commands

from utils import check_manage_permission


class SpeedSetupMethod(Enum):
    ALL = 1
    MEMBER = 2
    DETAIL = 3


class SubscribeItem(Enum):
    BANGON_BANGJE = ["뱅온", "방제", "뱅종"]
    CHAT = [
        "우왁굳",
        "아이네",
        "징버거",
        "릴파",
        "주르르",
        "고세구",
        "비챤",
    ]
    ALERT = ["유튜브", "토토", "카페"]


class SpeedSetupView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self._method = SpeedSetupMethod.ALL
        self._streamers = [
            "우왁굳",
            "아이네",
            "징버거",
            "릴파",
            "주르르",
            "고세구",
            "비챤",
        ]

        self.session: aiohttp.ClientSession = None

    @property
    def description(self):
        text = "## 왁스코드 빠른 설정\n"

        if self._method == SpeedSetupMethod.ALL:
            text += f"### 만들어질 채널\n- 왁스코드"
        elif self._method == SpeedSetupMethod.MEMBER:
            text += f"### 만들어질 채널\n"
            for streamer in self._streamers:
                text += f"- {streamer}\n"
        elif self._method == SpeedSetupMethod.DETAIL:
            text += f"### 만들어질 채널\n"
            for streamer in self._streamers:
                text += f"- {streamer}-뱅온-방제\n"
                text += f"- {streamer}-채팅\n"
                text += f"- {streamer}-알림\n\n"

        return text

    @discord.ui.button(
        label="한 채널에서 모든 알림 받기", row=0, style=discord.ButtonStyle.green
    )
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._method = SpeedSetupMethod.ALL
        button.style = discord.ButtonStyle.green

        self.member.style = discord.ButtonStyle.grey
        self.detail.style = discord.ButtonStyle.grey

        embed = interaction.message.embeds[0]
        embed.description = self.description
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(label="멤버별로 나눠진 채널에서 알림 받기", row=0)
    async def member(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._method = SpeedSetupMethod.MEMBER
        button.style = discord.ButtonStyle.green

        self.all.style = discord.ButtonStyle.grey
        self.detail.style = discord.ButtonStyle.grey

        embed = interaction.message.embeds[0]
        embed.description = self.description
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(label="나눠진 채널을 더 세분화해서 받기", row=0)
    async def detail(self, interaction: discord.Interaction, button: discord.ui.Button):
        self._method = SpeedSetupMethod.DETAIL
        button.style = discord.ButtonStyle.green

        self.all.style = discord.ButtonStyle.grey
        self.member.style = discord.ButtonStyle.grey

        embed = interaction.message.embeds[0]
        embed.description = self.description
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.select(
        placeholder="알림을 받을 스트리머를 선택하세요",
        options=[
            discord.SelectOption(label="우왁굳", default=True),
            discord.SelectOption(label="아이네", default=True),
            discord.SelectOption(label="징버거", default=True),
            discord.SelectOption(label="릴파", default=True),
            discord.SelectOption(label="주르르", default=True),
            discord.SelectOption(label="고세구", default=True),
            discord.SelectOption(label="비챤", default=True),
            discord.SelectOption(label="뢴트게늄"),
            discord.SelectOption(label="천양"),
            discord.SelectOption(label="빅토리"),
        ],
        row=1,
        min_values=1,
        max_values=9,
    )
    async def streamer(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self._streamers = select.values

        for option in select.options:
            option.default = option.label in self._streamers

        embed = interaction.message.embeds[0]
        embed.description = self.description
        await interaction.response.edit_message(view=self, embed=embed)

    async def _subscribe(
        self,
        channel: discord.TextChannel,
        streamers: list[str],
        item: Optional[SubscribeItem] = None,
    ):
        if self.session is None:
            self.session = aiohttp.ClientSession()

        data = {}

        for streamer in streamers:
            if item is None:
                data[streamer] = (
                    SubscribeItem.BANGON_BANGJE.value
                    + SubscribeItem.CHAT.value
                    + SubscribeItem.ALERT.value
                )
            else:
                data[streamer] = item.value

        webhook = await channel.create_webhook(
            name="왁스코드", reason="왁스코드 빠른 설정으로 만들어진 웹후크"
        )

        await self.session.post(
            "https://api.wakscord.xyz/subscribe",
            json={
                "url": webhook.url,
                "subs": data,
            },
        )

    @discord.ui.button(
        label="설정하기",
        emoji="➡️",
        style=discord.ButtonStyle.blurple,
        row=2,
    )
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=None, embed=None, content="채널 생성 중..."
        )

        channels: list[discord.TextChannel] = []

        if self._method == SpeedSetupMethod.ALL:
            channel = await interaction.guild.create_text_channel("왁스코드")
            await self._subscribe(channel, self._streamers)
            channels.append(channel)

        elif self._method == SpeedSetupMethod.MEMBER:
            for streamer in self._streamers:
                channel = await interaction.guild.create_text_channel(streamer)
                await self._subscribe(channel, [streamer])
                channels.append(channel)

        elif self._method == SpeedSetupMethod.DETAIL:
            for streamer in self._streamers:
                category = await interaction.guild.create_category(streamer)
                for channel_name, item in (
                    ("뱅온-방제", SubscribeItem.BANGON_BANGJE),
                    ("채팅", SubscribeItem.CHAT),
                    ("알림", SubscribeItem.ALERT),
                ):
                    channel = await category.create_text_channel(
                        f"{streamer}-{channel_name}"
                    )

                    await self._subscribe(channel, [streamer], item=item)
                    channels.append(channel)

        content = "## 왁스코드 구독 완료!\n\n"

        for channel in channels:
            content += f"- {channel.mention}\n"

        await interaction.edit_original_response(content=content)


class SpeedSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @discord.app_commands.command(name="빠른설정")
    async def speed_setup(self, interaction: discord.Interaction):
        """쉽고 빠르게 왁스코드 알림을 설정합니다."""

        if not await check_manage_permission(interaction):
            return

        view = SpeedSetupView()

        embed = discord.Embed(description=view.description, color=0x7EB49F)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SpeedSetup(bot))
