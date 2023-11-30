from typing import Optional

import aiohttp
from discord import Interaction, TextChannel, Webhook


async def check_manage_permission(interaction: Interaction) -> bool:
    if not interaction.channel.permissions_for(interaction.user).manage_channels:
        await interaction.response.send_message(
            "사용자님에게 **채널 관리하기** 권한이 없어요.", ephemeral=True
        )

        return False

    if not interaction.channel.permissions_for(interaction.guild.me).manage_channels:
        await interaction.response.send_message(
            "왁스코드 봇에 **채널 관리하기** 권한이 없어요.", ephemeral=True
        )

        return False

    if not interaction.channel.permissions_for(interaction.guild.me).manage_webhooks:
        await interaction.response.send_message(
            "왁스코드 봇에 **웹후크 관리하기** 권한이 없어요.", ephemeral=True
        )

        return False

    return True


async def get_webhook(channel: TextChannel) -> Webhook | None:
    webhooks = await channel.webhooks()

    for webhook in webhooks:
        if webhook.user == channel.guild.me:
            return webhook


async def fetch_subscribe_info(webhook: Webhook) -> Optional[dict]:
    key = f"{webhook.id}/{webhook.token}"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.wakscord.xyz/hookInfo", json={"keys": [key]}
        ) as response:
            if response.status != 200:
                return None

            data = await response.json()

            return data[key]
