#!/usr/bin/python3
""" Test delete feature
"""

from models.engine.file_storage import FileStorage
from models.state import City

fs = FileStorage()

# All States
all_city = fs.all(City)
print("All Cityes: {}".format(len(all_city.keys())))
for  city_key in all_city.keys():
            print(all_city[city_key])

            # Create a new State
new_city = City()
new_city.name = "Nnobi"
new_city.state_id = 'c50d05fa-e671-45ee-9691-1d1fee043687'
fs.new(new_city)
fs.save()
print("New city: {}".format(new_city))