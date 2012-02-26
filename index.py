import json
import bottle
from bottle import route, run, request, abort, response
from bottle import mako_view as view, mako_template as template
from pymongo import Connection, GEO2D
from bson import json_util
from json import JSONEncoder
from pymongo.objectid import ObjectId
 
class MongoEncoder(JSONEncoder):
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)
            
            
bottle.TEMPLATE_PATH.insert(0,'/Applications/MAMP/htdocs/bottle/env/views/')

connection = Connection('localhost', 27017)
db = connection.mydatabase

@route('/locations', method='PUT')
def put_location():
	data = request.body.readline()
	if not data:
		abort(400, 'No data received')
	entity = json.loads(data)
	try:
		db['locations'].save(entity)
	except ValidationError as ve:
		abort(400, str(ve))
		
@route('/people', method='GET')
@view('people')
def get_people():
	return dict(people=['James','Joshua'])

	
@route('/locations/:lat/:lng', method='GET')
def get_location(lat,lng):
	response.content_type = 'application/json'
	objdb = db.locations.find({'coordinate2d': {'$near': [lat,lng]}}, {'coordinate2d':bool(1)}).skip(0).limit(3)
	entries = [entry for entry in objdb]
	return MongoEncoder().encode(entries)

from bottle import static_file
@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='/static/')

run(host='localhost', port=8080)