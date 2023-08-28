from typing import Callable

import discord

import klutzbot.general.message
from klutzbot.general.config import Config
from klutzbot.general.guild import AllGuildInfos


class Interface:
    """Struct collecting details of interface and implementation."""

    def __init__(
        self,
        implementation: Callable[[], None],
        aliases: list[str],
        description: str = "No description available",
        n_args: int = 0,
        arg_descs: list[str] | None = None,
        more_args_allowed: bool = False,
        authorized_users_wl: set[str] | None = None,
        hide_help: bool = False,
    ):
        self.implementation = implementation
        # The first alias in the list is considered the primary one.
        # Stylistically, this should be a good balance between being descriptive and being fairly short.
        # Abbreviations should not be first, for example.
        assert len(aliases) > 0
        self.aliases = aliases
        if arg_descs is None:
            self.arg_descs = []
        else:
            self.arg_descs = arg_descs
        self.n_args = n_args
        self.more_args_allowed = more_args_allowed
        self.description = description
        # The whitelist of authorized users for each command can be specified here.
        # Leave as None if anyone can use the command.
        self.authorized_users_wl = authorized_users_wl
        # Hide the help text from the aggregate of help texts. Help text will still show if user has permission to use the command and the command is misused.
        self.hide_help = hide_help

        # Check that the implementer provided descriptions for each argument.
        if self.more_args_allowed:
            assert len(self.arg_descs) >= self.n_args
        else:
            assert len(self.arg_descs) == self.n_args

        # Construct the usage & error texts. They need to be formatted with the actual command alias used.
        if self.more_args_allowed:
            n_args_str = f"{self.n_args} or more"
        else:
            n_args_str = f"exactly {self.n_args}"
        if self.n_args == 1:
            s = ""
        else:
            s = "s"
        error_text = f"Need {n_args_str} argument{s}. Example usage:\n"
        usage_text = "{}"  # This needs to be formatted
        for arg_desc in self.arg_descs:
            usage_text += f" <{arg_desc}>"
        error_text += f"`{usage_text}`"
        self.usage_text = usage_text
        self.error_text = error_text


class InterfaceSet:
    def __init__(
        self,
        interfaces: list[Interface],
        start_char: str,
        help_text_preface: str = "Available commands:",
    ):
        self.interfaces = interfaces
        self.start_char = start_char

        help_text = help_text_preface + "\n\n"
        alias_list: list[str] = []
        alias_interface_map: dict[str, Interface] = {}
        for interface in self.interfaces:
            # Construct the all-help-text.
            if not interface.hide_help:
                command_name = interface.aliases[0]
                help_text += f"**{interface.usage_text.format(self.start_char + command_name)}**: {interface.description}\n"
                if len(interface.aliases) > 1:
                    aliases_str = (
                        "`"
                        + start_char
                        + f"`, `{start_char}".join(interface.aliases[1:])
                        + "`"
                    )
                    help_text += f"    Aliases: {aliases_str}\n"
            # Construct a map from command alias to interfaces.
            for alias in interface.aliases:
                if alias not in alias_list:
                    alias_list.append(alias)
                    alias_interface_map[alias] = interface
                else:
                    raise Exception(
                        f"The command name {alias} can only be defined once; it has been defined more than once"
                    )

        self.alias_list = alias_list
        self.alias_interface_map = alias_interface_map
        self.help_text = help_text


class Command(klutzbot.general.message.Message):
    """
    Abstract representation of one command and all its useful properties
    """

    START = "!"
    DELIM = " "

    def __init__(
        self,
        message: discord.Message,
        client: discord.Client,
        guild_infos: AllGuildInfos,
    ):
        super().__init__(message, client, guild_infos)
        # Strip out the start command indicator
        message_split = message.content[len(self.START) :].split(self.DELIM)
        self.command = message_split[0].lower()
        if len(message_split) > 0:
            self.args = message_split[1:]
        else:
            self.args = []
        self.num_args = len(self.args)


class GeneralCommand(Command):
    START = "!"


