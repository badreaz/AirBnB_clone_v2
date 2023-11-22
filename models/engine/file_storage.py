#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            objs = {}
            if type(cls) is str:
                cls = eval(cls)
            for k, v in self.__objects.items():
                if type(v) is cls:
                    objs[k] = v
            return objs
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w', encoding="utf-8") as f:
            temp = {}
            for key, val in self.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                temp = json.load(f)
                for val in temp.values():
                    class_name = val['__class__']
                    del val['__class__']
                    self.new(classes[class_name](**val))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        if obj is None:
            return
        del self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)]
