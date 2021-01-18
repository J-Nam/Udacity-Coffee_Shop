import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES

@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.short() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks_short
        }), 200
    except Exception:
        abort(404)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": drinks_long
        }), 200
    except Exception:
        abort(404)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    try:
        drink_data = request.get_json()
        if 'title' and 'recipe' not in drink_data:
            abort(422)
        title = drink_data['title']
        recipe = json.dumps(drink_data['recipe'])
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]

        return jsonify({
            "success": True,
            "drinks": drinks_long
        }), 200
    except Exception:
        db.session.rollback()
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    data = request.get_json()
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    try:
        title = data.get('title')
        recipe = json.dumps(data.get('recipe'))
        drink.title = title
        drink.recipe = recipe
        drink.update()
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
    except Exception:
        db.session.rollback()
        abort(422)

    return jsonify({
            "success": True,
            "drinks": drinks_long
    })


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    try:
        drink.delete()
    except Exception:
        db.session.rollback()
        abort(422)

    return jsonify({
            "success": True,
            "delete": id
    })

# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(AuthError)
def handle_auth_error(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response
