"""Stay Safe."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session,url_for)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from flask_debugtoolbar import DebugToolbarExtension

from model import *


app = Flask(__name__)

app.secret_key = "SAFE"

app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=["GET"])
def homepage():
    """Show homepage with form for user's name and number. If user is already stored
        in session, redirect to some-form"""

    #If there is a session, redirect to some-form
    if 'user_id' in session:
        return redirect('/some-form')
 
    #Else show homepage
    return render_template("homepage.html")


@app.route('/', methods=["POST"])
def save_name_num():
    """Saving name and num info into database. 
        If name and num already in db, redirect to 'some-form'
        else redirect to 'form'
        add to session. """

    #Grabs data from input form
    name = request.form.get("name")
    number = request.form.get("number")

    #Checks to see if user is already in db
    existing_phone = User_Phone.query.filter_by(number=number).first()


    #Checks if user matches phone in db
    if existing_phone:
        if existing_phone.user.name == name:

            user = User.query.filter_by(name=name).first()
            session["user_id"] = user.user_id

            return redirect('/some-form')

        else: 
            flash("This phone is registered to another name, please try again!")
            return redirect("/")

    else:

        #Create user and add to db
        user = User(name=name)
        db.session.add(user)
        db.session.commit()

        #Add their phone number to db
        user.add_number(number)

        #Create a session with user_id
        session["user_id"] = user.user_id

        return render_template("form.html")
 
    

@app.route('/form', methods=["GET"])
def show_full_form():
    """Show full form for creating new user and their details. """

    #if there is no session, redirect to homepage
    if 'user_id' not in session:
        return redirect('/')

    return render_template("form.html")



@app.route('/form', methods=["POST"])
def save_form():
    """Saves form information into database. """
  
    #Retrieves data from form
    e_name = request.form.get("e_name")
    e_number = request.form.get("e_number")
    details = request.form.get("details")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}" 

    user = User.query.get(session['user_id'])
    
    user.add_econtact(e_name)
    e_name = E_Contact.query.filter_by(e_name=e_name).first()
    print(e_name)
    e_name.add_enumber(e_number)
    user.add_activity(details, time)

    return redirect('/success')

@app.route('/some-form', methods=['GET'])
def show_some_form():
    """Shows part of form for people that has a session/ already been in db. """

    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']
    e_id = E_Contact.query.filter_by(user_id=user_id).order_by(desc(
        E_Contact.e_id)).first().e_id

    #Gets the last recorded items in the db
    last_ename = E_Contact.query.filter_by(user_id=user_id).order_by(desc(
        E_Contact.e_id)).first().e_name
    last_enumber = E_Phone.query.filter_by(e_id=e_id).order_by(desc(
        E_Phone.ephone_id)).first().e_number
    last_details = Activity.query.filter_by(user_id=user_id).order_by(desc(
        Activity.activity_id)).first().details
    last_time = Activity.query.filter_by(user_id=user_id).order_by(desc(
        Activity.activity_id)).first().time

    print("\n\n\n\n")
    print(last_enumber)
    print("ENUMBER")

    return render_template("some_form.html", 
                            last_ename=last_ename,
                            last_enumber=last_enumber,
                            last_details=last_details,
                            last_time=last_time)



@app.route('/some-form', methods=['POST'])
def save_some_form():
    """Shows form of people that has a session """

    #Retrieves data from form
    e_name = request.form.get("e_name")
    e_number = request.form.get("e_number")
    details = request.form.get("activity")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}"   



    # if user.check_econtact(e_name) == false:
    #     user.add_econtact(e_name)
    

    return redirect('/success')



@app.route('/success')
def succes():
    """Shows example text to emergency contact"""

    return render_template("success.html")

@app.route('/logout')
def logout():
    """Log out/ delete session."""

    del session["user_id"]
    return redirect("/")


if __name__ == "__main__":
    
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
