import discord

from klutzbot.general.config import Config, NoValueConfig
from klutzbot.general.guild import AllGuildInfos


class Message:
    """
    Representation of one message and all its useful properties
    """

    def __init__(
        self,
        message: discord.Message,
        client: discord.Client,
        guild_infos: AllGuildInfos,
    ):
        self.client = client
        self.channel_id = message.channel.id
        self.channel = message.channel
        self.message = message
        self.author = message.author
        self.author_name = self.author.name
        self.guild = message.guild
        self.guild_info = guild_infos[self.guild]
        self.embeds = message.embeds
        # A "pure embed" is a message whose only content is an embed.
        if (len(message.content) > 0) and (len(message.embeds) > 0):
            self.pure_embed = message.embeds[0]
        else:
            self.pure_embed = None


class MessageResponder:
    async def respond(self, _: Message):
        raise NotImplementedError


class GeneralMessageResponder(MessageResponder):
    async def respond(self, msg: Message):
        """Execute any possible responses to messages."""

        # Automatically shame a user (Slackbot)
        if msg.author_name in Config.BULLY_VICTIMS:
            await self.__shame(msg)

        # Michael's requested no-value-added reacts
        if msg.author_name in Config.NO_VALUE_USERS:
            await self.__novalue_react(msg)

    async def __shame(self, msg: Message):
        """
        Shame the message sender
        """
        await msg.message.add_reaction("🍅")

    async def __novalue_react(self, msg: Message):
        """
        React in a nondescript way based on what was said
        """
        custom_emoji_names = msg.guild_info.custom_emoji_names
        for raw_word in msg.message.content.split(" "):
            word = raw_word.lower()
            is_in_custom = False
            # Check if the word is in the name of a custom emoji; if so, react with that emoji.
            for custom_emoji_name in custom_emoji_names.keys():
                if (
                    word in custom_emoji_name.split("_")
                    and word not in NoValueConfig.CUSTOM_BLACKLIST
                ):
                    is_in_custom = True
                    await msg.message.add_reaction(
                        custom_emoji_names[custom_emoji_name]
                    )
                    # break
            # Otherwise, go based on the manually defined keywords
            if not is_in_custom and (word in NoValueConfig.KEYWORD_MAP.keys()):
                for listed_react in NoValueConfig.KEYWORD_MAP[word]:
                    print(listed_react)
                    await msg.message.add_reaction(listed_react)
