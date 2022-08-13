#In-progress: porting blacktea compatibility to this bot

class TeaTimeConstants():
    def __init__(self):
        self.emoji_to_unicode_dict = {
            "✅":   "\U00002705"
        }

        self.medal_emojis = {
            1: "\U0001F947", #🥇
            2: "\U0001F948", #🥈
            3: "\U0001F948", #🥉
        }

        self.scrabble_scores_raw = {
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
        self.letter_to_scrabble_score_dict = expand_point_dict(self.scrabble_scores_raw) #keys are str letters, values are int point values


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


class TeaTimeBot():
    def __init__(self):
        self.gametrackers = {} #dict; keys are channel ids, values are GameTracker instances
        self.gameintromsgs = {} #dict; keys are channel ids, values are Discord message objects
        self.hsb = HighscoreBoard()





        


