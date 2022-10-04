import os
import discord
from discord.embeds import _EmptyEmbed
from dotenv import load_dotenv


import dataframe_image as dfi
import random

import numpy as np
import pandas as pd

import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#to-do: figure out how to get this automatically
user_to_id_dict = {
    "armadillo":    279870739451084800,
    "beetknee":     376970858859593728,
    "Chaosfnog":    88020501930209280,
    "gazinobot":    978030120734445628,
    "jdub":         178957301485535232,
    "Josh":         178957301485535232,
    "klutz":        657683377725636619,
    "lilabeth":     469706380220170240,
    "firemike":     138336085703917568,
    "mikes fargo":  138336085703917568,
    "Mudae":        432610292342587392,
    "Pinscher":     202600215255973888,
    "HarvZh":       251112534231220225,
    "superharvey":  251112534231220225,
    "teatimebot":   988636031597309983
}
id_to_user_dict = {y: x for x, y in user_to_id_dict.items()}

channel_to_id_dict = {
    "summons-general":          967994638919163906,
    "trades":                   970798258869911562,
    "mikes-workshop":           978287487699005521,
    "harvey-home":              969048327637315584,
    "spam2-electricbogaloo":    975966070231933008,
    "spam2":                    975966070231933008,
    "mudae-games":              969102758647070740,
    "mudae-testing":            988632895545556992,
    "mudae-testing-2":          989063755847573554
}


emoji_to_unicode_dict = {
    "✅":   "\U00002705"
}

medal_emojis = {
    1: "\U0001F947", #🥇
    2: "\U0001F948", #🥈
    3: "\U0001F948", #🥉
}

scrabble_scores_raw = {
    1: ["A","E","I","O","U","L","N","S","T","R"],
    2: ["D","G"],
    3: ["B","C","M","P"],
    4: ["F","H","V","W","Y"],
    5: ["K"],
    8: ["J","X"],
    10: ["Q","Z"]
}
def expand_point_dict(point_dict):
    return {letter.lower():score for score in point_dict.keys() for letter in point_dict[score]}
letter_to_scrabble_score_dict = expand_point_dict(scrabble_scores_raw) #keys are str letters, values are int point values

def display_point_dict(point_dict):
    display_str = ""
    for score in point_dict.keys():

        score_str = "Worth "+str(score)+" "
        if score == 1:
            score_str += "point: "
        else:
            score_str += "points: "
            
        for letter in point_dict[score]:
            score_str += letter+", "
        
        score_str = score_str[:-2] + "\n"
        display_str += score_str
    return display_str




client = discord.Client()

class TeaTimeBot():
    def __init__(self):
        self.gametrackers = {} #dict of dicts; keys are channels ids, second keys are users, values are scores
        self.gametracker_init_requests = {}
        self.hsb = HighscoreBoard()




