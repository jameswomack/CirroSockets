import sys
import json
import bottle
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from bottle import route, Bottle, view, request
from bottle import route, run, request, abort, response
from bottle import mako_view as view, mako_template as template
from pymongo import Connection, GEO2D
from bson import json_util
from json import JSONEncoder
from bson.objectid import ObjectId

app = Bottle()

j = []

class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


connection = Connection('localhost', 27017)
db = connection.mydatabase

@app.route('/locations', method='PUT')
def put_location():
	data = request.body.readline()
	if not data:
		abort(400, 'No data received')
	entity = json.loads(data)
	try:
		db['locations'].save(entity)
	except ValidationError as ve:
		abort(400, str(ve))

@app.route('/people', method='GET')
@view('people')
def get_people():
	return dict(people=['James','Joshua'])


@app.route('/locations/:lat/:lng', method='GET')
def get_location(lat,lng):
	response.content_type = 'application/json'
	objdb = db.locations.find({'coordinate2d': {'$near': [lat,lng]}}, {'coordinate2d':bool(1)}).skip(0).limit(3)
	entries = [entry for entry in objdb]
	return MongoEncoder().encode(entries)

from bottle import static_file
@app.route('/<filename>')
def server_static(filename):
    return static_file(filename, root='static')

@app.route('/')
def server_static():
    return static_file('index.html', root='static')

@app.route('/ws')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        j.append(ws)
        try:
            while True:
            	if ws is not None:
                	message = ws.receive()
                if not message:
                    break
                for _ws in j:
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
