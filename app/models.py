# app/models.py

from app import db


class Cars(db.Model):
    """This class defines the cars table """

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(256), nullable=False, unique=True)
    model = db.Column(db.String(256), nullable=False)
    year = db.Column(db.Integer)

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

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
        return "<Car: {}".format(self.make, self.model, self.year)


class Branches(db.Model):
    """This class defines the branches table"""

    __tablename__ = 'branches'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    postcode = db.Column(db.String, nullable=False)

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
        return "<Branch: {}".format(self.city, self.postcode)
