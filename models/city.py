#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, DateTime
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    '''
    Define the class City that inherits from BaseModel.
    '''
    __tablename__ = 'cities'
    if storage_type == 'db':
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime)
        upated_at = Column(DateTime)
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        state = relationship("State", back_populates="cities")
    else:
        name = ""
        state_id = ""
