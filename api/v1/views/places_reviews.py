#!/usr/bin/python3
"""reviews view to handle all reviews request API"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import Flask, jsonify, abort, request, make_response
from werkzeug.exceptions import NotFound
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place_id(place_id):
    """ Retrieves all reviews object: GET /reviews/<place_id>/reviews'"""
    reviews = []
    onereview = None
    for s in storage.all(Review).values():
        if s.place_id == place_id:
            reviews.append(s.to_dict())
            onereview = s.to_dict()
    if len(reviews) <= 0:
        abort(404)
    else:
        if len(reviews) == 1:
            return jsonify(onereview)
        return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieves a review object: GET /api/v1/reviews/<review_id>"""
    eachreview = storage.get(Review, review_id)
    if eachreview is None:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        abort(404)
        return response
    else:
        return jsonify(eachreview.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def DELETE_review_by_id(review_id):
    """ Deletes a review object:: DELETE /api/v1/reviews/<review_id>"""
    eachreview = storage.get(Review, review_id)
    if eachreview is None:
        abort(404)
    else:
        storage.delete(eachreview)
        storage.save()
        return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review_by_placeid(place_id):
    """create a new review"""
    oneplace = storage.get(Place, place_id)
    if oneplace is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    record = request.get_json()
    oneuser = storage.get(User, record['user_id'])
    if oneuser is None:
        abort(404)
    record['place_id'] = oneplace.id
    review = Review(**record)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id',
                        'place_id', 'created_at', 'updated_at']:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict())
