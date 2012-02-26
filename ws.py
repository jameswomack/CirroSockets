from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from bottle import route, Bottle, view, request

app = Bottle()

j = []

@app.route('/')
@view('index')
def index():
    return {}


@app.route('/ws')
def api():
    if request.environ.get('wsgi.websocket'):
    	print 1
        ws = request.environ['wsgi.websocket']
        j.append(ws)
        print 2
        try:
            while True:
            	print 'True'
            	print 3
            	if ws is not None:
                	message = ws.receive()
                print 4
                if not message:
                    break
                print 5
                for _ws in j:
                	print _ws
                	if _ws is None:
                		j.remove(_ws) 
                	else:
                		_ws.send(message) if _ws != ws else 0
            if ws is not None:
            	ws.close()
            j.remove(ws)
        except geventwebsocket.WebSocketError, ex:
            print '%s: %s' % (ex.__class__.__name__, ex)

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8080), app, \
            handler_class=WebSocketHandler)
    http_server.serve_forever()