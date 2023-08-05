import discord


class React():
    """
    Representation of one react and all its useful properties
    """
    def __init__(self, payload: discord.RawReactionActionEvent, client: discord.Client):
        self.client = client
        self.channel_id = payload.channel_id
        self.channel = client.get_channel(self.channel_id)
        self.reactor_id = payload.user_id
        self.reactor = payload.member
        self.reactor_name = self.reactor.name
        self.react = payload.emoji.name
        self.message_id  = payload.message_id
        self.guild = client.get_guild(payload.guild_id)

    @property
    async def message(self) -> discord.Message:
        return await self.channel.fetch_message(self.message_id)

async def mirror_react(reac: React, custom_emoji_names: dict):
    target_message = await reac.message
    for custom_emoji_name in custom_emoji_names.keys():
        if reac.react == custom_emoji_name:
            await target_message.add_reaction(custom_emoji_names[custom_emoji_name])
            return
    await target_message.add_reaction(reac.react)
    return


