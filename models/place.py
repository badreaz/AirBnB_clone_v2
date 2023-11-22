#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from os import getenv
from models.base_model import Base, BaseModel
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

metadata = Base.metadata
place_amenity = Table("place_amenity", metadata,
        Column("place_id", String(60), ForeignKey("places.id"), primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"), primary_key=True, nullable=False)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Reivew", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    @property
    def reviews(self):
        """ returns the list of Review instances with place_id
        equals to the current place.id """
        review = []
        for ins in models.storage.all(Review).values():
            if self.id == ins.place_id:
                review.append(ins)
        return review

    @property
    def amenities(self):
        """ returns the list of Amenity instances based on
        an attribute amenity_ids that contains all Amenity.id
        linked to the place """
        amenity = []
        for ins in models.storage.all(Amenity).values():
            if ins.id in self.amenity_ids:
                amenity.append(ins)
        return amenity

    @amenities.setter
    def amenities(self, obj=None):
        """ handles append method for adding an Amenity.id
        to the attribute amenity_ids """
        if type(obj) == Amenity and obj.id not in self.amenity_ids:
            self.amenity_ids.append(obj.id)