import operator
from src.board import physics
from src.board.board import ROBOT_ID, Board
from src.board.simplePhysicsBoard import SimplePhysicsBoard, VELOCITY
import cPickle

SPEED = 'speed'

filename = 'physics'

class PhysicsBoard(SimplePhysicsBoard):
    def __init__(self, maxSpeed, maxNegAcc, maxPosAcc):
        try:
            file = open(filename, 'r')
            self.moves = cPickle.load(file)
        except IOError:
            self.moves = physics.getAllowedMoves(maxSpeed=maxSpeed, maxPosAcc=maxPosAcc, maxNegAcc=maxNegAcc, vis=False)
            cPickle.dump(self.moves)

    def addRobot(self, position, robotID, initialDirection):
        Board.addRobot(self, position, robotID)
        self.graph.node[position][VELOCITY] = initialDirection
        self.graph.node[position][SPEED] = 0

    def getAllowedMoves(self, position):
        """
        returns list of tuples of (endP,endV,listOfTakenFields) that represent allowed moves
        e.g.   (
                (4,6), #end point
                (2,(1,-1)), #end velocity (speed, (xDirection, yDirection))
                [(4,6), (4,5), (5,4)] #list of points that would be taken while making this move
               )
        list of taken fields is given in no particular order
        """
        self.moves[self.graph]
        eAP = [position] + filter(self._canMoveTo, self.graph.neighbors(position))


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
