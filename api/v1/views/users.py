#!/usr/bin/python3
"""users view to handle all users_request API"""
from models import storage
from models.user import User
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retreive all users of the application """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    eachuser = []
    for s in storage.all(User).values():
        eachuser.append(s.to_dict())
    return jsonify(eachuser)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a User object: GET /api/v1/users/<user_id>"""
    eachuser = storage.get(User, user_id)
    if eachuser is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachuser.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE_user_by_id(user_id):
    """ Deletes a User object:: DELETE /api/v1/users/<user_id>"""
    eachuser = storage.get(User, user_id)
    if eachuser is None:
        abort(404)
    else:
        storage.delete(eachuser)
        storage.save()
        return (jsonify({}))


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_user():
    """create a new user"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update a user record"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
