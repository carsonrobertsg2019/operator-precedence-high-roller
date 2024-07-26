import json

class JsonHandling:
    def __init__(self):
       with open('gambling_info.json', 'r') as openfile: self.gambling_info_object = json.load(openfile)

    def gambling(self):
        return self.gambling_info_object["gambling"] == "True"

    def iseven(self):
        return self.gambling_info_object["even"] == "True"

    def update_json(self, gambling = None, even = None):
        if (gambling != None):
            self.gambling_info_object["gambling"] = str(gambling)
        if (even != None):
            self.gambling_info_object["even"] = str(even)
        json_object = json.dumps(self.gambling_info_object, indent=2)
        with open("gambling_info.json", "w") as outfile: outfile.write(json_object)