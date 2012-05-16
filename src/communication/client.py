import httplib
import json
from robot import Robot

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

def get_move(url, robot):
	httpServ = httplib.HTTPConnection(url)
	httpServ.connect()
	httpServ.request('POST', "/test", robot.to_json())
	response = httpServ.getresponse()
	httpServ.close()
	if response.status == httplib.OK:
		return tuple(json.loads(response.read())['move']) 
	#TODO throw exception

if __name__ == '__main__':
	r = Robot()
	r.allowedMoves.append((1,1))
	r.setOwnPosition((0,0))
	r.robots.append((0,0))
	print get_move("127.0.0.1:8000", r)