class GameTracker():
    """
    Tracks a single game in a given channel and keeps track of words used. Tallies points too.
    """
    def __init__(self, channel, activegame, highscoreboard, pointlimit = None):
        self.channel = channel
        self.activegame = activegame
        self.highscoreboard = highscoreboard
        self.pointlimit = pointlimit
        self.round = 0
        self.finalround = None
        self.gameover = False
        self.players = []
        self.unanswered_players = [] #queue of players who have prompts that haven't yet gotten answers
        self.highscorers = set()
        self.prompts = {} #keys are str player ids, values are list of 3-letter prompts that the game has presented.
        self.words = {} #keys are str player ids, values are list of words that player used in this game; each list should be same size as corresponding list in prompts.
        self.word_msgs = {} #keys are str player ids, values are list of message_ids that correspond to the message that the words came from.
        self.points = {} #keys are str player ids, values are list of point values for each word; again, eahc list is same size as prompts and words.
        self.point_totals = {} #keys are str player ids, values are the total points so far (int).
        

    def introduce_player(self, player):
        self.prompts[player] = []
        self.words[player] = []
        self.word_msgs[player] = []
        self.points[player] = []
        self.point_totals[player] = 0
        self.players.append(player)

    def add_prompt(self, player, prompt):

        if player not in self.prompts.keys():
            self.introduce_player(player)
        else:
            self.prompts[player].append(prompt)
        self.unanswered_players.append(player)

        if(player == self.players[0]): #if this is the first player, then a round has passed.
            self.round += 1

        if self.finalround is not None:
            if (self.round == (self.finalround + 1)):
                self.gameover = True

    def fail_answer(self):
        self.give_answer(None, None)

    def give_answer(self, answer, message):

        if message is None:
            player = self.unanswered_players[0]
            self.word_msgs[player].append(None)
        else:
            player = message.author.id
            self.word_msgs[player].append(message.id)

        self.unanswered_players.pop(0)

        self.words[player].append(answer)
        self.points[player].append(0)

        this_answer_points, calculation_str = self.calculate_points(answer)
        add_points_notice_str = self.add_points(player, this_answer_points)

        calculation_str += add_points_notice_str
        calculation_str += "\n"+str(id_to_user_dict[player])+" has "+str(self.point_totals[player])+" points!"

        if self.pointlimit is not None:
            if self.point_totals[player] >= self.pointlimit:
                self.finalround = self.round

        if self.activegame == "blacktea custom":
            return ""
        else:
            return calculation_str

    def calculate_points(self, word):
        if self.activegame == "blacktea":
            if word == None:
                return 0, ""
            else:
                return 1, "" #the word used doesn't matter
        elif self.activegame == "blacktea scrabble":
            if word == None:
                return 0, ""
            else:
                point_breakdown_str = word + " point breakdown: "

                word_score = 0
                for letter in word:
                    
                    letter_score = letter_to_scrabble_score_dict[letter]
                    word_score += letter_score

                    point_breakdown_str += str(letter_score) + "+"
                point_breakdown_str = point_breakdown_str[:-1] #cut off last plus
                point_breakdown_str += "="+str(word_score)

                return word_score, point_breakdown_str
        elif self.activegame == "blacktea long":
            if word == None:
                return 0, ""
            else:
                return len(word), ""
        elif self.activegame == "blacktea custom":
            return 0, ""

    def add_points(self, player, points, msg_id = "END"):
        if msg_id == "END":
            self.points[player][-1] += points
        else:
            word_position = self.word_msgs[player].index(msg_id)
            self.points[player][word_position] += points

        self.point_totals[player] += points

        add_points_notice_str = ""

        if (self.activegame == "blacktea custom") and (msg_id != "END"):
            add_points_notice_str += "Awarded **"+str(points)+" points** to **"+str(id_to_user_dict[player]+"** for "+str(self.words[player][word_position])+"!\n")
            add_points_notice_str += str(id_to_user_dict[player])+" now has "+str(self.point_totals[player])+" points!"

        if (self.point_totals[player] > self.highscoreboard.get_score(self.activegame,player)) and (player not in self.highscorers):
            self.highscorers.add(player)
            add_points_notice_str += "\n⭐ WOW! You've beaten your personal best score, "+str(id_to_user_dict[player])+"! ⭐"

        return add_points_notice_str

    def end_game(self):

        #Display final results

        if len(self.players) != 0:

            final_point_totals = [self.point_totals[player] for player in self.players] #extract points
            final_point_totals = list(set(final_point_totals)) #remove duplicates
            final_point_totals.sort(reverse=True) #sort descending order

            final_results_msg = ":coffee:Final Results::coffee:\n"

            medal_ct = min([len(self.players),3])
            for player in self.players:
                for medal_rank in range(1,medal_ct+1):

                    if self.point_totals[player] == final_point_totals[medal_rank-1]:
                        final_results_msg += medal_emojis[medal_rank]

                final_results_msg += id_to_user_dict[player]+": "+str(self.point_totals[player])
                if player in self.highscorers:
                    final_results_msg += " ⭐ HIGH SCORE! ⭐"
                final_results_msg += "\n"
                
            #Save high score results
            for highscorer in self.highscorers:
                self.highscoreboard.set_score(self.activegame, highscorer, self.point_totals[highscorer])
            
            #Save other results?

            self.gameover = True

            return final_results_msg

        else:

            self.gameover = True

            return "Never mind!"


