"""Global config variables."""


class Config:
    # The highest level users.
    ADMINS = {"klutzeh"}
    DEVS = {"klutzeh"}

    # Users who subscribe to dumb bot antics
    NO_VALUE_USERS = {"klutzeh", "firemike"}

    # Users to bully
    BULLY_VICTIMS = {"YAGPDB.xyz"}


class NoValueConfig:
    # Manually curated.
    KEYWORD_MAP = {
        "diamond": "💎🙌",
        "ass": "🍑",
        "booty": "🍑",
        "christmas": "🎄",
        "birthday": "🎉",
        "zibu": "❤️",
    }

    # These words will never trigger an automatic reaction with custom server-specific emoji reacts.
    CUSTOM_BLACKLIST = [
        "lmao",
    ]
