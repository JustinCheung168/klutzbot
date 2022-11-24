import discord
import klutzbot.command_defs.message

async def shame_slackbot(message: discord.Message, client: discord.Client):
    """
    Shame Slackbot
    """
    if message.author.name == "YAGPDB.xyz":
        await message.add_reaction("🍅")

# Manually curated. Not sure how one would algorithmically assign this.
KEYWORD_MAP = {
    "diamond": "💎🙌",
    "ass": "🍑",
    "booty": "🍑",
    "christmas": "🎄",
    "birthday": "🎉",
    "zibu": "❤️",
    "futaba": "❤️",
    "league": "🤓"
}
async def novalue_react(message: discord.Message, client: discord.Client, custom_emoji_names: dict[str,discord.Emoji]):
    """
    React in a nondescript way based on what was said
    """
    msg = klutzbot.command_defs.message.Message(message, client)

    for raw_word in msg.message.content.split(" "):
        word = raw_word.lower()
        # Check if the word is in the name of a custom emoji; if so, react with that emoji.
        for custom_emoji_name in custom_emoji_names.keys():
            if word in custom_emoji_name.split("_"):
                await msg.message.add_reaction(custom_emoji_names[custom_emoji_name])
                break
        # Otherwise, go based on the manually defined keywords
        if word in KEYWORD_MAP.keys():
            for listed_react in KEYWORD_MAP[word]:
                await msg.message.add_reaction(listed_react)



            


