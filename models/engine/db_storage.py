#!/usr/bin/python3
""" DBStorage new engine class module """
from os import getenv
from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """ new engine database """
    __engine = None
    __session = None

    def __init__(self):
        """ init method """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(getenv("HBNB_MYSQL_USER"),
                                              getenv("HBNB_MYSQL_PWD"),
                                              getenv("HBNB_MYSQL_HOST"),
                                              getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if (getenv("HBNB_ENV") == "test"):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on all objects depending on the class name """
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
            for mycls in classes:
                objects = self.__session.query(mycls).all()
                dic = {}
                for obj in objects:
                    key = "{}.{}".format(type(obj).__name__)
                    dic[key] = obj
        else:
            if type(cls) is str:
                cls = eval(cls)
            objects = self.__session.query(cls)
            dic = {}
            for obj in objects:
                key = "{}.{}".format(type(obj).__name__)
                dic[key] = obj
        return dic

    def new(self, obj):
        """ add new object to the session """
        self.__session.add(obj)

    def save(self):
        """ commit all changes of the session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete obj if it's not None """
        self.__session.delete(obj)

    def reload(self):
        """ create tables and initialize session """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
