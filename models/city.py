#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    
    state_id = Column(String(60), ForeignKey("states.id"))
    name = Column(String(128))
