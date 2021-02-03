import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
#from auth import AuthError
#from flask import jsonify

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
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
    
    if len(drinks) == 0;
        abort(404)
    
    try:
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200

    except:
        abort(404)



'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():

   # drinks = [drink.long() for drink in Drink.query.order_by(Drink.id).all()]

    drink_query = Drink.query.all()
    drinks = [drink.long() for drink in drink_query]
    
    if len(drinks) == 0;
        abort(404)
    
    try:
        return jsonify({
            "success": True,
            "drinks": drinks
        }), 200

    except:
        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(token):
   
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if not title or not recipe:
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Add title and recipe"
        }), 422

    try:
        drink = Drink(title=title, recipe=json.dumps([recipe]))
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200

    except:
        abort(422)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad_request"
                    }), 400


@app.errorhandler(401)
def not_authorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "not authorized"
                    }), 401

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def record_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "record not found"
                    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False, 
                    "error": 405,
                    "message": "method not allowed"
                    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "internal server error"
                    }), 500

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
#https://auth0.com/docs/quickstart/backend/python

# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response