import json
import ast

class Robot:
    def __init__(self):
        self.robots = []
        self.allowedMoves = []
        self.destination = []

    def setOwnPosition(self, position):
        self.position = position

    def getOwnPosition(self):
        return self.position

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getSpeed(self):
        return self.speed

    def setSpeed(self, speed):
        self.speed = speed

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, velocity):
        self.velocity = velocity

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json):
        dictionary = ast.literal_eval(json)
        self.robots = [(x[0], x[1]) for x in dictionary["robots"]]
        self.allowedMoves = [((x[0][0], x[0][1]), (x[1][0], x[1][1])) for x in dictionary["allowedMoves"]]
        self.destination = [(x[0], x[1]) for x in dictionary["destination"]]
        self.position = (tuple(dictionary["position"]))
        self.velocity = (tuple(dictionary["velocity"]))
        self.id = dictionary["id"]
        self.speed = dictionary["speed"]



