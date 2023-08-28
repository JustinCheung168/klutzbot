import discord

from klutzbot.general.config import Config
from klutzbot.general.message import Message, MessageResponder


class TTMessageResponder(MessageResponder):
    async def respond(self, msg: Message):
        """Execute any possible responses to messages."""

        # TODO implement blacktea here
