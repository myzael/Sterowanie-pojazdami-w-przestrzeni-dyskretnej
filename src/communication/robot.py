import json
import ast

class Robot:
    def __init__(self):
        self.robots = []
        self.allowedMoves = []

    def setOwnPosition(self, position):
        self.position = position

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json):
        dictionary = ast.literal_eval(json)
        self.robots = [ (x[0], x[1]) for x in dictionary["robots"]]
        self.allowedMoves = [ (x[0], x[1]) for x in dictionary["allowedMoves"]]
        self.position = (tuple(dictionary["position"]))



