#!/usr/bin/env python3
import discord
import os
from dotenv import load_dotenv


def generate_client():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    return client, TOKEN

class KlutzBotInstructor():
    """
    Listens for input from Discord, then tells KlutzBot to crunch the numbers,
    then outputs KlutzBot's result.
    """
    def __init__(self, client):
        

        @client.event
        async def on_ready():
            """
            Do startup things
            """
            pass
        
        @client.event
        async def on_message(message):
            """
            Runs every time any message is sent. Handles responses to messages.
            """
            if (len(message.embeds) == 0):
                pass
                #then this is a normal message.
            elif (len(message.embeds) == 1):
                pass
                #then this is an embed-only message
            else:
                raise Exception("Don't know what to do here")

        @client.event
        async def on_raw_reaction_add(payload):
            pass
            #react response


class KlutzBotInstruction():
    """
    A standardized instruction format that KlutzBotInstructor tells KlutzBot for any given instruction.

    Attributes:
        instruction_type: One of "message", "embed", "command", or "react".
        sender: The int ID of the user who placed the input.

        message: 

    """
    def __init__(self):
        pass


    




def main():
    client, TOKEN = generate_client()
    kbi = KlutzBotInstructor(client)
    client.run(TOKEN)

if __name__ == "__main__":
    main()