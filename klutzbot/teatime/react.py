import discord

from klutzbot.general.config import Config
from klutzbot.general.react import React, ReactResponder


class TTReactResponder(ReactResponder):
    async def respond(self, rct: React):
        """Execute any possible responses to reacts."""

        # TODO implement blacktea here
