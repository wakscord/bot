from typing import Optional

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import check_manage_permission, fetch_subscribe_info, get_webhook


class MemberSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.member = None

    @discord.ui.button(label="우왁굳", style=discord.ButtonStyle.primary, row=0)
    async def wak(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "우왁굳"
        self.stop()

    @discord.ui.button(label="아이네", style=discord.ButtonStyle.primary, row=0)
    async def ine(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "아이네"
        self.stop()

    @discord.ui.button(label="징버거", style=discord.ButtonStyle.primary, row=0)
    async def jing(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "징버거"
        self.stop()

    @discord.ui.button(label="릴파", style=discord.ButtonStyle.primary, row=1)
    async def lilpa(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "릴파"
        self.stop()

    @discord.ui.button(label="주르르", style=discord.ButtonStyle.primary, row=1)
    async def jururu(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "주르르"
        self.stop()

    @discord.ui.button(label="고세구", style=discord.ButtonStyle.primary, row=1)
    async def gosegu(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "고세구"
        self.stop()

    @discord.ui.button(label="비챤", style=discord.ButtonStyle.primary, row=2)
    async def viichan(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.member = "비챤"
        self.stop()

    @discord.ui.button(label="뢴트게늄", style=discord.ButtonStyle.primary, row=2)
    async def rent(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "뢴트게늄"
        self.stop()

    @discord.ui.button(label="천양", style=discord.ButtonStyle.primary, row=2)
    async def cheon(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.member = "천양"
        self.stop()


class AlertSelectView(discord.ui.View):
    map = {
        "뱅온 알림": "뱅온",
        "뱅종 알림": "뱅종",
        "방제 변경 알림": "방제",
        "유튜브 업로드 알림": "유튜브",
        "토토 결과 알림": "토토",
        "왁물원 글 알림": "카페",
    }

    def __init__(self, webhook: discord.Webhook, subs: dict, member: str):
        super().__init__(timeout=None)

        self.webhook = webhook
        self.subs = subs
        self.member = member

        for children in self.children:
            children.style = (
                discord.ButtonStyle.green
                if self.map[children.label] in subs[member]
                else discord.ButtonStyle.secondary
            )

    async def edit_subscribe(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        enable = button.style == discord.ButtonStyle.secondary

        if enable:
            self.subs[self.member].append(self.map[button.label])
        else:
            self.subs[self.member].remove(self.map[button.label])

        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://api.wakscord.com/subscribe",
                json={
                    "url": self.webhook.url,
                    "subs": self.subs,
                },
            )

        await interaction.response.edit_message(
            content=f"{self.member}의 {button.label}을 {'활성화' if enable else '비활성화'}했어요.",
            view=None,
        )

    @discord.ui.button(label="뱅온 알림", style=discord.ButtonStyle.green)
    async def bangon_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="방제 변경 알림", style=discord.ButtonStyle.green)
    async def title_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="뱅종 알림", style=discord.ButtonStyle.green)
    async def end_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="유튜브 업로드 알림", style=discord.ButtonStyle.green)
    async def youtube_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="토토 결과 알림", style=discord.ButtonStyle.green)
    async def toto_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="왁물원 글 알림", style=discord.ButtonStyle.green)
    async def waxmuseum_alert(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)


class ChatAlertSelectView(discord.ui.View):
    map = {
        "우왁굳": ["우왁굳"],
        "이세돌": [
            "아이네",
            "징버거",
            "릴파",
            "주르르",
            "고세구",
            "비챤",
        ],
        "고멤": [
            "곽춘식",
            "권민",
            "김치만두번영택사스가",
            "단답벌레",
            "도파민 박사",
            "독고혜지",
            "뢴트게늄",
            "부정형인간",
            "비밀소녀",
            "비즈니스킴",
            "왁파고",
            "이덕수 할아바이",
            "카르나르 융터르",
            "풍신",
            "프리터",
            "해루석",
            "히키킹",
        ],
        "교멤": [
            "닌닌",
            "데스해머 쵸로키",
            "미미짱짱세용",
            "미스 발렌타인",
            "버터우스 3세",
            "불곰",
            "빅토리",
            "사랑전도사 젠투",
            "성기사 샬롯",
            "수셈이",
            "시리안 레인",
            "아마데우스최",
            "아이 쓰께끼",
            "진희",
            "철도왕 길버트",
            "캡틴 설리반",
            "크리즈",
        ],
    }

    def __init__(self, webhook: discord.Webhook, subs: dict, member: str):
        super().__init__(timeout=None)

        self.webhook = webhook
        self.subs = subs
        self.member = member

        for children in self.children:
            children.style = discord.ButtonStyle.green

            for sub in self.map[children.label]:
                if sub not in subs[member]:
                    children.style = discord.ButtonStyle.secondary
                    break

    async def edit_subscribe(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        enable = button.style == discord.ButtonStyle.secondary

        if enable:
            self.subs[self.member].extend(self.map[button.label])
        else:
            for sub in self.map[button.label]:
                self.subs[self.member].remove(sub)

        async with aiohttp.ClientSession() as session:
            await session.post(
                "https://api.wakscord.com/subscribe",
                json={
                    "url": self.webhook.url,
                    "subs": self.subs,
                },
            )

        await interaction.response.edit_message(
            content=f"{self.member}의 {button.label}을 {'활성화' if enable else '비활성화'}했어요.",
            view=None,
        )

    @discord.ui.button(label="우왁굳", style=discord.ButtonStyle.green)
    async def wakgood(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="이세돌", style=discord.ButtonStyle.green)
    async def isedol(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="고멤", style=discord.ButtonStyle.green)
    async def gomem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.edit_subscribe(interaction, button)

    @discord.ui.button(label="교멤", style=discord.ButtonStyle.green)
    async def gyomem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.edit_subscribe(interaction, button)


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="설정", description="왁스코드 알림 설정")

    async def get_info(
        self, interaction: discord.Interaction, none: bool = False
    ) -> Optional[dict]:
        if not await check_manage_permission(interaction):
            return

        webhook = await get_webhook(interaction.channel)

        if webhook is None:
            await interaction.response.send_message(
                "이 채널은 왁스코드에 구독 되어있지 않아요.", ephemeral=True
            )

            return None

        await interaction.response.defer(ephemeral=True, thinking=True)

        info = await fetch_subscribe_info(webhook)

        if info is None:
            if none:
                await interaction.edit_original_response(
                    content="구독 정보가 존재하지 않습니다."
                )
                return None
            else:
                return webhook, {
                    "우왁굳": [],
                    "아이네": [],
                    "징버거": [],
                    "릴파": [],
                    "주르르": [],
                    "고세구": [],
                    "비챤": [],
                    "뢴트게늄": [],
                    "천양": [],
                }

        return webhook, info

    @group.command(name="변경")
    async def set_settings(self, interaction: discord.Interaction):
        """이 채널의 왁스코드 설정을 웹사이트에서 변경합니다."""

        if not await check_manage_permission(interaction):
            return

        webhook = await get_webhook(interaction.channel)

        if webhook is None:
            return await interaction.response.send_message(
                "이 채널은 왁스코드에 구독 되어있지 않아요.", ephemeral=True
            )

        await interaction.response.send_message(
            f"[여기](<https://app.wakscord.com/waktaverse?make={webhook.id}/{webhook.token}>)에서 설정을 변경할 수 있어요.",
            ephemeral=True,
        )

    @group.command(name="보기")
    async def show_settings(self, interaction: discord.Interaction):
        """이 채널의 알림 설정을 봅니다."""

        _, info = await self.get_info(interaction)

        if info is None:
            return

        embed = discord.Embed(
            title="왁스코드 구독 정보",
            color=0x6DB69E,
        )

        for key, value in info.items():
            if value[0] is None:
                continue

            embed.add_field(
                name=key, value="\n".join([f"- {v}" for v in value]), inline=False
            )

        await interaction.edit_original_response(embed=embed)

    @group.command(name="알림")
    async def set_alert_settings(self, interaction: discord.Interaction):
        """이 채널의 알림 설정을 변경합니다."""

        webhook, info = await self.get_info(interaction, none=False)
        view = MemberSelectView()

        await interaction.edit_original_response(
            content="어떤 멤버의 알림을 설정할까요?", view=view
        )

        await view.wait()

        if view.member is None:
            return await interaction.edit_original_response(
                content="취소되었습니다.", view=None
            )

        await interaction.edit_original_response(
            content=f"{view.member}의 어떤 알림 카테고리를 켜거나 끌까요?",
            view=AlertSelectView(webhook, info, view.member),
        )

    @group.command(name="채팅")
    async def set_chat_settings(self, interaction: discord.Interaction):
        """이 채널의 트위치 채팅 알림 설정을 변경합니다."""

        webhook, info = await self.get_info(interaction, none=False)
        view = MemberSelectView()

        await interaction.edit_original_response(
            content="어떤 멤버의 채팅 알림을 설정할까요?", view=view
        )

        await view.wait()

        if view.member is None:
            return await interaction.edit_original_response(
                content="취소되었습니다.", view=None
            )

        await interaction.edit_original_response(
            content=f"{view.member}의 어떤 채팅 알림 카테고리를 켜거나 끌까요?",
            view=ChatAlertSelectView(webhook, info, view.member),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
