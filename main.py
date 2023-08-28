#!/usr/bin/env python3
import sys

import discord

import klutzbot.bot

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
        return  # Immediately leave if this bot sent the message to prevent responses of bot to itself.

    # Message handling
    await bot.respond_to_message(message)


@bot.client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """
    Actions to taken upon any react being added.
    """
    # React handling
    await bot.respond_to_react(payload)


if __name__ == "__main__":
    bot.run(sys.argv)
