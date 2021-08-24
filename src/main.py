"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Person, Task
#from models import Person

#creo un usuario 
#this made the conecction with the DB
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.serialize()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#this help us to get the information from the table. We must to do this for each of them
@app.route('/person', methods=['GET'])
def getPerson():
    persons = Person.get_all()
    if persons:
        return jsonify(persons),200
    
    return jsonify({'message': 'Error. Table not found'}), 500

#
@app.route('/person/<int:id>/tasks', methods=['GET'])
def get_task(id):
    personTask = Task.get_task_by_person(id)
    if not personTask:
        return jsonify({'message': 'task not found'}), 200
    return jsonify(personTask), 201

#
@app.route('/person', methods=['POST'])
def create_personTask():
    nickmane = request.json.get('nickname')
    if not (nickmane):
        return {'error': 'Missing info'}, 400
    
    user = Person(nickmane = nickmane)
    user.create()

    return jsonify(user.serialize()), 201

@app.route('/person/<int:id>/task', methods = ['POST'])
def add_new_task(id):
    task_txt = request.json.get('task_txt')
    if not (task_txt and id):
        return {'error': 'Error'}, 400

    task = Task(task_txt and id)
    task.add_new()

    return jsonify(task.serialize()), 201
    print("insuficiente ", request_body)
    return jsonify(task)

@app.route('/person/<int:id>', methods = ['DELETE'])
def delete_account(id):
    person = Person.get_by_id(id)

    if person:
        person.delete()
        return jsonify(person.serialize()),200
    
    return jsonify({'msg': 'Account not found'}),404

#@app.route('/person/<int:id>', methods = ['PATCH'])
#def update_account_by_id(id):
 #   person = person.read_by_id(id)
  #  if not person:
   #     return jsonify({'messege': 'person not found'}), 404

    #new_nickname = request.jason.get('nickname')
    #if new_nickname and not person.get_by_nickmane(new_nickname):
     #   person.update(new_nickname)
      #  return jsonify(person.to_dict()), 200

    #return jsonify({'message': 'nickname exist'}), 400

#@app.route('/person/<int:id>/task/<int:position>', methods=['DELETE'])
#def delete_personTask(id, position):

    #task_to_delete = Task.get_one_task(position)
   # if(task_to_delete):
       # task_to_delete.delete()
        #return jsonify(task_to_delete.to_dict()),200

   # return{'error': 'Not access'}, 400

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
