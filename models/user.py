#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


storage_type = getenv("HBNB_TYPE_STORAGE")


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"

    if storage_type = "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(Sting(128), nullable=False)
        last_name = Column(Sting(128), nullable=False)
        places = relationship("Place", back_populates="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
