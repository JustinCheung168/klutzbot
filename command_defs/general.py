import teatime

class Translator():
    def __init__(self, client):
        #Build user and id relationship dicts
        self.user_to_id_dict = {}
        self.id_to_user_dict = {}
        for guild in client.guilds:
            for user in guild.members:
                self.user_to_id_dict[user.name] = user.id
                self.id_to_user_dict[user.id] = user.name
        #Some bots do not appear for whatever reason, so need to add them manually...
        self.user_to_id_dict["Slackbot"] = 204255221017214977

        #Build channel and id relationship dict
        #ASSUMES NONE OF THE ACTIVE GUILDS SHARE CHANNEL NAMES.
        self.channel_to_id_dict = {}
        self.channel_id_list = []
        for guild in client.guilds:
            for channel in guild.channels:
                self.channel_to_id_dict[channel.name]=channel.id
                self.channel_id_list.append(channel.id)

    def un2id(self, username):
        return self.user_to_id_dict[username]

    def id2un(self, userid):
        return self.id_to_user_dict[userid]

    def ch2id(self, channelname):
        return self.channel_to_id_dict[channelname]



async def run_command(message, channel, client, rk):
    command_pieces = message.content.split(" ",1)
    command_raw = command_pieces[0]
    command = command_raw.lower()
    if len(command_pieces) > 1:
        arg_raw = command_pieces[1]
        arg = arg_raw.lower()
    else:
        arg = ""

    args = arg.split(" ")

    commander_id = message.author.id

    #Unique teatimebot commands

    if (command == "$klutzhelp"):
        """
        This is the primary documentation of this bot.
        """
        pass

    if (command == '$amogus'):
        await channel.send("https://tenor.com/view/boiled-soundcloud-boiled-boiled-irl-boiled-utsc-boiled-cheesestick-agem-soundcloud-gif-20049996")

    if (command == "$klutzsay") and (commander_id == rk.user_to_id_dict["klutz"]):
        """
        Usage: $klutzsay <channel to send message to> <message>
            OR to send to current channel: $klutzsay <message>
        """
        arg_pieces = arg_raw.split(" ",1)
        if len(arg_pieces) > 1:
            if arg_pieces[0] in rk.channel_to_id_dict.keys():
                sending_channel = client.get_channel(rk.channel_to_id_dict[arg_pieces[0]])
            elif int(arg_pieces[0]) in rk.channel_id_list:
                sending_channel = client.get_channel(int(arg_pieces[0]))
            else:
                sending_channel = channel
            host_message = arg_pieces[1]
        else:
            sending_channel = channel
            host_message = arg_pieces[0]
        await sending_channel.send(host_message)