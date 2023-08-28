"""Bot data and connections."""
import os

import discord
from dotenv import load_dotenv

import klutzbot.general.command
import klutzbot.general.guild
import klutzbot.general.message
import klutzbot.general.react
import klutzbot.teatime.command
import klutzbot.teatime.message


class Bot:
    def __init__(self):
        """Collection of data and connections specific to this bot."""

        # Required for login
        self.intents = discord.Intents.all()
        self.client = discord.Client(intents=self.intents)

        # Extra information to collect
        self.guild_infos = klutzbot.general.guild.AllGuildInfos()

        # Handlers for message response and command running
        self.general_cmd_runner = klutzbot.general.command.GeneralCommandRunner()
        self.general_msg_responder = klutzbot.general.message.GeneralMessageResponder()
        self.general_rct_responder = klutzbot.general.react.GeneralReactResponder()

        self.tt_cmd_runner = klutzbot.teatime.command.TTCommandRunner()
        self.tt_msg_responder = klutzbot.teatime.message.TTMessageResponder()

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
        print(f"{self.client.user.name} is connected to Discord!")
        for guild in self.client.guilds:
            print(f"Connected to {guild.name}")
            # Collect info about each guild
            self.guild_infos.add_guild_info(guild)

    async def respond_to_message(self, message: discord.Message):
        """ """

        # Decide if the message is a command, and if so, what kind of command.
        # Commands are assumed to be formatted as:
        #     <start string><command name> <arg1> <arg2> <arg3> ...
        # General command handling
        if (
            message.content[: len(klutzbot.general.command.GeneralCommand.START)]
            == klutzbot.general.command.GeneralCommand.START
        ):
            cmd = klutzbot.general.command.GeneralCommand(
                message, self.client, self.guild_infos
            )
            await self.general_cmd_runner.run(cmd)
        # Teatime bot functionality is provided using Mudae's command start character
        elif (
            message.content[: len(klutzbot.teatime.command.TTCommand.START)]
            == klutzbot.teatime.command.TTCommand.START
        ):
            cmd = klutzbot.teatime.command.TTCommand(
                message, self.client, self.guild_infos
            )
            await self.tt_cmd_runner.run(cmd)
        else:
            msg = klutzbot.general.message.Message(
                message, self.client, self.guild_infos
            )
            await self.general_msg_responder.respond(msg)
            await self.tt_msg_responder.respond(msg)

    async def respond_to_react(self, react: discord.RawReactionActionEvent):
        """
        Take any needed actions in response to a react.
        """
        rct = klutzbot.general.react.React(react, self.client, self.guild_infos)
        await rct.respond()
