"""Stay Safe."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session,url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from model import *


app = Flask(__name__)

app.secret_key = "SAFE"

app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=["GET"])
def homepage():
    """Homepage"""
    


    return render_template("homepage.html")


@app.route('/', methods=["POST"])
def save_form_data():
    """Saving input form data into database."""

    #Retrieves data from form
    name = request.form.get("name")
    number = request.form.get("number")
    e_name = request.form.get("e_name")
    e_number = request.form.get("e_number")
    details = request.form.get("activity")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}" 

    #This checks or finds if any of their info are in database
    user = User.query.filter_by(name=name).first()
    user_id = user.user_id

    phone = User_Phone.query.filter_by(number=number).first()
    phone_id = phone.phone_id

    econtact = E_Contact.query.filter_by(e_name=e_name).first()
    e_id = econtact.e_id

    ephone = E_Phone.query.filter_by(e_number=e_number).first()
    ephone_id = ephone.ephone_id

    #Check if name matches the phone number by matching up user_id
    phone_user_id = phone.user_id

    #Check if userid matches econtact userid 
    econ_user_id = econtact.user_id

    #Check if econtactid matches enumber econtact id 
    enum_econ_id = ephone.e_id 

    #If user and phone does not match in database, then add all the information
    if user_id != phone_user_id:

        #Adding new_user first, to get user_id
        new_user = User(name=name)
        db.session.add(new_user)

        #Querying to get user_id
        user = User.query.filter_by(name=name).first()
        user_id = user.user_id

        #Adding number and econtact to get econtact id
        new_number = User_Phone(number=number, user_id=user_id)
        new_econtact = E_Contact(e_name=e_name, user_id=user_id)
        db.session.add(new_number)
        db.session.add(new_econtact)

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id
        # print(e_id)

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone match, but userid and econtact userid doesnt
    elif (user_id == phone_user_id) and (user_id != econ_user_id):

        #Adding econtact to get econtact id
        new_econtact = E_Contact(e_name=e_name, user_id=user_id)
        db.session.add(new_econtact)

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone, user and econtact match but econtact and ephone doesnt
    elif (user_id == phone_user_id) and (user_id == econ_user_id) and (
        e_id != enum_econ_id):

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone, user and econtact, and econtact and ephone match
    elif (user_id == phone_user_id) and (user_id == econ_user_id) and (
        e_id == enum_econ_id):

        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(activity)

        db.session.commit()        




    return redirect('/success')

@app.route('/success')
def succes():

    return render_template("success.html")


if __name__ == "__main__":
    
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
