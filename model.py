"""Models and database functions for Stay Safe App"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy

##########################################################################

# Model definitions 

class User(db.Model):
    """Users of Stay Safe Website. """

    __tablename__ = "users"




class User_Phone(db.Model):
    """User phone numbers. """

    __tablename__ = "phones"




class Emgy_Con(db.Model):
    """In Case of Emergency: Emergency contacts. """

    __tablename__ = "econtacts"




class EC_Phone(db.Model):
    """Emergency contact phone numbers. """

    __tablename__ = "ecphones"



class Activity(db.Model):
    """User's activities. """

    __tablename__ = "activities"











def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///contacts'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

    