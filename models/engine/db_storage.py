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
        from sqlalchemy import sessionmaker
        objs_dict = {}
        self.__session = sessionmaker(bind=self.__engine)()
        #session = self.__session
        if cls is not None:
            objs = self.__session.query(cls)
        else:
            objs = self.__session.query().all()

        for obj in objs:
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
        self.__session = scoped_session(session)
