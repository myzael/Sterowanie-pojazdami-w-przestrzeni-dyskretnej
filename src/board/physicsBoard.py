import copy
import operator
from src.board import physics
from src.board.board import ROBOT_ID, Board
from src.board.physicsReader import readPhysics
from src.board.simplePhysicsBoard import SimplePhysicsBoard, VELOCITY
import cPickle

SPEED = 'speed'

class PhysicsBoard(SimplePhysicsBoard):
    def __init__(self, boardfilename, physicsfilename, draw=False, maxSpeed=None, maxPosAcc=None, maxNegAcc=None):
        Board.__init__(self, boardfilename, draw)
        if maxSpeed==None and maxPosAcc==None and maxNegAcc==None:
            self.moves = readPhysics(physicsfilename)
        else:
            try:
                file = open(physicsfilename, 'r')
                self.moves = cPickle.load(file)
            except IOError:
                self.moves = physics.getAllowedMoves(maxSpeed=maxSpeed, maxPosAcc=maxPosAcc, maxNegAcc=maxNegAcc, vis=False)
                file = open(physicsfilename, 'w')
                cPickle.dump(self.moves, file)

    def addRobot(self, position, robotID, initialDirection, initialSpeed = 0):
        Board.addRobot(self, position, robotID)
        self.graph.node[position][VELOCITY] = initialDirection
        self.graph.node[position][SPEED] = initialSpeed

    def getAllowedMoves(self, position):
        """
        returns list of tuples of (endP,endV,listOfTakenFields) that represent allowed moves
        e.g.   [(
                (4,6), #end point
                (2,(1,-1)), #end velocity (speed, (xDirection, yDirection))
                [(4,6), (4,5), (5,4)] #list of points that would be taken while making this move
               ),...]
        list of taken fields is given in no particular order
        """

        key = (self.graph.node[position][SPEED], self.graph.node[position][VELOCITY])
        aMoves = copy.copy(self.moves[key])
        aMoves = map(lambda tup: self.translate(tup,position), aMoves)

        aMoves = filter(lambda tup: self._positionExists(tup[0]), aMoves)
        aMoves = filter(lambda tup: not self._positionOccupied(tup[0]), aMoves)

        l=[]
        for move in aMoves:
            if move[2] not in l:
                l.append(move[2])
        print l

        return aMoves

    def getAvaliableStates(self, state):

        key = state[2],state[1]
        aMoves = copy.copy(self.moves[key])
        aMoves = map(lambda tup: self.translate(tup,state[0]), aMoves)

        aMoves = filter(lambda tup: self._positionExists(tup[0]), aMoves)

        return aMoves

    def translate(self, tup, position):
        return (tuple(map(operator.add, tup[0], position))),tup[1],tup[2]


    def moveRobot(self, sourcePosition, targetPosition, newSpeed, newVelocity):
        if not self._positionOccupied(sourcePosition):
            raise StandardError(
                'Cannot move robot. Position ' + str(sourcePosition) + ' does not contain any robots')
        elif sourcePosition == targetPosition:
            self.graph.node[sourcePosition][SPEED] = 0
        elif not self._canMoveTo(targetPosition): # or not self._isGoodVelocity(sourcePosition, targetPosition):
            raise StandardError('Cannot move robot. Move from ' + str(sourcePosition) + ' to ' + str(
                targetPosition) + ' is illegal')
        else:
            self.history.append((sourcePosition, targetPosition))
            self.graph.node[targetPosition][ROBOT_ID] = self.graph.node[sourcePosition].pop(ROBOT_ID)

            del self.graph.node[sourcePosition][VELOCITY]
            self.graph.node[targetPosition][VELOCITY] = newVelocity

            del self.graph.node[sourcePosition][SPEED]
            self.graph.node[targetPosition][SPEED] = newSpeed

if __name__ == "__main__":
    b = PhysicsBoard('test.bmp','physics',4,3,4)
    b.addRobot((0, 0), 1, (0,1))
    b.addRobot((0, 1), 2, (0,1))

    print '#############################'
    for move in b.getAllowedMoves((0,0)):
        print move

    print '#############################'

    for move in b.getAllowedMoves((0,1)):
        print move

    print '#############################'

#    states = [((0, 0), (0, 1), 0),((0, 0), (0, 1), 2),((0, 0), (0, 1), 3),((0, 0), (0, 1), 4)]
    states = [((0, 0), (0, 1), 4)]
    for state in states:
        print state
        print '###########'
        for i in b.getAvaliableStates(state):
            print i
        print '#############################'


