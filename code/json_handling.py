import json

class JsonHandling:
    def __init__(self, playername = ""):
       with open('player_info.json', 'r') as openfile: self.player_info_object = json.load(openfile)
       self.add_player_if_unique(playername)

    def add_player_if_unique(self, playername):
        unique = True
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i]["username"] == playername:
                unique = False
        if unique:
            self.player_info_object["players"].append({"username": playername, "gambling": "False", "even": "False"})
            json_object = json.dumps(self.player_info_object, indent=2) 
            with open("player_info.json", "w") as outfile: outfile.write(json_object)
        pass

    def calc_index(self, playername):
        for i in range(len(self.player_info_object["players"])):
            if self.player_info_object["players"][i] == playername: 
                return i
        else: return 0

    def gambling(self, playername):
        index = self.calc_index(playername)
        return self.player_info_object["players"][index]["gambling"] == "True"

    def iseven(self, playername):
        index = self.calc_index(playername)
        return self.player_info_object["players"][index]["even"] == "True"

    def update_json(self, playername, gambling = None, even = None):
        index = self.calc_index(playername)
        if (gambling != None):
            self.player_info_object["players"][index]["gambling"] = str(gambling)
        if (even != None):
            self.player_info_object["players"][index]["even"] = str(even)
        json_object = json.dumps(self.player_info_object, indent=2)
        with open("player_info.json", "w") as outfile: outfile.write(json_object)