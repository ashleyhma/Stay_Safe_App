"""Stay Safe."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from model import *
from schedule_texts import *
import datetime, time, googlemaps
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse 


app = Flask(__name__)
app.secret_key = "SAFE"
app.jinja_env.undefined = StrictUndefined
GOOGLE_KEY = os.getenv('GOOGLE_KEY')

@app.route('/', methods=['GET', 'POST'])
def homepage():
    """Show homepage with form for user's name and number.
    
    If user is already stored in session, redirect to default-form.
    """

    #If there is a session, redirect to default-form
    if 'user_id' in session:
        return redirect('/default-form')
 
    #Else show homepage
    return render_template('index.html')


@app.route('/check-phone-num.json')
def check_phone_num():
    """Receives and sends data to react. 
    
    Checks if user has already been in the database.
    """

    name = request.values.get("name")
    number = request.values.get("number")
    msg = ''
    # import pdb; pdb.set_trace()

    existing_phone = User_Phone.query.filter_by(number=number).first()

    #Checks if user matches phone in db
    if existing_phone:
        if existing_phone.user.name == name:
            session["user_id"] = existing_phone.user.user_id
            msg = 'okay'

        else: 
            msg = 'name not with number'
            # flash("This phone is registered to another name, please try again!")
    else:
        msg = 'not registered'
        # flash("We do not have your number registered. Please register!")
        
    return jsonify({ 'msg': msg })

@app.route('/register-form')
def show_registration_form():
    """Show full form for registering a new user and their details. """

    return render_template("register_form.html")

@app.route('/default-form')
def show_default_form():
    """Shows part of form for people that has a session/ already been in db. """

    return render_template("default_form.html")

@app.route('/default-form.json')
def send_default_form_data():
    """Sends data to react"""

    if session.get('user_id'):
        user_id = session['user_id']

        user = User.query.options(
            db.joinedload('phones')
        ).options(db.joinedload('e_contacts')
        ).options(db.joinedload('activities')
        ).get(user_id)

        last_time = user.activities[-1].time
        hours, minutes = last_time.split(":")

        last_data = {
            "e_id": user.e_contacts[-1].e_id, 
            "last_ename": user.e_contacts[-1].e_name,
            "last_enumber": user.e_contacts[-1].e_phones[-1].e_number,
            "last_details": user.activities[-1].details,
            "last_hours": hours,
            "last_mins": minutes
        }

        return jsonify(last_data)


@app.route('/change-emergency-contact', methods=['GET', 'POST'] )
def change_emergency_contact():
    """Show emergency contact change form"""

    return render_template("change_econtact.html")


@app.route('/change-emergency-contact', methods=['POST'])
def reset_emergency_contact():
    """This will either add a phone to the emergency contact or add another emergency contact and number"""

    user_id = session["user_id"]
    user = User.query.get(user_id)

    e_name = request.form.get("ename")
    e_number = request.form.get("enum")

    existing_ephone = E_Phone.query.filter_by(e_number=e_number).first()

    #If they try to add a new name with an existing ephone, tell them to try again
    if existing_ephone:
        flash("This phone number already exists, please try again")
        return redirect("/change-emergency-contact")

    #Else if the user has this econtact, add the number to this econtact
    elif user.check_econtact(e_name): 
        e_contact = E_Contact.query.filter_by(e_name=e_name).first()
        e_contact.add_enumber(e_number)

    #If everything is new, add both
    else: 
        user.add_econtact(e_name)
        e_contact = E_Contact.query.filter_by(e_name=e_name).first()
        e_contact.add_enumber(e_number)

    return redirect('/default-form')

@app.route('/check-ec-contact.json', methods=['GET', 'POST'])
def check_ec_contact():

    user_id = session["user_id"]
    user = User.query.get(user_id)

    ename = request.form.get("ename")
    enumber = request.form.get("enumber")

    existing_ephone = E_Phone.query.filter_by(e_number=enumber).first()

    if existing_ephone:
        return jsonify({'msg': 'This phone number already exists, please try again'})

    e_contact = E_Contact.query.filter_by(e_name=e_name).first()
    e_contact.add_enumber(e_number)

    if not user.check_econtact(e_name): 
        user.add_econtact(e_name)
    
    phone_numbers = [ phone.e_number for phone in e_contact.e_phones ]
    return jsonify({'name': e_contact.name, 'numbers': phone_numbers})


@app.route('/new-user-success', methods=['POST'])
def show_new_user_text():
    """Takes in the register form information.

    Displays the information submitted by the user.
    """

    #Grabs data from input form
    name = request.form.get("name")
    number = request.form.get("number")
    

    #Create user and add to db
    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    #Add their phone number to db
    user.add_number(number)

    #Create a session with user_id
    session["user_id"] = user.user_id

    #Retrieves data from form
    e_name = request.form.get("e_name")
    e_number = request.form.get("e_number")
    details = request.form.get("details")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}" 

    formatted_num = number[:3] + "-" + number[3:6] + "-" + number[6:]
    num_for_twilio = "+1" + number
    
    user.add_econtact(e_name)
    e_name = E_Contact.query.filter_by(e_name=e_name).first()
    e_name.add_enumber(e_number)
    user.add_activity(details, time)
    user_name = user.name
    e_contact = e_name.e_name

    #Changing int time to datetime time for text use
    datetime_time = datetime.time(hours, minutes)

    # #Retrieves address from db
    # address = user.locations[-1].address
    address = None

    #Example texts to user and emergency texts
    okay_text = write_okay_text(user_name) 
    check_text = write_ec_text(user_name, e_contact, details, number, address)

    #Sends the "Are you okay" text at the specific time said in form
    schedule_check_text_time(hours, minutes, user_name, num_for_twilio)

    #Add user_id to check_text table to false because no text received yet
    user.add_check_text(False)


    return render_template("success.html",
                            user_name=user_name,
                            number=number,
                            e_name=e_contact,
                            e_number=e_number,
                            details=details,
                            datetime_time=datetime_time,
                            okay_text=okay_text,
                            check_text=check_text,
                            GOOGLE_KEY=GOOGLE_KEY,
                            address=address
                            )



@app.route('/returning-user-success.json')
def get_form_data():
    """Takes in information from the main form. 
    
    Displays information submitted by user.
    """

    user_id = session['user_id']
    user = User.query.options(
        db.joinedload('phones')
    ).options(db.joinedload('e_contacts')
    ).options(db.joinedload('activities')
    ).get(user_id)

    user_name = user.name
    phone = user.phones[-1].number,
    number = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]

    #Gets the last recorded items in the db FOR RETURNING USER
    e_id = user.e_contacts[-1].e_id
    last_ename = user.e_contacts[-1].e_name
    last_enumber = user.e_contacts[-1].e_phones[-1].e_number

    #Retrieves db data from form
    details = request.form.get("details")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}"
    
    # #Retrieves address from db
    # address = user.locations[-1].address
    address = None

    #Always add activity, even if it has been used before
    user.add_activity(details, time)
    
    #To show example of texts on html page
    okay_text = write_okay_text(user_name) 
    check_text = write_ec_text(user_name, last_ename, details, number, address)

    #Changing int time to datetime time for text use
    datetime_time = datetime.time(hours, minutes)

    num_for_twilio = "+1" + phone

    #Sends the "Are you okay" text at the specific time said in form
    schedule_check_text_time(hours, minutes, user_name, num_for_twilio)

    #Add user_id to check_text table to false because no text received yet
    user.add_check_text(False)

    form_data = {
            "user_name": user.name,
            "number": user.phones[-1].number,
            "e_name": user.e_contacts[-1].e_name,
            "e_number": user.e_contacts[-1].e_phones[-1].e_number,
            "details": user.activities[-1].details,
            "datetime_time": datetime_time,
            "okay_text": okay_text,
            "check_text": check_text,
            "GOOGLE_KEY": GOOGLE_KEY,
            "address": address
        }
    
    return jsonify(form_data)

@app.route('/returning-user-success', methods=['POST'])
def show_returning_user_text():

    user_id = session['user_id']
    user = User.query.get(user_id)
    user_name = user.name
    phone = User_Phone.query.filter_by(user_id=user_id).first().number
    number = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]

    #Gets the last recorded items in the db FOR RETURNING USER
    e_id = user.e_contacts[-1].e_id
    last_ename = user.e_contacts[-1].e_name
    last_enumber = user.e_contacts[-1].e_phones[-1].e_number


    #Retrieves db data from form
    details = request.form.get("details")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}"

    # #Retrieves address from db
    # address = user.locations[-1].address
    address = None

    #Always add activity, even if it has been used before
    user.add_activity(details, time)
    
    #To show example of texts on html page
    okay_text = write_okay_text(user_name) 
    check_text = write_ec_text(user_name, last_ename, details, number, address)

    #Changing int time to datetime time for text use
    datetime_time = datetime.time(hours, minutes)

    num_for_twilio = "+1" + phone


    #Sends the "Are you okay" text at the specific time said in form
    schedule_check_text_time(hours, minutes, user_name, num_for_twilio)

    #Add user_id to check_text table to false because no text received yet
    user.add_check_text(False)


    

    return render_template("success.html",
                            user_name=user_name,
                            number=number,
                            e_name=last_ename,
                            e_number=last_enumber,
                            details=details,
                            datetime_time=datetime_time,
                            okay_text=okay_text,
                            check_text=check_text,
                            GOOGLE_KEY=GOOGLE_KEY,
                            address=address
                            )


@app.route('/get-location-data')
def get_gmaps_data():
    """Retrieves latitude and longitude from google maps website.
    
    Translates latitude and longitude into a street address and saves all three into database."""
    gmaps = googlemaps.Client(os.environ.get('GOOGLE_KEY'))
    user_id = session['user_id']
    user = User.query.get(user_id)

    #Retrieve lat, long and add to database
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if lat:
        result = gmaps.reverse_geocode(latlng=(lat, lng))
        address = result[0]['formatted_address']

        user.add_location(lat, lng, address)
    
    print("\n\n")
    print("LAT", lat)
    print("LNG", lng)
    print("\n\n")
    return render_template("data.html",
                            lat=lat,
                            lng=lng,
                            address=address)


@app.route('/sms', methods=['GET','POST'])
def sms():
    """Receives texts"""

    #Requests the from number and the message
    from_number = request.form['From']
    message_body = request.form['Body']
   
    user = db.session.query(User).join(User_Phone).filter(User_Phone.number == from_number[2:]).first()
    user_id = user.user_id

    #Gets status of object. "True" or "False" if its been received
    check_status = Check_Text.query.filter_by(user_id=user_id).first()

    #change db row to true 
    check_status.true_false = True
    db.session.commit()

    resp = MessagingResponse()
    resp.message("Glad you are okay! Thank you for using Stay Safe.")
    return str(resp)


@app.route('/logout')
def logout():
    """Log out/ delete session."""

    del session["user_id"]
    return redirect("/")
        


if __name__ == "__main__":

    schedule.every(20).seconds.do(check_time)

    connect_to_db(app)

    DebugToolbarExtension(app)

    schedule.run_continuously(1)
    
    app.jinja_env.auto_reload = app.debug
    app.debug = True
    app.config['TESTING'] = True

    app.run(port=5000, host='0.0.0.0', debug=True)






