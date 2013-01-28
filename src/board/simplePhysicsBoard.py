from board import Board
from board import ROBOT_ID
import operator
import networkx as nx
VELOCITY = 'velocity'

class SimplePhysicsBoard(Board):

    def addRobot(self, position, robotID):
            Board.addRobot(self, position, robotID)
            self.graph.node[position][VELOCITY] = (0, 0)

    def moveRobot(self, sourcePosition, targetPosition, newSpeed, newVelocity): #TODO handle speed and velocity
        if not self._positionOccupied(sourcePosition):
            raise StandardError('Cannot move robot. Position ' + str(sourcePosition) + ' does not contain any robots')
        elif sourcePosition == targetPosition:
            self.graph.node[sourcePosition][VELOCITY] = (0, 0)
        elif not self._canMoveTo(targetPosition) or not self._isGoodVelocity(sourcePosition, targetPosition):
            raise StandardError('Cannot move robot. Move from ' + str(sourcePosition) + ' to ' + str(targetPosition) + ' is illegal')
        else:
            self.history.append((sourcePosition, targetPosition))
            self.graph.node[targetPosition][ROBOT_ID] = self.graph.node[sourcePosition].pop(ROBOT_ID)

            # set new velocity
            del self.graph.node[sourcePosition][VELOCITY]
            self.graph.node[targetPosition][VELOCITY] = tuple(map(operator.sub, targetPosition, sourcePosition))

#    def draw(self):
#        nc = map(self.createNodesColors, self.graph.nodes())
#        nx.draw_networkx_nodes(self.graph, self.nodePositions, node_size=200, node_color=nc,animated=True)
#
#        l = []
#        for r in self.getRobots():
#            vel =self.graph.node[r][VELOCITY]
#            if vel != (0,0):
#                velPos = tuple(map(operator.add, vel, r))
#                l.append((r, velPos))
#                # fucking networkx ordering!
#                l.append((velPos, r))
#
#        ec = map((lambda x: x in l and 'y' or'k'), self.graph.edges())
#
#        nx.draw_networkx_edges(self.graph, self.nodePositions, edge_color=ec, width=5, animated=True)
#        nx.draw_networkx_labels(self.graph, self.nodePositions, labels=self.getRobots(), font_color='w', animated=True)

    def createNodesColors(self, tup):
        if tup in self.getRobots().keys():
            return 'r'
        else:
            return 'w'

    def createEdgesColors(self, tup):
        if tup in list:
            return 'g'
        else:
            return 'k'


    def getFreeNeighbors(self,position):
        return filter(lambda p :not self._positionOccupied(p), self.graph.neighbors(position))

    def getAllowedMoves(self, position):
        # emptyAvaliablePlaces
        eAP = [position] + filter(self._canMoveTo, self.graph.neighbors(position))
        places_with_good_velocity = filter(lambda c: self._isGoodVelocity(position, c), eAP)
        #TODO: should return proper velocities, speed is not required here as agent should know that speed can change only by one
        return [(node, (1,1)) for node in places_with_good_velocity]

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
    b1 = SimplePhysicsBoard('test.bmp')
    b1.addRobot((0, 0), 1)
    b1.addRobot((0, 1), 2)
    b1.refreshBoard();

    b1.moveRobot((0, 1), (0, 2));
    b1.refreshBoard();

    b1.moveRobot((0, 2), (0, 3));
    b1.refreshBoard();

    b1.moveRobot((0, 3), (0, 4));
    b1.refreshBoard();

    b1.moveRobot((0, 4), (0, 5));
    b1.refreshBoard();

    b1.moveRobot((0, 5), (1, 6));
    b1.refreshBoard();

    b1.moveRobot((1, 6), (2, 7));
    b1.refreshBoard();
    
    b1.moveRobot((2, 7), (2, 8));
    b1.refreshBoard();