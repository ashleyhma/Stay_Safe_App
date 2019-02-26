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
# run_with_ngrok(app)

app.secret_key = "SAFE"

app.jinja_env.undefined = StrictUndefined

GOOGLE_KEY = os.getenv('GOOGLE_KEY')


@app.route('/', methods=["GET"])
def homepage():
    """Show homepage with form for user's name and number. If user is already stored
        in session, redirect to default-form"""

    #If there is a session, redirect to default-form
    if 'user_id' in session:
        return redirect('/default-form')
 
    #Else show homepage
    return render_template("index.html")


@app.route('/', methods=["POST"])
def save_name_num():
    """Saving name and num info into database. 
        If name and num already in db, redirect to 'default-form'
        else redirect to 'form'
        add to session. """

    #Grabs data from input form
    name = request.form.get("name")
    number = request.form.get("number")

    #Checks to see if user is already in db
    existing_phone = User_Phone.query.filter_by(number=number).first()


    # Checks if user matches phone in db
    if existing_phone:
        if existing_phone.user.name == name:

            user = User.query.filter_by(name=name).first()
            session["user_id"] = user.user_id

            #If matches, send them to the default form
            return redirect('/default-form')

        #If not, make them try again
        else: 
            flash("This phone is registered to another name, please try again!")
            return redirect("/")
    else:
        flash("We do not have your number registered. Please register!")
        return redirect("/")

@app.route('/check-phone-num.json')
def check_phone_num():

    name = request.values.get("name")
    number = request.values.get("number")
    msg = {}
    # import pdb; pdb.set_trace()

    existing_phone = User_Phone.query.filter_by(number=number).first()

    #Checks if user matches phone in db
    if existing_phone:
        if existing_phone.user.name == name:
            user = User.query.filter_by(name=name).first()
            session["user_id"] = user.user_id
            msg['msg'] = 'okay'

        else: 
            msg['msg']= 'name not with number'
            # flash("This phone is registered to another name, please try again!")
    else:
        msg['msg'] = 'not registered'
        # flash("We do not have your number registered. Please register!")
        
    # print(name)
    # print(number)
    # print(existing_phone)
    # print(existing_phone.user.name)
    return jsonify(msg)

@app.route('/register-form')
def show_registration_form():
    """Show full form for registering a new user and their details. """
    

    return render_template("register_form.html")


@app.route('/default-form')
def show_default_form():
    """Shows part of form for people that has a session/ already been in db. """

    # if 'user_id' not in session:
    #     return redirect('/')

    user_id = session['user_id']

    user = User.query.options(
        db.joinedload('phones')
    ).options(db.joinedload('e_contacts')
    ).options(db.joinedload('activities')
    ).filter_by(user_id=user_id).first()

    e_id = user.e_contacts[-1].e_id
    last_ename = user.e_contacts[-1].e_name
    last_enumber = user.e_contacts[-1].e_phones[-1].e_number
    last_details = user.activities[-1].details
    last_time = user.activities[-1].time
    split_time = last_time.split(":")
    hours = split_time[0]
    minutes = split_time[1]


    return render_template("default_form.html", 
                            last_ename=last_ename,
                            last_enumber=last_enumber,
                            last_details=last_details,
                            hours=hours,
                            minutes=minutes)


@app.route('/change-emergency-contact', methods=['GET'] )
def change_emergency_contact():
    """Show emergency contact change form"""



    return render_template("change_econtact.html")


@app.route('/change-emergency-contact', methods=['POST'])
def reset_emergency_contact():
    """This will either add a phone to the emergency contact or add another 
    emergency contact and number"""

    user_id = session["user_id"]
    user = User.query.get(user_id)

    e_name = request.form.get("ename")
    e_number = request.form.get("enum")


    existing_ephone = E_Phone.query.filter_by(e_number=e_number).first()

    #If they try to add a new name with an existing ephone, tell them to try again
    if existing_ephone:
        flash("This phone number already exists, please try again")
        return redirect("/reset_emergency_contact")

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

