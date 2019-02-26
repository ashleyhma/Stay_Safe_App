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

    def check_econtact(self, econtact):
        contacts = [name.e_name for name in self.e_contacts]
        return econtact in contacts 

    def add_econtact(self, e_name):
        econtact = E_Contact(e_name=e_name)
        self.e_contacts.append(econtact)
        
        db.session.add(self)
        db.session.commit()


    def add_activity(self, details, time):
        activity = Activity(details=details, time=time)
        self.activities.append(activity)

        db.session.add(self)
        db.session.commit()

    def add_check_text(self, true_false):
        check_text = Check_Text(true_false=true_false)
        self.check_texts.append(check_text)

        db.session.add(self)
        db.session.commit()

    def add_location(self, lat, lng):
        location = Location(lat=lat, lng=lng)
        self.locations.append(location)

        db.session.add(self)
        db.session.commit()

    def __repr__(self):

        return f"<User={self.name}, id={self.user_id} >"


class User_Phone(db.Model):
    """User phone numbers. """

    __tablename__ = "phones"

    phone_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    number = db.Column(db.String(10), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref="phones")

    def __repr__(self):

        return f"<Phone={self.number}, id={self.phone_id}, user_id={self.user_id}>"


class E_Contact(db.Model):
    """In Case of Emergency: Emergency contacts. """

    __tablename__ = "e_contacts"

    e_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    e_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User",
                            backref="e_contacts")

    def check_ephone(self, e_number):
        numbers = [ephone.e_number for ephone in self.e_phones]
        return e_number in numbers

    def add_enumber(self, e_number):
        phone = E_Phone(e_number=e_number)
        self.e_phones.append(phone)

        db.session.add(self)
        db.session.commit() 

    def __repr__(self):

        return f"<ICE={self.e_name}, id={self.e_id}, user_id={self.user_id}>"


class E_Phone(db.Model):
    """Emergency contact phone numbers. """

    __tablename__ = "e_phones"

    ephone_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    e_number = db.Column(db.String(10), nullable=False, unique=True)
    e_id = db.Column(db.Integer, db.ForeignKey('e_contacts.e_id'))

    e_contacts = db.relationship("E_Contact",
                            backref="e_phones")

    def __repr__(self):

        return f"<EPhone={self.e_number}, id={self.ephone_id}, e_id={self.e_id}>"

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

        return f"<Activity={self.details}, user_id={self.user_id}>"

class Check_Text(db.Model):
    """Storing if texts are received."""

    __tablename__ = "check_texts"

    text_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    true_false = db.Column(db.Boolean, nullable=False)

    user = db.relationship("User",
                            backref="check_texts")

    def __repr__(self):

        return f"<Id={self.text_id} user_id={self.user_id} T/F={self.true_false}>"


class Location(db.Model):
    """Storing location of user from Google Maps API."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)


    user = db.relationship("User",
                            backref="locations")


    def __repr__(self):

        return f"<ID={self.location_id} user_id={self.user_id} lat={self.lat} long={self.lng}"





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

