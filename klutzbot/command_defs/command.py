import discord

import klutzbot.command_defs.message


class Command(klutzbot.command_defs.message.Message):
    """
    Representation of one command and all its useful properties
    """

    start = "!"

    def __init__(self, message: discord.Message, client: discord.Client):
        super().__init__(message, client)
        # Strip out the start command indicator
        message_split = message.content[len(self.start):].split(" ")
        self.command = message_split[0].lower()
        if len(message_split) > 0:
            self.args = message_split[1:]
        else:
            self.args = []
        self.num_args = len(self.args)

async def say(cmd: Command):
    help_str=f"Need exactly two arguments: {Command.start}{cmd.command} <id of channel to send message to> <message>"
    if cmd.num_args >= 2:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        host_message = ' '.join(cmd.args[1:])
        await target_channel.send(host_message)
    else:
        await cmd.channel.send(help_str)

async def reply(cmd: Command):
    help_str=f"Need exactly three arguments: {Command.start}{cmd.command} <id of channel to send message to> <id of message to reply to> <message>"
    if cmd.num_args >= 3:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_message = ' '.join(cmd.args[2:])
        await target_message.channel.send(host_message, reference=target_message)
    else:
        await cmd.channel.send(help_str)

async def react(cmd: Command):
    help_str=f"Need exactly three arguments: {Command.start}{cmd.command} <id of channel to send message to> <id of message to react to> <message>"
    if cmd.num_args == 3:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_react = cmd.args[2]
        await target_message.add_reaction(host_react)
    else:
        await cmd.channel.send(help_str)