@app.route('/check-ec-contact.json')
def check_ec_contact():

    user_id = session["user_id"]
    user = User.query.get(user_id)

    ename = request.values.get("ename")
    enum = request.values.get("enumber")

    existing_ephone = E_Phone.query.filter_by(e_number=e_number).first()

    msg = {}

    if existing_ephone:
        msg['msg'] = 'existing'
    
    return jsonify(msg)


@app.route('/new-user-success', methods=['POST'])
def show_new_user_text():

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

    #Retrieving location from ajax request
    lat = request.values.get("lat")
    lng = request.values.get("lng")
    # user.add_location(lat,lng)

    #Example texts to user and emergency texts
    okay_text = write_okay_text(user_name) 
    check_text = write_ec_text(user_name, e_contact, details, number, lat, lng)

    #Sends the "Are you okay" text at the specific time said in form
    schedule_check_text_time(hours, minutes, user_name, num_for_twilio)

    #Add user_id to check_text table to false because no text received yet
    user.add_check_text(False)


    return render_template("new_user_success.html",
                            user_name=user_name,
                            number=number,
                            e_name=e_contact,
                            e_number=e_number,
                            details=details,
                            datetime_time=datetime_time,
                            okay_text=okay_text,
                            check_text=check_text,
                            GOOGLE_KEY=GOOGLE_KEY,
                            lat=lat,
                            lng=lng)


@app.route('/returning-user-success', methods=['POST'])
def show_returning_user_text():
    """Shows example text to emergency contact"""

    user_id = session['user_id']
    user = User.query.get(user_id)
    user_name = user.name
    phone = User_Phone.query.filter_by(user_id=user_id).first().number
    number = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]

    #Gets the last recorded items in the db FOR RETURNING USER
    last_econtact = E_Contact.query.filter_by(user_id=user_id).order_by(desc(
        E_Contact.e_id)).first()
    last_ename = last_econtact.e_name
    
    #Gets last emergency contact number for above emergency contact
    e_id = last_econtact.e_id
    last_enumber = E_Phone.query.filter_by(e_id=e_id).order_by(desc(
        E_Phone.ephone_id)).first().e_number


    #Retrieves db data from form
    details = request.form.get("details")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    time = f"{hours}:{minutes}"

    #Always add activity, even if it has been used before
    user.add_activity(details, time)

    #Retrieve lat, long and add to database
    # lat = request.form.get("lat")
    # lng = request.form.get("lng")
    # # pos = request.form.get("pos")
    # # results = request.form.get("results")

    # print("\n\n\n")
    # print("LAT", lat)
    # print("LNG", lng)
    # print("pos", pos)
    # print("results", results)
    # user.add_location(lat,lng)
    
    #To show example of texts on html page
    okay_text = write_okay_text(user_name) 
    check_text = write_ec_text(user_name, last_ename, details, number)

    #Changing int time to datetime time for text use
    datetime_time = datetime.time(hours, minutes)

    num_for_twilio = "+1" + phone


    #Sends the "Are you okay" text at the specific time said in form
    schedule_check_text_time(hours, minutes, user_name, num_for_twilio)

    #Add user_id to check_text table to false because no text received yet
    user.add_check_text(False)
    

    return render_template("returning_success.html",
                            user_name=user_name,
                            last_ename=last_ename,
                            last_enumber=last_enumber,
                            details=details,
                            okay_text=okay_text,
                            check_text=check_text,
                            number=number,
                            datetime_time=datetime_time,
                            GOOGLE_KEY=GOOGLE_KEY,
                            )

@app.route('/get-location-data')
def get_js_data():

    user_id = session['user_id']
    user = User.query.get(user_id)

    #Retrieve lat, long and add to database
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    user.add_location(lat,lng)

    print("\n\n\n")
    print("LAT", lat)
    print("LNG", lng)
    print("hellooooo")

    return render_template("data.html",
                            lat=lat,
                            lng=lng)

@app.route('/sms', methods=['GET','POST'])
def sms():
    """Receives texts"""

    # import pdb; pdb.set_trace()

    #Requests the from number and the message
    from_number = request.form['From']
    message_body = request.form['Body']

    # print(from_number)
    # print(message_body)
   
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

    
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    schedule.run_continuously(1)
    app.debug = True

    app.run(port=5000, host='0.0.0.0')






