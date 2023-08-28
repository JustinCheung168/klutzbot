import discord

from klutzbot.general.config import Config
from klutzbot.general.guild import AllGuildInfos


class React:
    """
    Representation of one react and all its useful properties
    """

    def __init__(
        self,
        payload: discord.RawReactionActionEvent,
        client: discord.Client,
        guild_infos: AllGuildInfos,
    ):
        self.client = client
        self.channel_id = payload.channel_id
        self.channel = client.get_channel(self.channel_id)
        self.reactor_id = payload.user_id
        self.reactor = payload.member
        self.reactor_name = self.reactor.name
        self.react = payload.emoji.name
        self.message_id = payload.message_id
        self.guild_id = payload.guild_id
        self.guild = client.get_guild(self.guild_id)
        self.guild_info = guild_infos[self.guild]

    @property
    async def message(self) -> discord.Message:
        return await self.channel.fetch_message(self.message_id)


class ReactResponder:
    async def respond(self, _: React):
        raise NotImplementedError


class GeneralReactResponder(ReactResponder):
    async def respond(self, rct: React):
        """Execute any possible responses to reacts."""

        # Reinforce reacts
        if rct.reactor_name in Config.ADMINS:
            await self.__mirror_react()

    async def __mirror_react(self, rct: React):
        custom_emoji_names = rct.guild_info.custom_emoji_names
        target_message = await rct.message
        for custom_emoji_name in custom_emoji_names.keys():
            if rct.react == custom_emoji_name:
                await target_message.add_reaction(custom_emoji_names[custom_emoji_name])
                return
        await target_message.add_reaction(rct.react)
        return
