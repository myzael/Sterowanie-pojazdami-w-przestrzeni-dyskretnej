import sys

sys.path.append("C:\Kuba\Coding\Studies\Agenty\Sterowanie-pojazdami-w-przestrzeni-dyskretnej")
import time
import BaseHTTPServer
from robot import Robot
from src.board.physicsBoard import PhysicsBoard

HOST_NAME = 'localhost'

board = None
limit = None


def selection(openset, end):
    return min(openset, key=lambda point: abs(end[0] - point[0]) + abs(end[1] - point[1]))


def physics_selection(openset, end):
    def heuristics(state):
        x, y = state[0]
        return abs(end[0] - x) + abs(end[1] - y)

    return min(openset, key=heuristics)


def a_star(start, end, robots):
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
            if point not in closedset and point not in robots:
                if point not in openset:
                    openset.add(point)
    return selection(openset, end)


def physics_a_star(start, end):
    print end
    global board
    global limit
    path = []
    previous = {}
    closedset = set()
    openset = {start}
    steps = 0

    while openset and steps < limit:
        steps += 1
        current = physics_selection(openset, end)
        if current[0] == end:
            path.insert(0, current)
            while current in previous:
                current = previous[current]
                path.insert(0, current)
            return path[1]
        openset.remove(current)
        closedset.add(current)
        for state in board.getAvaliableStates(current):
            if state not in closedset:
                if state not in openset:
                    openset.add(state)
                previous[state] = current
    current = physics_selection(openset, end)
    path.insert(0, current)
    while current in previous:
        current = previous[current]
        path.insert(0, current)
    print path
    return path[1]


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
                                  a_star(robot.position, robot.destination[0], robot.robots))
            log = '{"robotID" : %s, "move": [ %s, %s ], "speed" : %s, "velocity" : [%s, %s] }' % (
            robot.id, move[0][0], move[0][1], move[2], move[1][0], move[1][1])
            print log
            self.wfile.write(log)


if __name__ == '__main__':
    board = PhysicsBoard(sys.argv[3], '../../board', 4, 4, 6, False)
    limit = int(sys.argv[2])
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), aStarAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
