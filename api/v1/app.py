#!/usr/bin/python3
"""states view to handle all states request API"""
from api.v1.views import app_views
from models import storage
from os import environ
from flask import Flask, render_template, make_response, jsonify


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """close the session connection when done"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error handler"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """main function"""
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
