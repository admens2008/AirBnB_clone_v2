#!/usr/bin/python3
"""states view to handle all states request API"""
from models import storage
from models.state import State
from models.city import City
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves a city object: GET /api/v1/cityies/<city_id>"""
    eachcity = storage.get(City, city_id)
    if eachcity is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachcity.to_dict())


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state_id(state_id):
    """ Retrieves a cities object: GET /api/v1/states/<state_id>"""
    state_ = {'state_id': state_id}
    cities = []
    onecity = None
    for s in  storage.all(City).values():
        if s.state_id == state_id:
            cities.append(s.to_dict())
            onecity = s.to_dict()
    if len(cities) <= 0:
        abort(404)
    else:
        if len(cities) == 1:
            return jsonify(onecity)
        return jsonify(cities)


@app_views.route('/states/s/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE__state_by_id(state_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    eachstate = storage.get(State, state_id)
    if eachstate is None:
        abort(404)
    else:
        storage.delete(eachstate)
        storage.save()
        return (jsonify({}))


@app_views.route('/states/k/', methods=['POST'], strict_slashes=False)
def post__state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/n/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put__state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())
