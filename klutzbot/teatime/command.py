from klutzbot.general.command import (Command, CommandRunner, Interface,
                                      InterfaceSet)


class TTCommand(Command):
    """
    Representation of one command and all its useful properties for teatimebot functionality.
    Most commands only work when Mudae is present.
    """

    START = "$"  # Mudae's command character


class TTCommandRunner(CommandRunner):
    _CMD_CLS = TTCommand

    _DO_PRINT_FAILED_RUN_HELP = False

    # Command implementations.

    async def _help(self, cmd: _CMD_CLS):
        await super()._help(cmd)

    __HELP = Interface(
        _help,
        aliases=["teahelp", "helptea", "help"],
        description="Display help text!",
    )

    async def __print_highscores(self, cmd: _CMD_CLS):
        pass

    __PRINT_HIGHSCORES = Interface(
        __print_highscores,
        aliases=["highscores", "hs"],
        description="Displays high scores for a given game!",
        n_args=1,
        arg_descs=["name of game"],
    )

    async def __print_scrabble_rules(self, cmd: _CMD_CLS):
        pass

    __PRINT_SCRABBLE_RULES = Interface(
        __print_scrabble_rules,
        aliases=["scrabblerules", "scrabble", "sr"],
        description="Displays the point values of each letter in Scrabble!",
    )

    async def _print_aliases(self, cmd: _CMD_CLS):
        await super()._print_aliases(cmd)

    __PRINT_ALIASES = Interface(
        _print_aliases,
        aliases=["cmdalias"],
        description="Prints the aliases of a given command!",
        n_args=1,
        arg_descs=["name of command"],
    )

    # Commands that are supplements to existing Mudae commands.
    async def __blacktea_init(self, cmd: _CMD_CLS):
        pass

    __BLACKTEA_INIT = Interface(
        __blacktea_init,
        aliases=["blacktea"],
        description=f"""Starts the blacktea word game through Mudae! Four alternate modes available:
        `{_CMD_CLS.START}blacktea`
            Starts the vanilla blacktea word game through Mudae!
        `{_CMD_CLS.START}blacktea scrabble`
            Starts the blacktea word game through Mudae, where points are given based on letter values in Scrabble!
        `{_CMD_CLS.START}blacktea long`
            Starts the blacktea word game through Mudae, with extra points for longer words!
        `{_CMD_CLS.START}blacktea custom`
            Starts the blacktea word game through Mudae, with points only being added manually!""",
        n_args=0,
        arg_descs=["scoring mode"],
        more_args_allowed=True,
    )

    async def __award_points(self, cmd: _CMD_CLS):
        pass

    __AWARD_POINTS = Interface(
        __award_points,
        aliases=["awardpoints", "ap"],
        description="Manually award points during a blacktea custom game! **Used as a reply to a player's valid answer.**",
        n_args=1,
        arg_descs=["number of points"],
    )

    async def __exit_game(self, cmd: _CMD_CLS):
        pass

    __EXIT_GAME = Interface(
        __exit_game,
        aliases=["exitgame"],
        description="Exit the ongoing game in this channel.",
    )

    # Any new commands must be declared below and defined above.

    _INTERFACES = InterfaceSet(
        [
            __HELP,
            __PRINT_HIGHSCORES,
            __PRINT_SCRABBLE_RULES,
            __PRINT_ALIASES,
            __BLACKTEA_INIT,
            __AWARD_POINTS,
            __EXIT_GAME,
        ],
        start_char=_CMD_CLS.START,
        help_text_preface=f"""
Hi, I'm klutzbot! 
With commands that start with `{_CMD_CLS.START}`, I supplement Mudae's tea games and add functionalities like Scrabble scoring. 
Here are my commands:""",
    )
