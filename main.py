#!/usr/bin/env python3
import sys

import discord

import klutzbot.bot
import klutzbot.command_defs.message
import klutzbot.command_defs.react

# Global bot information holder
bot = klutzbot.bot.Bot()

# Connect Discord bot interfaces to allow bot to listen for Discord events and act accordingly

@bot.client.event
async def on_ready():
    """
    Runs on bot startup and lets us know which servers the bot successfully connected to.
    """
    bot.on_ready()

@bot.client.event
async def on_message(message: discord.Message):
    """
    Runs every time any message is sent. Handles responses to messages.
    """
    if message.author == bot.client.user: 
        return #Immediately leave if this bot sent the message to prevent responses of bot to itself.

    if len(message.content) > 0:
        #Command handling
        if (message.content[0:len(bot.cmd_start)] == bot.cmd_start): 
            await bot.execute_command(message)
        #Non-command message handling
        else: 
            await bot.respond_to_message(message)
    #Pure embed handling
    elif (len(message.embeds) > 0): 
        pass

@bot.client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """
    Actions to taken upon any react being added.
    """
    await bot.respond_to_react(payload)

if __name__ == "__main__":
    bot.run(sys.argv)
