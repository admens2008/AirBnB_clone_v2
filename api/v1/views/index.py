#!/usr/bin/python3
"""app.py to connect to API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """ status of the application """
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
