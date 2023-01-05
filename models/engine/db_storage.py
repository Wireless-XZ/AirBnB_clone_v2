""" db_storage Module"""
class DBStorage:
    """Class definition"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the class instance"""
        from sqlalchemy import create_engine
        from os import getenv
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """Queries on the current database"""
        from console import HBNBCommand
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        objs_dict = {}
        if cls is not None:
            if cls in HBNBCommand.classes.keys():
                for obj in self.__session.query(cls).all():
                    objs_dict.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        else:
            for key, val in HBNBCommand.classes.items():
                for obj in self.__session.query(val).all():
                    objs_dict.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        return (objs_dict)

    def new(self, obj):
        """Adds the object to the current database session"""
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
        from models.base_model import Base
        from sqlalchemy.orm import sessionmaker, scoped_session
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)()
