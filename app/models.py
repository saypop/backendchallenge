# app/models.py

from app import db
from flask import jsonify


class Cars(db.Model):
    """This class defines the cars table"""

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(25), nullable=False)
    model = db.Column(db.String(25), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    currently_with = db.Column(db.String(256))

    def __init__(self, make, model, year, currently_with=None):
        self.make = make
        self.model = model
        self.year = year
        self.currently_with = currently_with

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cars.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Car: {}, {}, {}, {}>".format(self.make, self.model, self.year, self.currently_with)


class Branches(db.Model):
    """This class defines the branches table"""

    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(25), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)

    def __init__(self, city, postcode):
        self.city = city
        self.postcode = postcode

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Branches.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "{ " + "type: branch, id: {}, city: {}, postcode: {} ".format(self.id, self.city, self.postcode) + " }"


class Drivers(db.Model):
    """This class defines the drivers table"""

    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(10), nullable=False)

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Drivers.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "{ " + "type: driver, id: {}, name: {}, dob: {} ".format(self.id, self.name, self.dob) + " }"
