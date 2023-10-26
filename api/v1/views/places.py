#!/usr/bin/python3
"""places view to handle all places request API"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """retreive all places of the application """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    eachplace = []
    for s in storage.all(Place).values():
        eachplace.append(s.to_dict())
    return jsonify(eachplace)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieves a Place object: GET /api/v1/places/<place_id>"""
    eachplace = storage.get(Place, place_id)
    if eachplace is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachplace.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE_place_by_id(place_id):
    """ Deletes a Place object:: DELETE /api/v1/places/<place_id>"""
    eachplace = storage.get(Place, place_id)
    if eachplace is None:
        abort(404)
    else:
        storage.delete(eachplace)
        storage.save()
        return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    onecity = storage.get(City, city_id)
    if onecity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    record = request.get_json()
    oneuser = storage.get(User, record['user_id'])
    if oneuser is None:
        abort(404)
    record['city_id'] = onecity.id
    place = Place(**record)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
