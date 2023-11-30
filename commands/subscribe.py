from enum import Enum, auto
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from utils import check_manage_permission, get_webhook

if TYPE_CHECKING:
    from discord import Interaction
    from typing_extensions import Self

    from bot import WakscordBot


class DeleteWebhookResult(Enum):
    DELETE = auto()
    DISMISS = auto()
    CANCEL = auto()


class DeleteWebhookView(discord.ui.View):
    def __init__(self, webhook: discord.Webhook) -> None:
        super().__init__(timeout=None)

        self.webhook = webhook
        self.result: DeleteWebhookResult = DeleteWebhookResult.CANCEL

    @discord.ui.button(label="삭제 후 새로 구독하기", style=discord.ButtonStyle.primary, row=0)
    async def delete(
        self, _: Interaction[WakscordBot], __: discord.ui.Button[Self]
    ) -> None:
        await self.webhook.delete()

        self.result = DeleteWebhookResult.DELETE

        self.stop()

    @discord.ui.button(label="무시하고 계속 진행하기", style=discord.ButtonStyle.danger, row=1)
    async def dismiss(
        self, _: Interaction[WakscordBot], __: discord.ui.Button[Self]
    ) -> None:
        self.result = DeleteWebhookResult.DISMISS

        self.stop()

    @discord.ui.button(label="취소하기", style=discord.ButtonStyle.secondary, row=2)
    async def cancel(
        self, interaction: Interaction[WakscordBot], _: discord.ui.Button[Self]
    ) -> None:
        self.result = DeleteWebhookResult.CANCEL

        await interaction.response.edit_message(content="취소되었습니다.", view=None)

        self.stop()


class Subscribe(commands.Cog):
    def __init__(self, bot: WakscordBot) -> None:
        self.bot = bot

    @discord.app_commands.command(name="구독")
    async def subscribe(self, interaction: Interaction[WakscordBot]) -> None:
        """이 채널의 왁스코드 알림을 웹사이트에서 설정합니다."""
        assert isinstance(interaction.channel, discord.TextChannel)

        if not await check_manage_permission(interaction):
            return

        webhook = await get_webhook(interaction.channel)
        if webhook is not None:
            view = DeleteWebhookView(webhook)
            await interaction.response.send_message(
                "이 채널에는 이미 왁스코드 봇으로 구독된 웹후크가 있어요.\n어떻게 할까요?\n\n(`/설정 변경` 커맨드로 기존 설정을 변경할 수 있어요.)",
                view=view,
                ephemeral=True,
            )

            await view.wait()

            if view.result == DeleteWebhookResult.CANCEL:
                return
        else:
            await interaction.response.defer(ephemeral=True, thinking=True)

        webhook = await interaction.channel.create_webhook(
            name="왁스코드", reason="왁스코드 빠른 설정으로 만들어진 웹후크"
        )

        await interaction.edit_original_response(
            content=f"[여기](<https://wakscord.xyz/?make={webhook.id}/{webhook.token}>)에서 구독을 진행해주세요!",
            view=None,
        )


async def setup(bot: WakscordBot) -> None:
    await bot.add_cog(Subscribe(bot))
