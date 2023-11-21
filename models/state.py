#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import Base, BaseModel
from models.storage import storage
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    @property
    def cities(self):
        """ returns a list of cities """
        city = []
        for ins in storage.all(City).values():
            if self.id == ins.state_id:
                city.append(ins)
        return city
