import sys
import time
import BaseHTTPServer
from robot import Robot
from board.board import Board
from networkx import shortest_path, shortest_path_length
from itertools import permutations
from SocketServer import BaseRequestHandler

HOST_NAME = 'localhost'
board = None
robots = {}
robotsPaths = {}
moves = {}


EXPONENT = 7

class PermutationShortestPathAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    agent that searches shortest paths in different orders to achieve the best solution
    '''
    
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        robotsPaths = {}

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_POST(self):
        """Respond to a POST request."""
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        robot = Robot()
        robot.from_json(post_body)
  #      robotsPaths = {}
        if(not robotsPaths.has_key(robot.getId())):
            robots[robot.getId()] = robot
            self.calculatePaths(board, robot)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

#        print 'id: {0}, path: {1}, position: {2}'.format(robot.getId(), robotsPaths[robot.getId()], robot.position)


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %s, %s ] }' % robot.getOwnPosition())
        else:
            allowedMoves = robot.allowedMoves
            desired = moves[robot.getId()][0]
            print desired
            if desired in allowedMoves:
                del moves[robot.getId()][0]
                self.wfile.write('{ "move": [ %s, %s ] }' % desired)
            else:
                self.wfile.write('{ "move": [ %s, %s ] }' % robot.getOwnPosition())
                
    def calculatePaths(self, b, robot):
            global moves
            paths = {}
            for dest in robot.destination :
                paths[dest] = shortest_path_length(b.graph, robot.getOwnPosition(), dest)
        
            # strip the first node on path -> the starting position    
            sp = shortest_path(b.graph, robot.getOwnPosition(), min(paths, key=paths.get))[1:]
            robotsPaths[robot.getId()] = sp
        
            penalty = sys.maxint
            for perm in permutations(robotsPaths):
                positions = []
                newMoves = {}
                for id in perm:
                    robot = robots[id]
                    time = 0
                    if len(positions) <= time:
                        positions.append([])
                    positions[time].append(robot.getOwnPosition())
        
                    newMoves[robot.getId()] = []
                    oldPosition = robotsPaths[robot.getId()][0]
                    positions[0].append(oldPosition)
                    newMoves[robot.getId()].append(oldPosition)
                    for position in robotsPaths[robot.getId()][1:]:
                        time = time + 1
                        if len(positions) <= time:
                            positions.append([])
                        while position in positions[time]:
                            if len(positions) <= time:
                                positions.append([])
                            positions[time].append(oldPosition)
                            if robot.getId() not in newMoves:
                                newMoves[robot.getId()] = []
                            newMoves[robot.getId()].append(oldPosition)
                            time += 1
                        positions[time].append(position)
                        if robot.getId() not in newMoves:
                            newMoves[robot.getId()] = []
                        newMoves[robot.getId()].append(position)
                        oldPosition = position
        
                newPenalty = sum(map(lambda x: (len(newMoves[x]) - len(robotsPaths[x])) ** EXPONENT, newMoves.keys()))
                print  newPenalty
                if penalty > newPenalty:
                    penalty = newPenalty
                    moves = newMoves



if __name__ == '__main__':
    board = Board(sys.argv[2], False)

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), PermutationShortestPathAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
