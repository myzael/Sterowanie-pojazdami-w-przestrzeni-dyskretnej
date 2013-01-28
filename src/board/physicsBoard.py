import copy
import operator
from src.board import physics
from src.board.board import ROBOT_ID, Board
from src.board.simplePhysicsBoard import SimplePhysicsBoard, VELOCITY
import cPickle

SPEED = 'speed'

class PhysicsBoard(SimplePhysicsBoard):
    def __init__(self, boardfilename, physicsfilename, maxSpeed, maxPosAcc, maxNegAcc, draw=False ):
        Board.__init__(self, boardfilename, draw)
        try:
            file = open(physicsfilename, 'r')
            self.moves = cPickle.load(file)
        except IOError:
            self.moves = physics.getAllowedMoves(maxSpeed=maxSpeed, maxPosAcc=maxPosAcc, maxNegAcc=maxNegAcc, vis=False)
            file = open(physicsfilename, 'w')
            cPickle.dump(self.moves, file)

    def addRobot(self, position, robotID, initialDirection):
        Board.addRobot(self, position, robotID)
        self.graph.node[position][VELOCITY] = initialDirection
        self.graph.node[position][SPEED] = 0

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

        return filter(lambda tup :not self._positionOccupied(tup[0]),aMoves)

    def translate(self, tup, position):
        return (tuple(map(operator.add, tup[0], position))),tup[1],tup[2]


    def moveRobot(self, sourcePosition, targetPosition, newSpeed, newVelocity):
        if not self._positionOccupied(sourcePosition):
            raise StandardError(
                'Cannot move robot. Position ' + str(sourcePosition) + ' does not contain any robots')
        elif sourcePosition == targetPosition:
            self.graph.node[sourcePosition][SPEED] = 0
        elif not self._canMoveTo(targetPosition) or not self._isGoodVelocity(sourcePosition, targetPosition):
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
    b = PhysicsBoard('test.bmp','physics',4,2,4)
    b.addRobot((0, 1), 1, (0,1))

    print b.getAllowedMoves((0,1))