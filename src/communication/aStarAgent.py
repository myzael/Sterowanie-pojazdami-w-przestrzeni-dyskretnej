import sys

sys.path.append("/home/makz/studia/agenty/Sterowanie-pojazdami-w-przestrzeni-dyskretnej/src")
import time
import BaseHTTPServer
import random
from board.board import Board
from robot import Robot

HOST_NAME = 'localhost'

b = None

def a_star(start, end):
    global b
    closedset = set()
    openset = {start}
    path = []
    previous = {}

    while openset:
        current = min(openset, key=lambda point: abs(end[0] - point[0]) + abs(end[1] - point[1]))
        if current == end:
            path.insert(0, current)
            while current in previous :
                current = previous[current]
                path.insert(0, current)
            return path
        openset.remove(current)
        closedset.add(current)
        for point in b.getAllowedMoves(current):
            if point not in closedset:
                if point not in openset:
                    openset.add(point)
                previous[point] = current
    return path

class aStarAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        """Respond to a POST request."""
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        print post_body
        robot = Robot()
        robot.from_json(post_body)
        print a_star(robot.position, robot.destination[0])
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %s, %s ], "speed" : 1, "velocity" : [1, 1] }' % robot.getOwnPosition())
        else:
            move = robot.allowedMoves[int(random.random() * len(robot.allowedMoves))]
            self.wfile.write('{ "move": [ %s, %s ], "speed" : 1, "velocity" : [%s, %s] }' % (
                move[0][0], move[0][1], move[1][0], move[1][1]))

if __name__ == '__main__':
    b = Board(sys.argv[2], False)
    print a_star((0, 0), (5, 6))
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), aStarAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
