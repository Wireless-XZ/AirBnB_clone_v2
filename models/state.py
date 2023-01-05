#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from models.city import City
from os import getenv
import models


storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    '''
    Implementation for the State.
    '''
    __tablename__ = 'states'
    if storage_type == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates='state')
    else:
        name = ""

        if storage_type != 'db':
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
