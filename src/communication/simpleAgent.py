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

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_POST(s):
        """Respond to a POST request."""
        content_len = int(s.headers.getheader('content-length'))
        post_body = s.rfile.read(content_len)
        robot = Robot()
        robot.from_json(post_body)
        print robot.position
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        if robot.getOwnPosition() in robot.destination:
            s.wfile.write('{ "move": [ %s, %s ] }' % robot.getOwnPosition())
        else:
            s.wfile.write('{ "move": [ %s, %s ] }' % robot.allowedMoves[int(random.random() * len(robot.allowedMoves))])

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), SimpleAgent)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
