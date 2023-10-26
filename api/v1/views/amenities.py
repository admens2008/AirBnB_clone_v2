#!/usr/bin/python3
"""amenity view to handle all amenities request API"""
from models import storage
from models.amenity import Amenity
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retreive all amenities of the application """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    eachamenity = []
    for s in storage.all(Amenity).values():
        eachamenity.append(s.to_dict())
    return jsonify(eachamenity)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves a State object: GET /api/v1/amenities/<amenity_id>"""
    eachamenity = storage.get(Amenity, amenity_id)
    if eachamenity is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachamenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE_amenity_by_id(amenity_id):
    """ Deletes a State object:: DELETE /api/v1/amenities/<amenity_id>"""
    eachamenity = storage.get(Amenity, amenity_id)
    if eachamenity is None:
        abort(404)
    else:
        storage.delete(eachamenity)
        storage.save()
        return (jsonify({}))


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    amenity.save()
    return jsonify(amenity.to_dict())
