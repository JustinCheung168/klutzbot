#!/usr/bin/env python3
import sys
import os
import pydantic

import discord
from dotenv import load_dotenv

intents = discord.Intents.all()
client = discord.Client(intents=intents)

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


@client.event
async def on_message(message: discord.Message):
    """
    Runs every time any message is sent. Handles responses to messages.
    """
    if message.author == client.user: #Immediately leave if this bot sent the message to prevent responses of bot to itself.
        return
    if len(message.content) > 0:
        if (message.content[0] == "!"): #Command handling
            await execute_command(message)
    elif (len(message.embeds) > 0): #Pure embed handling
        embedded = message.embeds[0]


async def execute_command(message: discord.Message):
    # Interpret message as a command
    channel = client.get_channel(message.channel.id)

    message_split = message.content.split(" ")
    command = message_split[0].lower()
    if len(message_split) > 0:
        args = message_split[1:]
    else:
        args = []
    
    # Interpret specific commands
    say_cmd = "!say"
    if (command == say_cmd) and (message.author.name == "klutz"):
        await say(args, say_cmd, channel)

async def say(args: list[str], say_cmd, channel):
    if len(args) == 2:
        target_channel = client.get_channel(int(args[0]))
        host_message = args[1]
        await target_channel.send(host_message)
    else:
        await channel.send(f"Need exactly two arguments: {say_cmd} <id of channel to send message to> <message>")




@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """
    Actions to taken upon any react being added.
    """
    pass



client.run(os.getenv(choose_token(sys.argv)))
