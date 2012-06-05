from board import Board
from board import ROBOT_ID
import operator
VELOCITY = 'velocity'

class SimplePhysicsBoard(Board):

    def addRobot(self, position, robotID):
            Board.addRobot(self, position, robotID)
            self.graph.node[position][VELOCITY] = (0, 0)

    def moveRobot(self, sourcePosition, targetPosition):
        if not self._positionOccupied(sourcePosition):
            raise StandardError('Cannot move robot. Position ' + str(sourcePosition) + ' does not contain any robots')
        elif sourcePosition == targetPosition:
            self.graph.node[sourcePosition][VELOCITY] = (0,0)
        elif not self._canMoveTo(targetPosition) or not self._isGoodVelocity(sourcePosition, targetPosition):
            raise StandardError('Cannot move robot. Move from ' + str(sourcePosition) + ' to ' + str(targetPosition) + ' is illegal')
        else:
            self.history.append((sourcePosition, targetPosition))
            self.graph.node[targetPosition][ROBOT_ID] = self.graph.node[sourcePosition].pop(ROBOT_ID)
            del self.graph.node[sourcePosition][VELOCITY]
            self.graph.node[targetPosition][VELOCITY] = tuple(map(operator.sub, targetPosition, sourcePosition))

    def getAllowedMoves(self, position):
        # emptyAvaliablePlaces
        eAP = [position] + filter(self._canMoveTo, self.graph.neighbors(position))
        return filter(lambda c : self._isGoodVelocity(position, c), eAP)

    def _isGoodVelocity(self, source, target):
        velocity = self.graph.node[source].get(VELOCITY, None)
        if velocity == None:
            return False
        elif velocity == (0, 0) or source == target:
            return True
        else:
            wantedV = tuple(map(operator.sub, target, source))
            c = tuple(map(operator.sub, velocity, wantedV))
            return abs(c[0]) + abs(c[1]) <= 1

if __name__ == "__main__":
    b1 = SimplePhysicsBoard('test.bmp', False)
    b1.addRobot((0, 0), 1)
    b1.addRobot((0, 1), 2)
    print b1.getAllowedMoves((0, 0))
    print b1.getRobots()
    b1.refreshBoard();

    b1.moveRobot((0, 1), (0, 2));
    print b1.getAllowedMoves((0, 2))
    b1.refreshBoard();

    b1.moveRobot((0, 2), (0, 3));
    print b1.getAllowedMoves((0, 3))
    b1.refreshBoard();
    
    b1.moveRobot((0, 3), (0, 4));
    print b1.getAllowedMoves((0, 4))
    b1.refreshBoard();
    
    b1.moveRobot((0, 4), (0, 4));
    print b1.getAllowedMoves((0, 4))
    b1.refreshBoard();
    
    b1.moveRobot((0, 4), (0, 3));
    print b1.getAllowedMoves((0, 3))
    b1.refreshBoard();

#if __name__ == "__main__":
#    a = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
#    for t in a:
#        print t
#        print '\n'
#        for org in a:
#            r = tuple(map(operator.sub, t, org))
#            if abs(r[0]) + abs(r[1]) <= 1:
#                print org
#            
#        print "############"

