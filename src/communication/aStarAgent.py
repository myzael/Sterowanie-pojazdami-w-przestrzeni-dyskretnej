import sys

sys.path.append("/home/makz/studia/agenty/Sterowanie-pojazdami-w-przestrzeni-dyskretnej/src")
from board.physicsBoard import PhysicsBoard
import time
import BaseHTTPServer
from robot import Robot

HOST_NAME = 'localhost'

board = None
limit = None

def selection(openset, end):
    return min(openset, key=lambda point: abs(end[0] - point[0]) + abs(end[1] - point[1]))


def physics_slection(openset, end):
    def heuristics(state):
        x, y = state[0]
        return abs(end[0] - x) + abs(end[1] - y)

    return min(openset, key=heuristics)


def a_star(start, end):
    global board
    global limit
    closedset = set()
    openset = {start}
    steps = 0

    while openset and steps < limit:
        steps += 1
        current = selection(openset, end)
        if current == end:
            return end
        openset.remove(current)
        closedset.add(current)
        for point in board.getFreeNeighbors(current):
            if point not in closedset:
                if point not in openset:
                    openset.add(point)
    return selection(openset, end)


def physics_a_star(start, end):
    global board
    global limit
    path = []
    previous = {}
    closedset = set()
    openset = {start}
    steps = 0

    while openset and steps < limit:
        steps += 1
        current = physics_slection(openset, end)
        if current[0] == end:
            path.insert(0, current)
            while current in previous:
                current = previous[current]
                path.insert(0, current)
            return path[0]
        openset.remove(current)
        closedset.add(current)
        for state in board.getAllowedMoves(current):
            if state not in closedset:
                if state not in openset:
                    openset.add(state)
                previous[state] = current
    current = physics_slection(openset, end)
    path.insert(0, current)
    while current in previous:
        current = previous[current]
        path.insert(0, current)
    return path[0]


class aStarAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self, limit):
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
        print
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %s, %s ], "speed" : 0, "velocity" : [1, 1] }' % robot.getOwnPosition())
        else:
            move = physics_a_star((robot.position, robot.velocity, robot.speed),
                a_star(robot.position, robot.destination[0]))
            self.wfile.write('{ "move": [ %s, %s ], "speed" : %s, "velocity" : [%s, %s] }' % (
                move[0][0], move[0][1], move[2], move[1][0], move[1][1]))

if __name__ == '__main__':
    board = PhysicsBoard(sys.argv[3], 'board', 4, 2, 4, False)
    limit = int(sys.argv[2])
    #    print a_star((0, 0), (12, 2))
    print board.getFreeNeighbors((5, 0))
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), aStarAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
