import discord

class Message():
    """
    Representation of one message and all its useful properties
    """
    def __init__(self, message: discord.Message, client: discord.Client):
        self.client = client
        self.channel_id = message.channel.id
        self.channel = message.channel
        self.message = message
        self.author = message.author
        self.author_name = self.author.name
        self.guild = message.guild

async def shame_slackbot(msg: Message):
    """
    Shame Slackbot
    """
    if msg.author.name == "YAGPDB.xyz":
        await msg.message.add_reaction("🍅")

async def novalue_react(msg: Message, custom_emoji_names: dict):
    """
    React in a nondescript way based on what was said
    """
    for raw_word in msg.message.content.split(" "):
        word = raw_word.lower()
        is_in_custom = False
        # Check if the word is in the name of a custom emoji; if so, react with that emoji.
        for custom_emoji_name in custom_emoji_names.keys():
            if word in custom_emoji_name.split("_") and word not in NoValueInfo.CUSTOM_BLACKLIST:
                is_in_custom = True
                await msg.message.add_reaction(custom_emoji_names[custom_emoji_name])
                # break
        # Otherwise, go based on the manually defined keywords
        if not is_in_custom and (word in NoValueInfo.KEYWORD_MAP.keys()):
            for listed_react in NoValueInfo.KEYWORD_MAP[word]:
                print(listed_react)
                await msg.message.add_reaction(listed_react)

class NoValueInfo:

    # Manually curated.
    KEYWORD_MAP = {
        "diamond": "💎🙌",
        "ass": "🍑",
        "booty": "🍑",
        "christmas": "🎄",
        "birthday": "🎉",
        "zibu": "❤️",
        "futaba": "❤️",
    }

    # These words will never trigger an automatic reaction with custom server-specific emoji reacts.
    CUSTOM_BLACKLIST = [
        "lmao",
    ]