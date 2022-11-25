#!/usr/bin/env python3
import sys
import os

import discord
from dotenv import load_dotenv

import klutzbot.command_defs.message
import klutzbot.command_defs.novalue
import klutzbot.command_defs.react

intents = discord.Intents.all()
client = discord.Client(intents=intents)
custom_emoji_names = {}

load_dotenv()

def choose_token(cli_args: list[str]):
    if len(cli_args) == 2:
        if cli_args[1] == "teatimebot":
            token = "TEATIMEBOT_TOKEN"
        else:
            token = "KLUTZBOT_TOKEN"
    else:
        token = "KLUTZBOT_TOKEN"
    return token

@client.event
async def on_ready():
    """
    Runs on bot startup and lets us know which servers the bot successfully connected to.
    """
    print(f'{client.user.name} is connected to Discord!')
    for guild in client.guilds:
        print(f'Connected to {guild.name}')
        custom_emoji_names[guild] = {emoji.name:emoji for emoji in guild.emojis}

@client.event
async def on_message(message: discord.Message):
    """
    Runs every time any message is sent. Handles responses to messages.
    """
    if message.author == client.user: #Immediately leave if this bot sent the message to prevent responses of bot to itself.
        return

    # Shame Slackbot
    if message.author.name == "YAGPDB.xyz":
        await klutzbot.command_defs.novalue.shame_slackbot(message, client)
    # Michael's requested no-value-added reacts
    elif message.author.name == "firemike":
        await klutzbot.command_defs.novalue.novalue_react(message, client, custom_emoji_names[message.guild])

    if len(message.content) > 0:
        if (message.content[0] == "!"): #Command handling
            await klutzbot.command_defs.message.execute_command(message, client)
    elif (len(message.embeds) > 0): #Pure embed handling
        pass

@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """
    Actions to taken upon any react being added.
    """
    await klutzbot.command_defs.react.respond_to_react(payload, client)

client.run(os.getenv(choose_token(sys.argv)))
