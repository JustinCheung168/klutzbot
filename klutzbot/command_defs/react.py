import discord

class React():
    """
    Representation of one react and all its useful properties
    """
    def __init__(self, payload: discord.RawReactionActionEvent, client: discord.Client):
        self.client = client
        self.channel_id = payload.channel_id
        self.channel = client.get_channel(self.channel_id)
        self.reactor_id = payload.user_id
        self.reactor = payload.member
        self.reactor_name = self.reactor.name
        self.react = payload.emoji.name
        self.message_id  = payload.message_id

    @property
    async def message(self) -> discord.Message:
        return await self.channel.fetch_message(self.message_id)

async def respond_to_react(payload: discord.RawReactionActionEvent, client: discord.Client):
    """
    Take any needed actions in response to a react.
    """
    reac = React(payload, client)

    # if reac.reactor_name == "klutz":
    #     await mirror_react(reac)
        
# async def mirror_react(reac: React):
#     target_message = await reac.message
#     await target_message.add_reaction(reac.react)




