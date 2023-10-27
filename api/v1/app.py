#!/usr/bin/python3
""" test the application  your API  and all the application"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
# cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(error):
    """ dhdhhdkjkdkkkkkkfkkfkfkkfmmfmmnnn"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current connection"""
    storage.close()


if __name__ == '__main__':
    """ main function"""
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')), threaded=True)