class CachedObject():
    def __init__(self, cache_path, default_object = None):
        self.cache_path = cache_path
        if os.path.exists(cache_path):
            self.local_object = json.load(open(self.cache_path, 'r'))
        else:
            self.local_object = default_object
    
    def update(self, new_object):
        self.local_object = new_object
        json.dump(self.local_object, open(self.cache_path, 'w'))

class HighscoreBoard(CachedObject):
    """
    Structure of local_object:
    {game:{player:score}}
    """
    def __init__(self, cache_path = "data/hs.json"):
        super().__init__(cache_path, default_object = {})

    def disp(self, game):
        game_hsb = self.local_object[game]
        game_hsb_dict = {id_to_user_dict[int(key)]:[game_hsb[key]] for key in game_hsb.keys()}
        return pd.DataFrame(game_hsb_dict,index=['High Score']).T.sort_values(by='High Score', ascending = False)

    def set_score(self, game, player, new_score):

        player = str(player)

        if game not in self.local_object.keys():
            self.local_object[game] = {}

        if player not in self.local_object[game].keys():
            self.local_object[game][player] = 0

        if new_score > self.local_object[game][player]:
            self.local_object[game][player] = new_score
            json.dump(self.local_object, open(self.cache_path, 'w'))
            return True
        else:
            return False

    def get_score(self, game, player):
        player = str(player)

        if game not in self.local_object.keys():
            self.local_object[game] = {}

        if player not in self.local_object[game].keys():
            self.local_object[game][player] = 0

        return self.local_object[game][player]



    
    
ttb = TeaTimeBot()



async def terminate_gametracker(channel, announce = True):
    final_results_str = ttb.gametrackers[channel.id].end_game()
    if announce and (len(final_results_str) != 0):
        await channel.send(final_results_str)
    ttb.gametrackers.pop(channel.id, None)


@client.event
async def on_ready():
    """
    Runs on bot startup and lets us know which servers the bot successfully connected to.
    """
    print(f'{client.user} is connected to Discord!')
    for guild in client.guilds:
        print(f'Connected to {guild.name} (id: {guild.id})')

