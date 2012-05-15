import httplib
import json
from server import State

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

def get_move(url, state):
	httpServ = httplib.HTTPConnection(url)
	httpServ.connect()
	httpServ.request('POST', "/test", state.to_json())
	response = httpServ.getresponse()
	httpServ.close()
	if response.status == httplib.OK:
		return tuple(json.loads(response.read())['move']) 
	#TODO throw exception

if __name__ == '__main__':
	s = State()
	s.allowedMoves.append((1,1))
	s.setOwnPosition((0,0))
	s.agents.append((0,0))
	print get_move("127.0.0.1:8000", s)
