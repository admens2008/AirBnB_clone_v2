#!/usr/bin/python3
"""  class User that inherits from BaseModel:"""
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
import os


class User(BaseModel, Base):
    """Public class attributes:
email: string - empty string
password: string - empty string
first_name: string - empty string
last_name: string - empty string"""

    __tablename__ = "users"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        email = ""
        password = ""
        first_name = ""
        last_name = ""
    else:
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128))
        last_name = Column(String(128))
        places = relationship("Place", backref="user", cascade="delete")
        reviews = relationship("Review", backref="user", cascade="delete")
