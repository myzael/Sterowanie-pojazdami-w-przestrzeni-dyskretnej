import sys
import time
import BaseHTTPServer
import random
from robot import Robot
from board.board import Board
from networkx import shortest_path, shortest_path_length

HOST_NAME = 'localhost'
b = None
robots = {}


def calculatePath(robot):
#    choose the destination with shortest path
    paths = {}
    for dest in robot.destination :
        paths[dest] = shortest_path_length(b.graph, robot.getOwnPosition(), dest)
    return shortest_path(b.graph, robot.getOwnPosition(), min(paths, key=paths.get))[1:]



class ShortestPathAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    simple agent choosing the shortest path for all robots
    '''

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

        if(not robots.has_key(robot.getId())):
            robots[robot.getId()] = calculatePath(robot)

        robots[robot.getId()].remove(robot.getOwnPosition())
        print robot.position
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %self, %self ] }' % robot.getOwnPosition())
        else:
            moves = robot.allowedMoves
            desired = robots[robot.getId()][0]
            if desired in moves:
                del robots[robot.getId()][0]
                self.wfile.write('{ "move": [ %self, %self ] }' % desired)
            else:
                self.wfile.write('{ "move": [ %self, %self ] }' % robot.getOwnPosition())

if __name__ == '__main__':
    b = Board(sys.argv[2], False)

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), ShortestPathAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
