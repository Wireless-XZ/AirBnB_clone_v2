#!/usr/bin/python3
""" db_storage Module"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


classes = {"State": State, "City": City, "User": User,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """Class definition"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the class instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries on the current database"""
        objs_dict = {}
        if cls is not None:
            if cls in classes:
                for obj in self.__session.query(classes[cls]).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    objs_dict[key] = obj
        else:
            for key, val in classes.items():
                for obj in self.__session.query(val).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    objs_dict[key] = obj
        return (objs_dict)

    def new(self, obj):
        """Adds the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database
           Create the current database session"""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute
        (self.__session) tips or close() on the class Session tips
        """
        self.__session.close()
