#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Integer, Float, ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from os import getenv
#from models.city import City
#from models.user import User


storage_type = getenv("HBNB_TYPE_STORAGE")
metadata = Base.metadata
place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=1)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    if storage_type == 'db':
         reviews = relationship("Review", backref="place",
                                cascade="all, delete-orphan")
         amenities = relationship("Amenity",secondary=place_amenity,
                                  back_populates="place_amenities",
                                  viewonly=False)
    else:
        @property
        def reviews(self):
            """
            get list of Review instances with
            place_id equals to the current Place.id
            """
            list_reviews = []
            all_reviews = self.reviews
            for review in all_reviews:
                if review.place_id == Place.id:
                    list_reviews.append(review)
            return list_reviews

        @property
        def amenities(self):
            amenities_list = []
            amenity_objs = []
            for amenity_id in self.amenity_ids:
                key = 'Amenity.' + amenity_id
                if key in FileStorage.__objects:
                    amenity_objs.append(FileStorage.__objects[key])
            return amenity_objs

        @amenities.setter
        def amenities(self, obj):
            """
            adds an Amenity.id to the attribute amenity_ids if obj is
            an instance of Amenity
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
