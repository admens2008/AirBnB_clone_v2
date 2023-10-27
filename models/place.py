#!/usr/bin/python3
"""  class place that inherits from BaseModel:"""
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import *
from sqlalchemy.orm import *
if os.getenv('HBNB_TYPE_STORAGE') == "db":
    place_amenity = Table("place_amenity", Base.metadata,
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """place attributes for class Place"""
    __tablename__ = "places"
    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
    else:
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0)
        number_bathrooms = Column(Integer, default=0)
        max_guest = Column(Integer, default=0)
        price_by_night = Column(Integer, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship("Review", backref="place", cascade="delete")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    if os.getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def amenities(self):
            """getter attribute returns the list of Amenity instances"""
            from models.amenity import Amenity
            amenity_list = []
            all_amenities = models.storage.all(Amenity)
            for amenity in all_amenities.values():
                if amenity.place_id == self.id:
                    amenity_list.append(amenity)
            return amenity_list

        @property
        def reviews(self):
            """getter attribute return the list of Review instances"""
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def cities(self):
            """getter attribute reviewa that returns the list
              of reviews instances with place_id equals to the
              current place.id"""
            reviewslist = []
            for rev in models.storage.all('Review').values():
                if rev.place_id == Place.id:
                    reviewslist.append(rev)
            return reviewslist
