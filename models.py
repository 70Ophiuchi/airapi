from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.elements import collate
from sqlalchemy.sql.expression import column

database_name = "Airplanes"
database_path = 'postgres://bboafxezreihwv:a8b57bcf9ee1f036b78377d5a0adea0fe257fa182db47cba22c4518997a43f9f@ec2-3-209-65-193.compute-1.amazonaws.com:5432/dbibhl32k6odde'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()


class Airplanes(db.Model):  
    __tablename__ = 'airplanes'

    id = Column(Integer, primary_key=True)
    airplane_name = Column(String)
    airplane_manufacturer = Column(String)
    built_in = Column(String)

    def __init__(self, name, manufacturer, built_in):
        self.name = name
        self.manufacturer = manufacturer
        self.built_in = built_in

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'airplane_name': self.name,
        'airplane_manufacturer': self.manufacturer,
        'airplane_built_in': self.built_in
        }

class Airports(db.Model):
    __tablename__ = 'airports'

    id = Column(Integer, primary_key=True)
    airport_name = Column(String)
    airport_code = Column(String)
    airport_country = Column(String)
    
    def __init__(self, name, code, country):
        self.name = name
        self.code = code
        self.country = country

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'airport_name': self.name,
        'airport_code': self.code,
        'airport_country': self.country
        }