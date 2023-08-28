"""Guild-specific information"""
import discord


class GuildInfo:
    def __init__(self):
        self.custom_emoji_names: dict[str, discord.Emoji] = {}

    def collect(self, guild: discord.Guild):
        self.custom_emoji_names = {emoji.name: emoji for emoji in guild.emojis}


class AllGuildInfos:
    def __init__(self):
        self.guild_infos: dict[discord.Guild, GuildInfo] = {}

    def __getitem__(self, guild: discord.Guild) -> GuildInfo:
        return self.guild_infos[guild]

    def add_guild_info(self, guild: discord.Guild):
        self.guild_infos[guild] = GuildInfo()
        self.guild_infos[guild].collect(guild)