@client.event
async def on_message(message):
    """
    Runs every time any message is sent. Handles responses to messages.
    """
    channel = client.get_channel(message.channel.id)
    chid = channel.id

    if message.author == client.user: #Immediately leave if this bot sent the message to prevent responses of bot to itself.
        return


    if len(message.content) > 0:
        if (message.content[0] == "$"): #Process a command
            command_pieces = message.content.split(" ",1)
            command = command_pieces[0]
            command = command.lower()
            if len(command_pieces) > 1:
                arg = command_pieces[1]
                arg = arg.lower()
            else:
                arg = ""

            args = arg.split(" ")

            commander_id = message.author.id

            #Unique teatimebot commands

            if (command == "$helptea") or (command == "$teahelp"):
                """
                This is the primary documentation of this bot.
                """
                await channel.send("""
Hi, my name is teatimebot! I primarily supplement Mudae's tea games
and add functionalities like Scrabble scoring. If you have any questions,
please feel free to ask @klutz!
Here are my commands:
                """)
                await channel.send("""
 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_**GENERAL**_
**$helptea**: Displays this help message!
    Usage: $helptea
    Is the same as: $teahelp
**$guestecho**: Asks me to say hi!
    Usage: $guestecho
    Is the same as: $ge
**$getid**: Gets the user ID of a member of this server!
    Usage: $getid <name of user on this server>
            Don't include an @ sign!
    Is the same as: $gi
                """)
                await channel.send("""
 
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

_**TEA GAMES**_

**$highscores**: Displays high scores for a given game!
    Usage: $highscores <name of game>
    Valid game names: blacktea, blacktea scrabble
    Is the same as: $hs
                """)
                await channel.send("""
 ~~~~~~~~~~~~~~~~~~~~~~~~~

    _**BLACKTEA**_

**$blacktea**: Starts the vanilla blacktea word game through Mudae!
    Usage: $blacktea

**$blacktea scrabble**: Starts the blacktea word game through Mudae, using Scrabble scoring rules!
    Usage: $blacktea scrabble
**$scrabblerules**: Displays the point values of each letter in Scrabble!
    Usage: $scrabblerules
    Is the same as: $scrabblerules, $scrabble, $sr

**$blacktea long**: Starts the blacktea word game through Mudae, with extra points for longer words!
    Usage: $blacktea long

**$blacktea custom**: Starts the blacktea word game through Mudae, with points only being added manually via $awardpoints!
    Usage: $blacktea custom
**$awardpoints**: Manually award points during a blacktea custom game!
    Usage: AS A REPLY TO A PLAYER'S VALID ANSWER: $awardpoints <number of points>
    Is the same as: $ap
                """)


                      


            if (command == "$guestecho") or (command == "$ge"):
                await channel.send(f"Hi {id_to_user_dict[int(commander_id)]}!")

            if (command == '$getid') or (command == '$gi'):
                if arg in user_to_id_dict.keys():
                    await channel.send(str(user_to_id_dict[arg]))
                elif len(arg) == 0:
                    await channel.send("Please write someone's Discord name after $getid! For example:\n$getid klutz")
                else:
                    await channel.send("Can't find that person!")

            if (command == '$highscores') or (command == '$hs'):
                if arg in ttb.hsb.local_object.keys():
                    ri = random.randrange(1000000,2000000)
                    dfi.export(ttb.hsb.disp(arg),f"{ri}.png")
                    await channel.send(file=discord.File(f"{ri}.png"))
                    os.remove(f"{ri}.png")
                elif len(arg) == 0:
                    await channel.send("Please write the name of a Mudae game after $highscores! These are valid:\n$highscores blacktea\n$highscores blacktea scrabble\n$highscores blacktea long\n$highscores blacktea custom")
                else:
                    await channel.send("I don't know that game!")

            if (command == '$scrabblerules') or (command == '$scrabble') or (command == "$sr"):
                await channel.send("These are the point values for each Scrabble letter:\n"+display_point_dict(scrabble_scores_raw))

            #Supplementing existing commands

            if (command == '$blacktea'):
                if args[0] == "scrabble":
                    if len(args) > 1:
                        if args[1].isdigit():
                            pointlimit = args[1]
                        else:
                            pointlimit = None
                    ttb.gametrackers[chid] = GameTracker(channel, "blacktea scrabble", ttb.hsb, pointlimit=pointlimit)
                    await channel.send("I'll be tracking points for "+str(ttb.gametrackers[chid].activegame)+"!\nRemember, your goal is to write words that both fit the prompts and would have high scores in Scrabble!\nIf you would like to review the values of each letter in Scrabble, type: $scrabble")
                    if pointlimit is not None:
                        await channel.send("First to reach **"+str(pointlimit)+"** points wins!")
                elif args[0] == "long":
                    ttb.gametrackers[chid] = GameTracker(channel, "blacktea long", ttb.hsb)
                    await channel.send("I'll be tracking points for "+str(ttb.gametrackers[chid].activegame)+"!\nRemember, your goal is to write the longest possible words that fit the prompts!")
                elif args[0] == "custom":
                    ttb.gametrackers[chid] = GameTracker(channel, "blacktea custom", ttb.hsb)
                    await channel.send("I'm starting a round of "+str(ttb.gametrackers[chid].activegame)+"!\nRemember, add points to players by replying to their Mudae-verified valid answers with: $ap <number of points to award>")
                else:
                    ttb.gametrackers[chid] = GameTracker(channel, "blacktea", ttb.hsb)
                    await channel.send("I'll be tracking points for "+str(ttb.gametrackers[chid].activegame)+"!")
                
                
            if (command == '$exitgame'):
                if chid in ttb.gametrackers.keys():
                    await terminate_gametracker(channel)

            if (command == '$awardpoints') or (command == '$ap'):
                if chid in ttb.gametrackers.keys():
                    if ttb.gametrackers[chid].activegame == "blacktea custom":
                        try:
                            reply_id = message.reference.message_id
                            reply = await channel.fetch_message(reply_id)

                            add_points_str = ttb.gametrackers[chid].add_points(reply.author.id, int(arg), reply_id)
                            await channel.send(add_points_str)
                            
                        except:
                            await channel.send("Couldn't award points; did you remember to reply to the answer message, and use an integer point award?")
                    else:
                        await channel.send("Can't use this command outside a blacktea custom game! ($blacktea custom)")
                else:
                    await channel.send("Can't use this command outside a blacktea custom game! ($blacktea custom)")

            if (command == "$hostecho") and (commander_id == user_to_id_dict["klutz"]):
                await channel.send("Hi host!")

            if (command == "$hostsay") and (commander_id == user_to_id_dict["klutz"]):
                """
                Usage: $hostsay <channel to send message to> <message>
                    OR to send to current channel: $hostsay <message>
                """
                arg_pieces = arg.split(" ",1)
                if len(arg_pieces) > 1:
                    if arg_pieces[0] in channel_to_id_dict.keys():
                        sending_channel = client.get_channel(channel_to_id_dict[arg_pieces[0]])
                    else:
                        sending_channel = channel
                    host_message = arg_pieces[1]
                else:
                    sending_channel = channel
                    host_message = arg_pieces[0]
                await sending_channel.send(host_message)

            if (command == '$teadebug') and (commander_id == user_to_id_dict["klutz"]):
                pass


    if (message.author.id == user_to_id_dict["Mudae"]):

        #Tea Games!

        #blacktea:

        if ((":coffee:" in message.content) and ("Type a word containing: " in message.content)): #given a prompt
            prompt = message.content.split("Type a word containing: ",1)[1].replace("*","").lower()
            ttb.gametrackers[chid].add_prompt(message.mentions[0].id, prompt)

            if ttb.gametrackers[chid].gameover:
                await terminate_gametracker(channel)

        if (":boom: Time's up:" in message.content): #question wrong
            ttb.gametrackers[chid].fail_answer()

        if ((":trophy::trophy::trophy:" in message.content) and ("won the game!" in message.content)):
            await terminate_gametracker(channel)

        if ("No participants..." in message.content):
            await terminate_gametracker(channel, announce = False)

        if (len(message.embeds) > 0):
            embedded = message.embeds[0]
            if not isinstance(embedded.title, _EmptyEmbed):
                if ("The Black Teaword will start!" in embedded.title):
                    print('Game Starting!')



testlist = []

@client.event
async def on_raw_reaction_add(payload):

    #Behavior for blacktea game
    channel = client.get_channel(payload.channel_id)
    chid = channel.id
    if chid in ttb.gametrackers.keys():
        reactor = payload.user_id
        if reactor == user_to_id_dict["Mudae"]:
            react = payload.emoji.name
            if (react == emoji_to_unicode_dict["✅"]):
                message_id = payload.message_id
                message = await channel.fetch_message(message_id)
                valid_word = message.content.lower()
                if (len(valid_word) > 0) and ("$" not in valid_word) and ("/" not in valid_word): #exclude the check mark that mudae provides at start of game, as well as responses to commands
                    calculation_str = ttb.gametrackers[chid].give_answer(valid_word, message)
                    if len(calculation_str)>0:
                        await channel.send(calculation_str)

        



client.run(TOKEN)