"""Bot data and connections."""
import os

import discord
from dotenv import load_dotenv

import klutzbot.command_defs.message
import klutzbot.command_defs.command
import klutzbot.command_defs.react


class Bot:

    owner = "klutzeh"

    def __init__(self):
        """Collection of data and connections specific to this bot."""

        # Required for login
        self.intents = discord.Intents.all()
        self.client = discord.Client(intents=self.intents)

        # Extra information to collect
        self.guild_infos: dict[str, GuildInfo] = {}


    def run(self, cli_args: list[str]):
        """Start the bot."""

        # Determine which token to log in this bot as.
        load_dotenv()
        if len(cli_args) == 2:
            if cli_args[1] == "teatimebot":
                self.token_name = "TEATIMEBOT_TOKEN"
            else:
                self.token_name = "KLUTZBOT_TOKEN"
        else:
            self.token_name = "KLUTZBOT_TOKEN"
        token = os.getenv(self.token_name)

        # Use this token to connect the bot to the client.
        self.client.run(token)
        return
    
    def on_ready(self):
        print(f'{self.client.user.name} is connected to Discord!')
        for guild in self.client.guilds:
            print(f'Connected to {guild.name}')
            # Collect info about each guild
            self.guild_infos[guild] = GuildInfo()
            self.guild_infos[guild].collect(guild)   

    async def respond_to_message(self, message: discord.Message):
        msg = klutzbot.command_defs.message.Message(message, self.client)

        # Shame Slackbot
        if msg.author.name == "YAGPDB.xyz":
            await klutzbot.command_defs.message.shame_slackbot(msg)
        # Michael's requested no-value-added reacts
        if msg.author.name == "firemike" or msg.author.name == self.owner:
            await klutzbot.command_defs.message.novalue_react(msg, self.guild_infos[msg.guild].custom_emoji_names)
 
    async def execute_command(self, message: discord.Message):
        """
        Interpret a message as a command.
        Commands are assumed to be formatted as:
            !<command name> <arg1> <arg2> <arg3> ...
        """
        cmd = klutzbot.command_defs.command.Command(message, self.client)
        
        # Interpret specific commands
        if (cmd.command == "!say") and (cmd.author_name == self.owner):
            await klutzbot.command_defs.command.say(cmd)
        if (cmd.command == "!reply") and (cmd.author_name == self.owner):
            await klutzbot.command_defs.command.reply(cmd)
        if (cmd.command == "!react") and (cmd.author_name == self.owner):
            await klutzbot.command_defs.command.react(cmd)

    async def respond_to_react(self, payload: discord.RawReactionActionEvent):
        """
        Take any needed actions in response to a react.
        """
        reac = klutzbot.command_defs.react.React(payload, self.client)

        if reac.reactor_name == self.owner:
            await klutzbot.command_defs.react.mirror_react(reac, self.guild_infos[reac.guild].custom_emoji_names)
            


class GuildInfo:
    def __init__(self):
        """Guild-specific information collection"""
        self.custom_emoji_names: dict[str, discord.Emoji] = {}
        
    def collect(self, guild: discord.Guild):
        self.custom_emoji_names = {emoji.name:emoji for emoji in guild.emojis}

