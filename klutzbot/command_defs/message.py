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

class Command(Message):
    """
    Representation of one command and all its useful properties
    """
    def __init__(self, message: discord.Message, client: discord.Client):
        super().__init__(message, client)
        message_split = message.content.split(" ")
        self.command = message_split[0].lower()
        if len(message_split) > 0:
            self.args = message_split[1:]
        else:
            self.args = []
        self.num_args = len(self.args)

async def execute_command(message: discord.Message, client: discord.Client):
    """
    Interpret a message as a command.
    Commands are assumed to be formatted as:
        !<command name> <arg1> <arg2> <arg3> ...
    """
    cmd = Command(message, client)
    
    # Interpret specific commands
    if (cmd.command == "!say") and (cmd.author_name == "klutz"):
        await _say(cmd)
    if (cmd.command == "!reply") and (cmd.author_name == "klutz"):
        await _reply(cmd)
    if (cmd.command == "!react") and (cmd.author_name == "klutz"):
        await _react(cmd)
    if (cmd.command == "!amogus"):
        await _amogus(cmd)
    # if (cmd.command == "!joinvoice"): #broken rn, also idk how to leave voice
    #     await _join_voice(cmd)

async def _say(cmd: Command):
    help_str=f"Need exactly two arguments: {cmd.command} <id of channel to send message to> <message>"
    if cmd.num_args >= 2:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        host_message = ' '.join(cmd.args[1:])
        await target_channel.send(host_message)
    else:
        await cmd.channel.send(help_str)

async def _reply(cmd: Command):
    help_str=f"Need exactly three arguments: {cmd.command} <id of channel to send message to> <id of message to reply to> <message>"
    if cmd.num_args >= 3:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_message = ' '.join(cmd.args[2:])
        await target_message.channel.send(host_message, reference=target_message)
    else:
        await cmd.channel.send(help_str)

async def _react(cmd: Command):
    help_str=f"Need exactly three arguments: {cmd.command} <id of channel to send message to> <id of message to react to> <message>"
    if cmd.num_args == 3:
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_react = cmd.args[2]
        await target_message.add_reaction(host_react)
    else:
        await cmd.channel.send(help_str)

async def _amogus(cmd: Command):
    await cmd.channel.send("ඞ")
    # await cmd.channel.send("https://tenor.com/view/boiled-soundcloud-boiled-boiled-irl-boiled-utsc-boiled-cheesestick-agem-soundcloud-gif-20049996")

# async def _join_voice(cmd: Command):
#     help_str=f"Need the command issuer ({cmd.author_name}) to be connected to the voice channel of interest."
#     if cmd.author.voice:
#         await cmd.author.voice.channel.connect()
#     else:
#         await cmd.channel.send(help_str)
