import json
import ast
import time
import BaseHTTPServer


HOST_NAME = 'localhost'
PORT_NUMBER = 8000


class State:
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
	state = State()
	state.from_json(post_body)
	print state.position
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write('{ "move": [ %s, %s ] }' %state.allowedMoves[0])

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
