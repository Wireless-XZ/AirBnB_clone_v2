#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv



storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    '''
    Implementation for the State.
    '''
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if storage_type == 'db':
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            get list of City instances with state_id
            equals to the current State.id
            """
            list_cities = []
            all_cities = models.storage.all(City)
            for key, city_obj in all_cities.items():
                if city_obj.state_id == self.id:
                    list_cities.append(city_obj)
            return list_cities
