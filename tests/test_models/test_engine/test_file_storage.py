#!/usr/bin/python3
"""unittest Module for FileStorage class"""

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage
import datetime
from models.__init__ import storage
import json
import os
import models
import unittest
from os import getenv


class TestFileStorage_save(unittest.TestCase):
    """ test save method in Filestorage class """
    @classmethod
    def setUp(self):
        """ setup enviroments for the unittest """
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ tear down enviroments  for the unittest"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def clearStorage(self):
        """ clear the file contents for the unittest"""
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_save_with_None_parameter(self):
        """Test that models.storage.save() with None parameter does nothing"""
        pass
        # Check that the method returns None

    def test_save(self, obj=None):
        """ test_save_bypassing_None_parameter """
        with self.assertRaises(TypeError):
            models.storage.save(obj)

    def test_FileStorage_save(self, obj=None):
        """ test_save_bypassing_None_parameter """
        with self.assertRaises(TypeError):
            store = FileStorage()
            store.save(obj)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_method(self):
        """ test save function in filestorage class"""
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        with open("file.json", 'r') as file:
            getllobjs = file.read()
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)


class TestFileStorage_reload(unittest.TestCase):
    """ test reload method in Filestorage class """
    @classmethod
    def setUp(self):
        """ set up enviroments for the unit test """
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ tear down enviroments """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_reload(self):
        """ test_reload function to see if it works"""
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        storage.reload()
        getllobjs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)

    def test_reload_bypassing_None_parameter(self):
        """ test_reload_bypassing_None_parameter """
        with self.assertRaises(TypeError):
            storage.reload(None)


class TestFileStorage_all(unittest.TestCase):
    """ Test all method for file storage"""
    @classmethod
    def setUp(self):
        """ setup enviroments for the unittest"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ tear down enviroments for the unittest"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def clearStorage(self):
        """ clear the file contents  """
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_all(self):
        """ test all type """
        self.assertEqual(dict, type(models.storage.all()))

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_with_parameter(self):
        """ __objects is properly returned """
        new = State()
        new2 = BaseModel()
        temp = storage.all(cls='State')
        self.assertIsInstance(temp, dict)
        temp2 = storage.all(cls='BaseModel')
        self.assertIsInstance(temp2, dict)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_all_method(self):
        """ test_all_method """
        bmodel = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(bmodel)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        getllobjs = models.storage.all().keys()
        self.assertIn("BaseModel." + bmodel.id, getllobjs)
        self.assertIn("User." + user.id, getllobjs)
        self.assertIn("State." + state.id, getllobjs)
        self.assertIn("Place." + place.id, getllobjs)
        self.assertIn("City." + city.id, getllobjs)
        self.assertIn("Amenity." + amenity.id, getllobjs)
        self.assertIn("Review." + review.id, getllobjs)


class TestFileStorage__file_path(unittest.TestCase):
    """ Test __file_path if its correct"""
    def FileStorage__file_path(self):
        """ Test __file_path if its correct"""
        self.assertEqual("file.json", FileStorage__file_path)
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))


class TestFileStorage__init__(unittest.TestCase):
    """ Test all method for file storage"""

    def test_FileStorage_with_none_parameters(self):
        """ test_FileStorage_with_none_parameters"""
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_type(self):
        """ test FileStorage type """
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_private_attributes_type(self):
        """ test_FileStorage_private_attributes_type """
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_private_dict_type(self):
        """testFileStorage_private_dict_type"""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_storage_type(self):
        """ test storage type"""
        self.assertEqual(type(models.storage), FileStorage)


if __name__ == "__main__":
    unittest.main()
