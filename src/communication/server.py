import json
import ast

class State:
    def __init__(self):
        self.agents = []
        self.allowedMoves = []

    def __init__(self, json):
        self.from_json(json)

    def setOwnPosition(self, position):
        self.position = position

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json):
        dictionary = ast.literal_eval(json)
        self.agents = [ (x[0], x[1]) for x in dictionary["agents"]]
        self.allowedMoves = [ (x[0], x[1]) for x in dictionary["allowedMoves"]]
        self.position = (tuple(dictionary["position"]))

