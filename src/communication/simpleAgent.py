import sys
import time
import BaseHTTPServer
import random
from robot import Robot

HOST_NAME = 'localhost'


class SimpleAgent(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    simple agent choosing random move until it reaches destination
    '''

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
        print robot.position
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if robot.getOwnPosition() in robot.destination:
            self.wfile.write('{ "move": [ %s, %s ], "speed" : 1, "velocity" : [1, 1] }' % robot.getOwnPosition())
        else:
            move = robot.allowedMoves[int(random.random() * len(robot.allowedMoves))]
            self.wfile.write('{ "move": [ %s, %s ], "speed" : 1, "velocity" : [%s, %s] }' %( move[0][0], move[0][1], move[1][0], move[1][1]))

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), SimpleAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, sys.argv[1])
