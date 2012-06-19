import sys
import time
import BaseHTTPServer
from robot import Robot
from board.board import Board
from networkx import shortest_path, shortest_path_length
from itertools import permutations
from SocketServer import BaseRequestHandler

HOST_NAME = 'localhost'
b = None



EXPONENT = 7

class PermutationShortestPathAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    agent that searches shortest paths in different orders to achieve the best solution
    '''
    
    def __init__(self, request, client_address, server):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.robotsPaths = {}

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
  #      self.robotsPaths = {}
        if(not self.robotsPaths.has_key(robot.getId())):
            self.robotsPaths = self.calculatePaths(b, robot)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return

#        print 'id: {0}, path: {1}, position: {2}'.format(robot.getId(), self.robotsPaths[robot.getId()], robot.position)


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %s, %s ] }' % robot.getOwnPosition())
        else:
            moves = robot.allowedMoves
            desired = self.robotsPaths[robot.getId()][0]
            print desired
            if desired in moves:
                del self.robotsPaths[robot.getId()][0]
                self.wfile.write('{ "move": [ %s, %s ] }' % desired)
            else:
                self.wfile.write('{ "move": [ %s, %s ] }' % robot.getOwnPosition())
                
    def calculatePaths(self, b, robot):
            paths = {}
            for dest in robot.destination :
                paths[dest] = shortest_path_length(b.graph, robot.getOwnPosition(), dest)
        
            # strip the first node on path -> the starting position    
            sp = shortest_path(b.graph, robot.getOwnPosition(), min(paths, key=paths.get))[1:]
            self.robotsPaths[robot] = sp
        
            penalty = sys.maxint
            for perm in permutations(self.robotsPaths):
                positions = []
                newMoves = {}
                for robot in perm:
                    time = 0
                    if len(positions) <= time:
                        positions.append([])
                    positions[time].append(robot.getOwnPosition())
        
                    newMoves[robot] = []
                    for position in self.robotsPaths[robot]:
                        time = time + 1
                        if len(positions) <= time:
                            positions.append([])
                        while position in positions[time]:
                            time = time + 1
                            if len(positions) <= time:
                                positions.append([])
                            positions[time].append(position)
                            if robot not in newMoves:
                                newMoves[robot] = []
                            newMoves[robot].append(position)
                        positions[time].append(position)
                        if robot not in newMoves:
                            newMoves[robot] = []
                        newMoves[robot].append(position)
        
                newPenalty = sum(map(lambda x: (len(newMoves[x]) - len(self.robotsPaths[x])) ** EXPONENT, newMoves.keys()))
                if penalty > newPenalty:
                    penalty = newPenalty
                    moves = newMoves
        
            return moves

if __name__ == '__main__':
    b = Board(sys.argv[2], False)

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), PermutationShortestPathAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
