import json
import sys
import ast
import time
import BaseHTTPServer


HOST_NAME = 'localhost'

class Robot:
    def __init__(self):
        self.agents = []
        self.allowedMoves = []

    def setOwnPosition(self, position):
        self.position = position

    def to_json(self):
        return json.dumps(self.__dict__)

    def from_json(self, json):
        dictionary = ast.literal_eval(json)
        self.agents = [ (x[0], x[1]) for x in dictionary["agents"]]
        self.allowedMoves = [ (x[0], x[1]) for x in dictionary["allowedMoves"]]
        self.position = (tuple(dictionary["position"]))




class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
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
        s.wfile.write('{ "move": [ %s, %s ] }' %robot.allowedMoves[0])

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(sys.argv[1])), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, sys.argv[1])
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
