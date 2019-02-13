"""Models and database functions for Stay Safe App"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##########################################################################

# Model definitions 

class User(db.Model):
    """Users of Stay Safe Website. """

    __tablename__ = "users"


    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def check_phone(self, number):
        numbers = [phone.number for phone in self.phones]
        return number in numbers

    def add_number(self, number):
        phone = User_Phone(number=number)
        self.phones.append(phone)

        db.session.add(self)
        db.session.commit() 

    def __repr__(self):

        return f"<User= {self.name} id={self.user_id} >"


class User_Phone(db.Model):
    """User phone numbers. """

    __tablename__ = "phones"

    phone_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.String(10), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref="phones")

    def __repr__(self):

        return f"<Phone= {self.number} id={self.phone_id} user_id={self.user_id}>"


class E_Contact(db.Model):
    """In Case of Emergency: Emergency contacts. """

    __tablename__ = "e_contacts"

    e_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    e_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref="e_contacts")

    def __repr__(self):

        return f"<ICE= {self.e_name} id={self.e_id} user_id={self.user_id}>"


class E_Phone(db.Model):
    """Emergency contact phone numbers. """

    __tablename__ = "e_phones"

    ephone_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    e_number = db.Column(db.String(10), nullable=False)
    e_id = db.Column(db.Integer, db.ForeignKey('e_contacts.e_id'))

    e_contacts = db.relationship("E_Contact",
                            backref="e_phones")

    def __repr__(self):

        return f"<EPhone={self.e_number} id={self.ephone_id} e_id={self.e_id}>"

class Activity(db.Model):
    """User's activities. """

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    details = db.Column(db.String(300), nullable = True)
    time = db.Column(db.String(15), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    

    user = db.relationship("User",
                            backref="activities")

    def __repr__(self):

        return f"<Activity = {self.details} user_id={self.user_id}>"



##########################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///contacts'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    # db.create_all()
    print("Connected to DB.")

