import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Added CORS and after_request decorator to set Access-Control-Allow
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                        'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                        'GET, PATCH, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

'''
 @TODO - Done: 
 Ucomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# Populate Drink models.py with 3 rows test data initially
drink = Drink(title='black coffee', recipe='[{"name": "beans", "color": "red", "parts": 1}]')
drink.insert()
drink = Drink(title='cappuccino', recipe='[{"name": "milk and beans", "color": "green", "parts": 2}]')
drink.insert()
drink = Drink(title='double expresso', recipe='[{"name": "only beans", "color": "blue", "parts": 3}]')
drink.insert()

## ROUTES
'''
 @TODO - Done:
 Implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['GET'])
def get_drinks():

    drink_query = Drink.query.all()
    drinks = [drink.short() for drink in drink_query]
    
    if len(drinks) == 0:
        abort(404)
    
    try:
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200

    except:
        abort(404)

'''
 @TODO - Done:
 Implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):

    drink_query = Drink.query.all()
    drinks = [drink.long() for drink in drink_query]
    
    if len(drinks) == 0:
        abort(404)
    
    try:
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200

    except:
        abort(404)


'''
 @TODO - Done:
 Implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
        --#[drink.long()]
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
   
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if not title or not recipe:

        return jsonify({
            "success": False,
            "error": 422,
            "message": "Missing title or recipe"
        }), 422

    try:

        drink = Drink(title=title, recipe=json.dumps(recipe))
    
        drink.insert()   

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        }), 200

    except:
        abort(422)


'''
 @TODO - Done:
 Implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
        --Note: changed return array from drink to drinks as the array
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    
    if drink_id is None: 
        abort(404)

    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404)

    request_json = request.get_json()
    drink.title = request.json.get('title')
    drink.recipe = json.dumps(request_json.get('recipe'))

    drink.update()
    drinks = []
    drinks.append(drink.long())

    return jsonify({
        "success": True, 
        "drinks": drinks
        }), 200

'''
 @TODO - Done:
 Implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:drink_id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        if drink_id is None: 
            abort(404)

        drink = Drink.query.get(drink_id)

        if drink is None:
            abort(404)

        drink.delete()

        return jsonify({
            "success": True, 
            "delete": drink_id
            }), 200
    except:
        abort(422)


## Error Handling
'''
 @TODO - Done:
 Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "Unprocessable Entity"
                    }), 422

'''
 @TODO - Done:
 Implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Resource Not Found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "Bad request"
                    }), 400


@app.errorhandler(401)
def not_authorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "Not Authorized"
                    }), 401

'''
 @TODO - Done:
 Implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def record_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Record Not Found"
                    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False, 
                    "error": 405,
                    "message": "Method Not Allowed"
                    }), 405

'''
 @TODO - Done:
 Implement error handler for AuthError
    error handler should conform to general task above 
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    @app.errorhandler(AuthError)
    def authentication_failed(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": "Authentication failed"
        }), 401
