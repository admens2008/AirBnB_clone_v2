#!/usr/bin/python3
""" unittest for amenity class """
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from datetime import datetime
import json
import os
from time import sleep
import models
import unittest
from os import getenv
import MySQLdb


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestUser_save(unittest.TestCase):
    """ test save method for User class """
    @classmethod
    def setUp(self):
        """setUp the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_for_user_object(self):
        """ test_save_for_user_object """
        user = User()
        user.save()
        Ukey = "User." + user.id
        objs = models.storage.all()
        with open("file.json", "r") as file:
            self.assertIn(Ukey, file.read())
            self.assertIn(Ukey, objs)

    def test_save_and_pass_argument(self):
        """ test_save_and_pass_argument """
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_save_on_two_calls(self):
        """ test save for two different calls """
        user = User()
        sleep(0.1)
        updated_at_1 = user.updated_at
        user.save()
        updated_at_2 = user.updated_at
        self.assertLess(updated_at_1, updated_at_2)
        sleep(0.1)
        user.save()
        self.assertLess(updated_at_2, user.updated_at)


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestUser_to_dict(unittest.TestCase):
    """class to test to_dict method for Amenity class """
    @classmethod
    def setUp(self):
        """ setUp the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_to_dict_keys_if_same(self):
        """  test_to_dict_keys_if_same """
        user = User()
        self.assertNotEqual(user.__dict__, user.to_dict())

    def test_to_dict_type(self):
        """ test_to_dict_type """
        user = User()
        self.assertTrue(dict, type(user.to_dict()))

    def test_to_dict_with_None_arg(self):
        """ test_to_dict_with_None_arg """
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)

    def test_if_to_dict_kv_is_same_with__dict__(self):
        """ check if  test passes the  missing __class__ in __dict__"""
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_if_2_dict_kv_are_equal(self):
        """ test_if_2_dict_kv_are_equal """
        date_now = datetime.today()
        user = User()
        user.id = "909000"
        user.email = "gg@gmail.com"
        user.password = "828873"
        user.first_name = "pascal"
        user.last_name = "ojukwu"
        user.name = "Home appliances"
        user.created_at = date_now
        user.updated_at = date_now
        dict_amenity = {
            '__class__': 'User',
            'id': '909000',
            'name': 'Home appliances',
            'created_at': date_now.isoformat(),
            'updated_at': date_now.isoformat(),
            'email': 'gg@gmail.com',
            'password': '828873',
            'first_name': 'pascal',
            'last_name': 'ojukwu'
        }
        self.assertDictEqual(dict_amenity, user.to_dict())

    def test_dict_attributes_if_equal(self):
        """test_dict_attributes_if_equal"""
        user = User()
        user.attr_name = "Pascal"
        user.age = 67
        self.assertEqual("Pascal", user.attr_name)
        self.assertIn("attr_name", user.to_dict())


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestUser___str__(unittest.TestCase):
    @classmethod
    def setUp(self):
        """ setup the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    """ test str method if same """
    def test_str(self):
        """ test str representation """
        user = User()
        s = f"[{user.__class__.__name__}] ({user.id}) {user.__dict__}"
        self.assertEqual(user.__str__(), s)


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "test")
class TestUser__init__(unittest.TestCase):
    """ test init method for Amenity"""
    @classmethod
    def setUp(self):
        """ setup the enviroment for testing"""
        try:
            os.rename("file.json", "pascal")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        """ teardown the enviroment to end the testing"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("pascal", "file.json")
        except IOError:
            pass

    def test_user_with_none_parameters(self):
        """ test_User_with_none_parameters"""
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_superclass_of_user(self):
        """ test_superclass_of_user """
        user = User()
        self.assertTrue(issubclass(type(user), BaseModel))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_name_is_public_class_attribute(self):
        """ check if attr type is same as dict as well"""
        user = User()
        self.assertIn("first_name", dir(User()))
        self.assertEqual(str, type(User.password))
        self.assertEqual(str, type(User.email))
        self.assertEqual(str, type(User.last_name))
        self.assertEqual(str, type(User.first_name))
        self.assertNotIn("first_name", user.__dict__)

    def test_User_type(self):
        """ test User type """
        self.assertEqual(type(User()), User)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_User_public_attributes_type(self):
        """ test_public_public_attributes_type """
        self.assertEqual(str, type(User.first_name))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'NO DB')
    def test_id_if_typeis_str(self):
        """ test_id_if_typeis_str"""
        self.assertEqual(str, type(User().first_name))

    def test_created_at_if_typeis_datetime(self):
        """ test_created_at_if_type_datetime """
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_if_typeis_datetime(self):
        """ test_updated_at_if_type_datetime """
        self.assertEqual(datetime, type(User().updated_at))

    def test_dir(self):
        """ test dir and name attr"""
        user = User()
        user.email = "alx@yahoo.com"
        self.assertIn("email", dir(User()))
        self.assertIn("email", user.__dict__)

    def test_two_user_id_if_they_are_not_same(self):
        """ test_two_amenities_id_if_they_are_not_same """
        usr = User()
        usr_1 = User()
        self.assertNotEqual(usr.id, usr_1.id)

    def test_User_type(self):
        """ test User type"""
        self.assertEqual(type(User()), User)


if __name__ == "__main__":
    unittest.main()
