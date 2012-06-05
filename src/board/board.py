from PIL import Image
import networkx as nx
from networkx.classes.function import get_node_attributes
import matplotlib.pyplot as plt
import cPickle

ROBOT_ID = 'robotID'

class Board(object):
    '''Represents a board that models a part of reality. 
    If there is a conneciton between nodes, and the target node is empty, the move is allowed.'''
    i = 1

    def __init__(self, filename, draw=True):
        self._read(filename)
        self.history = []
        if draw:
            self.draw()
            plt.interactive(True)
            plt.hold(False)
            plt.show()

    def addRobot(self, position, robotID):
        if not self._positionExists(position):
            raise StandardError('Cannot add robot. Position ' + str(position) + ' does not exist')
        elif  self._positionOccupied(position) :
            raise StandardError('Cannot add robot! Position ' + str(position) + ' already occupied')
        elif self._containsRobot(robotID):
            raise StandardError('Cannot add robot. Robot of id ' + str(robotID) + ' is already on the board')
        else:
            self.graph.node[position][ROBOT_ID] = robotID

    def getRobots(self):
        '''Returns a dict where keys are positions and values robotID of robots on the board'''
        return get_node_attributes(self.graph, ROBOT_ID)

    def moveRobot(self, sourcePosition, targetPosition):
        if not self._positionOccupied(sourcePosition):
            raise StandardError('Cannot move robot. Position ' + str(sourcePosition) + ' does not contain any robots')
        elif sourcePosition == targetPosition:
            pass
        elif not self._canMoveTo(targetPosition):
            raise StandardError('Cannot move robot. Move from ' + str(sourcePosition) + ' to ' + str(targetPosition) + ' is illegal')
        else:
            self.history.append((sourcePosition, targetPosition))
            self.graph.node[targetPosition][ROBOT_ID] = self.graph.node[sourcePosition].pop(ROBOT_ID)


    def getAllowedMoves(self, position):
        '''Does NOT require a robot tom be in the specified position'''
        return [position] + filter(self._canMoveTo, self.graph.neighbors(position))
    def draw(self):
        nx.draw_networkx(self.graph, self.nodePositions, labels=self.getRobots(), node_size=150, node_color='g', font_color='w', animated=True)
#        nx.draw_networkx_nodes(b1.graph, b1.nodePositions, node_size=50)
    def refreshBoard(self):
        self.draw()
        plt.draw()
        pass

    def dumpHistory(self, filename):
        print len(self.history)
        cPickle.dump(self.history, open(filename, 'w+'))

    # Helper methods    
    def _canMoveTo(self, position):
        return self._positionExists(position) and not self._positionOccupied(position)
    def _positionExists(self, position):
        return position in self.graph.nodes()
    def _positionOccupied(self, position):
        ret = ROBOT_ID in self.graph.node[position]
        return ret
    def _containsRobot(self, robotID):
        return robotID in get_node_attributes(self.graph, ROBOT_ID).values()
    def _read(self, filename, resolution=1):
        '''
        Reads the image from given path pointing to a B&W bmp file.
        Uses the following assumptions:
        * only full B$W is supported #FFFFFF and #000000
        '''
        im = Image.open(filename)
        im = im.rotate(270)
        size = im.size
        a = im.load()

        # create a full grid graph
        self.graph = nx.grid_2d_graph(size[1], size[0])

        # fill the diagonal vertices
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                if i > 0 and j > 0:
                    self.graph.add_edge((i, j), (i - 1, j - 1))
                if i < size[0] - 1 and j > 0:
                    self.graph.add_edge((i, j), (i + 1, j - 1))
                if i > 0 and j < size[1] - 1:
                    self.graph.add_edge((i, j), (i - 1, j + 1))
                if i < size[0] - 1 and j < size[1] - 1:
                    self.graph.add_edge((i, j), (i + 1, j + 1))

        # remove unnecessary nodes
        for i in xrange(0, size[0]):
            for j in xrange(0, size[1]):
                if(a[j, i] == 0):
                    self.graph.remove_node((i, j))

        # create positions map
        self.nodePositions = {}
        for pair in self.graph.nodes():
            self.nodePositions[pair] = (pair[0] * 2.0, pair[1] * 2.0)




if __name__ == "__main__":
    b1 = Board('test.bmp')
    b1.addRobot((0, 0), 1)
    b1.addRobot((0, 1), 2)
    print b1.getAllowedMoves((0, 0))
    print b1.getRobots()
    b1.refreshBoard();

    b1.moveRobot((0, 1), (0, 2));
    print b1.getRobots()

    b1.moveRobot((0, 2), (0, 3));
    b1.moveRobot
    b1.refreshBoard();
    b1.moveRobot((0, 3), (0, 4));
    b1.refreshBoard();
    b1.moveRobot((0, 4), (0, 3));
    b1.refreshBoard();





#    plt.show()
#    
#    b2 = Board('test2.bmp')
#    nx.draw_networkx_edges(b2.graph, b2.nodePositions)
#    nx.draw_networkx_nodes(b2.graph, b2.nodePositions, node_size=50)
#    plt.savefig("test2-results.png")
#    plt.show()

