import httplib
from server import State

def printText(txt):
    lines = txt.split('\n')
    for line in lines:
        print line.strip()

httpServ = httplib.HTTPConnection("127.0.0.1", 8000)
httpServ.connect()

httpServ.request('GET', "/test")

response = httpServ.getresponse()
if response.status == httplib.OK:
    state = State()
    state.from_json(response.read())
    print state.allowedMoves
    print state.agents
    print state.position

httpServ.close()
