#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models import State, User, City
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("State objects: {}".format(storage.count(User)))
print("State objects: {}".format(storage.count(City)))
first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