class CommandRunner:
    _CMD_CLS = Command

    # Must overwrite this
    _INTERFACES: InterfaceSet = None

    _DO_PRINT_FAILED_RUN_HELP = False

    async def run(self, cmd: _CMD_CLS):
        """Attempt to run a command."""
        # Check if the command is a valid command.
        _command_exists = True
        _author_has_permission = True
        if cmd.command in self._INTERFACES.alias_list:
            _command_exists = True
            # Check the author's permission to run the command.
            interface = self._INTERFACES.alias_interface_map[cmd.command]
            if (
                interface.authorized_users_wl is None
                or cmd.author_name in interface.authorized_users_wl
            ):
                _author_has_permission = True
                # Check if a valid number of arguments has been passed in.
                if not interface.more_args_allowed:
                    arg_count_valid = cmd.num_args == interface.n_args
                else:
                    arg_count_valid = cmd.num_args >= interface.n_args
                if arg_count_valid:
                    # Execute the command.
                    await interface.implementation(self, cmd)
                else:
                    # Send help text since the wrong number of arguments was used.
                    await cmd.channel.send(
                        interface.error_text.format(cmd.START + cmd.command)
                    )
            else:
                _author_has_permission = False
        else:
            _command_exists = False
        if self._DO_PRINT_FAILED_RUN_HELP:
            await self.__print_failed_run_help(
                cmd, _author_has_permission, _command_exists
            )

    async def __print_failed_run_help(
        self, cmd: _CMD_CLS, _author_has_permission, _command_exists
    ):
        if not _author_has_permission:
            await cmd.channel.send(
                f"User {cmd.author_name} lacks permission to use command: {cmd.START}{cmd.command}"
            )
        if not _command_exists:
            await cmd.channel.send(f"Invalid command: {cmd.START}{cmd.command}")

    # Command implementations that should be available in multiple contexts.

    async def _help(self, cmd: _CMD_CLS):
        await cmd.channel.send(self._INTERFACES.help_text)

    async def _print_aliases(self, cmd: _CMD_CLS):
        target_command = cmd.args[0]
        if target_command in self._INTERFACES.alias_list:
            interface = self._INTERFACES.alias_interface_map[target_command]
            aliases = interface.aliases.copy()
            aliases.remove(target_command)
            if len(aliases) == 0:
                await cmd.channel.send(f"No aliases exist for {target_command}.")
            else:
                aliases_str = "`" + cmd.START + f"`, `{cmd.START}".join(aliases) + "`"
                await cmd.channel.send(f"Aliases for {target_command}: {aliases_str}")
        else:
            await cmd.channel.send(
                f"{cmd.command} is not a valid command, so no aliases for it were found."
            )


class GeneralCommandRunner(CommandRunner):
    _CMD_CLS = GeneralCommand

    _DO_PRINT_FAILED_RUN_HELP = True

    # Command implementations & interfaces.

    async def _help(self, cmd: _CMD_CLS):
        await super()._help(cmd)

    __HELP = Interface(
        _help,
        aliases=["help"],
        description="Display help text.",
    )

    async def __guestecho(self, cmd: _CMD_CLS):
        await cmd.channel.send(f"Hi {cmd.author_name}!")

    __GUESTECHO = Interface(
        __guestecho,
        aliases=["guestecho", "ge"],
        description="Asks me to say hi!",
    )

    async def __get_id(self, cmd: _CMD_CLS):
        pass

    __GET_ID = Interface(
        __get_id,
        aliases=["getid", "gi"],
        description="Gets the user ID of a member of this server! (do not include the @ sign)",
        n_args=1,
        arg_descs=["name of user on this server"],
    )

    async def _print_aliases(self, cmd: _CMD_CLS):
        await super()._print_aliases(cmd)

    __PRINT_ALIASES = Interface(
        _print_aliases,
        aliases=["cmdalias", "alias"],
        description="Prints the aliases of a given command!",
        n_args=1,
        arg_descs=["name of command"],
    )

    async def __say(self, cmd: _CMD_CLS):
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        host_message = " ".join(cmd.args[1:])
        await target_channel.send(host_message)

    __SAY = Interface(
        __say,
        aliases=["say"],
        description="Admin method to cause bot to send a message.",
        n_args=2,
        arg_descs=["id of channel to send message to", "message"],
        more_args_allowed=True,
        authorized_users_wl=Config.ADMINS,
        hide_help=True,
    )

    async def __reply(self, cmd: _CMD_CLS):
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_message = " ".join(cmd.args[2:])
        await target_message.channel.send(host_message, reference=target_message)

    __REPLY = Interface(
        __reply,
        aliases=["reply"],
        description="Admin method to cause bot to reply to a message.",
        n_args=3,
        arg_descs=[
            "id of channel to send message to",
            "id of message to reply to",
            "message",
        ],
        more_args_allowed=True,
        authorized_users_wl=Config.ADMINS,
    )

    async def __react(self, cmd: _CMD_CLS):
        target_channel = cmd.client.get_channel(int(cmd.args[0]))
        target_message = await target_channel.fetch_message(int(cmd.args[1]))
        host_react = cmd.args[2]
        await target_message.add_reaction(host_react)

    __REACT = Interface(
        __react,
        aliases=["react"],
        description="Admin method to cause bot to react to a message.",
        n_args=3,
        arg_descs=[
            "id of channel to send message to",
            "id of message to react to",
            "message",
        ],
        more_args_allowed=False,
        authorized_users_wl=Config.ADMINS,
        hide_help=True,
    )

    async def __debug(self, cmd: _CMD_CLS):
        await cmd.channel.send("No debug behavior defined")

    __DEBUG = Interface(
        __debug,
        aliases=["debug"],
        description="Dev debug method that can be called from Discord interface.",
        authorized_users_wl=Config.DEVS,
        hide_help=True,
    )

    # Any new commands must be declared below and defined above.
    _INTERFACES = InterfaceSet(
        [
            __HELP,
            __GUESTECHO,
            __GET_ID,
            __PRINT_ALIASES,
            __SAY,
            __REPLY,
            __REACT,
            __DEBUG,
        ],
        start_char=_CMD_CLS.START,
        help_text_preface=f"""
Hi, I'm klutzbot! 
Here are my commands:""",
    )
