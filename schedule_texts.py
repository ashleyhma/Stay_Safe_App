# FUNCTIONS TO SCHEDULE 

import datetime
import time
from pytz import timezone
import pytz
import schedule
from twilio.rest import Client
from twilio.rest import TwilioRestClient
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from model import *
from flask_sqlalchemy import SQLAlchemy 

#Twilio Account Information
account_sid = os.getenv('TEST_TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TEST_TWILIO_AUTH_TOKEN')
my_number = os.getenv('MY_NUMBER')
twilio_number = os.getenv('TEST_NUMBER')

""" RUNS A JOB ONLY ONCE 

def job_that_executes_once():
    # Do some work ...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)

https://schedule.readthedocs.io/en/stable/faq.html#how-can-i-run-a-job-only-once """

def write_okay_text(user_name):
    """Writes up a generalized hey, are you okay? text """

    print(account_sid)
    print(auth_token)
    return f"""Hi {user_name}, this is Stay Safe. Hope you are doing okay! If you do 
    not respond within 5 minutes, we will send a text to your emergency contact."""



def send_check_text(user_name, number):
    """Sends okay_text when it is the specified time using Twilio."""

    print("Sending text to User")

    client = Client(account_sid, auth_token)
    text = write_okay_text(user_name)

    message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=number
                        )

    print(client)
    print(text)
    print(message.sid)


    return schedule.CancelJob


def schedule_check_text_time(hour, minutes, user_name, number):
    """takes inputted time and keeps checking time until the right time to call 
    the text function. """

    #Changes string to datetime object
    datetime_time = str(datetime.time(hour, minutes)).split(":")
    time = datetime_time[0] + ":" + datetime_time[1]
    print(time)
 
    #Schedules are you okay text
    schedule.every().day.at(time).do(send_check_text, user_name=user_name, number=number).tag('first_text')


def write_ec_text(user_name, e_name, details, number, lat=None, lng=None):
    """Writes up specific text to emergency contact."""

    if lat == None:
        return f"""Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, 
        I might have not made it to my destination. Please give me a call at {number}."""  
    else:
        return f"""Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, 
        I might have not made it to my destination. My last location is at latitutde: {lat}, 
        longitude: {lng}. Please give me a call at {number}."""  


def send_ec_text(user_name, e_name, details, number, e_number, lat=None, lng=None):
    """Sends emergency contact text using Twilio."""

    print("Sending Text to Emergency Contact")

    client = Client(account_sid, auth_token)
    text = write_ec_text(user_name, e_name, details, number, lat, lng)

    message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=e_number
                        )

    print(text)
    print(message.sid)

    return schedule.CancelJob


def schedule_ec_text_time(hour, minutes, user_name, e_name, details, number, 
    e_number, lat=None, lng=None):
    """Check for the time that the emergency contact text will be sent out"""

    # #Adding 5 minutes to check time
    # wait_min = minutes + 6 


    # if wait_min == 61:
    #     later_min = 1
    #     u_hour += 1
    # elif wait_min == 62:
    #     later_min = 2
    #     u_hour += 1 
    # elif wait_min == 63:
    #     later_min = 3
    #     u_hour += 1
    # elif wait_min == 64:
    #     later_min = 4
    #     u_hour += 1 
    # elif wait_min == 65:
    #     later_min = 5
    #     u_hour += 1 
    # elif wait_min == 66:
    #     later_min = 6
    #     u_hour += 1 
    # else:
    #     later_min = wait_min


    #FOR TEST: Adding 2 min to schedule time
    wait_min = minutes + 2 

    if wait_min == 58:
        later_min = 0
        hour += 1 
    elif wait_min == 59:
        later_min = 1
        hour += 1 
    elif wait_min == 60:
        later_min = 2
        hour += 1
    else:
        later_min = wait_min

    datetime_time = str(datetime.time(hour, later_min)).split(":")
    time = datetime_time[0] + ":" + datetime_time[1]
    print(time)

    schedule.every().day.at(time).do(send_ec_text, user_name=user_name, 
        e_name=e_name, details=details, number=number, e_number=e_number, 
        lat=lat, lng=lng)



def change_to_wait_time(hour, minutes):
    """Change pacific time to utc time"""


    # #Adding 5 minutes to check time
    # wait_min = minutes + 5 

    # if wait_min == 61:
    #     later_min = 1
    #     u_hour += 1
    # elif wait_min == 62:
    #     later_min = 2
    #     u_hour += 1 
    # elif wait_min == 63:
    #     later_min = 3
    #     u_hour += 1
    # elif wait_min == 64:
    #     later_min = 4
    #     u_hour += 1 
    # elif wait_min == 65:
    #     later_min = 5
    #     u_hour += 1 
    # else:
    #     later_min = wait_min


    #FOR TEST: Adding 1 min to check time
    wait_min = minutes + 1 


    if wait_min == 60:
        later_min = 0
        hour += 1 
    elif wait_min == 61:
        later_min = 1
        hour += 1 
    else:
        later_min = wait_min


    datetime_time = str(datetime.time(hour, later_min)).split(":")
    time = datetime_time[0] + ":" + datetime_time[1]
    # print(time)
    return time
            



def check_time():
    """Checks if it is the right time (5 min after the first text sent)
        If it the value in db is false, then schedule emergency contact text."""

    print("checking...")
    print(schedule.jobs)

    #RIGHT NOW's TIME 
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    now_time = str(datetime.time(now_hour, now_minute))

    #Querying everything in the check text table that isnt None 
    unchecked_text_queue = Check_Text.query.options(
        db.joinedload('user').joinedload('e_contacts')
    ).options(
        db.joinedload('user').joinedload('activities')
    ).all()



    for check in unchecked_text_queue:
    # while unchecked_text_queue:
        #retrieve info for everyone in queue
        
        user = check.user 
        user_id = user.user_id
        user_name = user.name

        # phone = User_Phone.query.filter_by(user_id=user_id).first().phone
        phone = user.phones[-1].number

        # e_name = E_Contact.query.filter_by(user_id=user_id).order_by(desc(
        # E_Contact.e_id)).first().e_name
        e_name = user.e_contacts[-1].e_name
        e_number = user.e_contacts[-1].e_phones[-1].e_number
        formatted_enum = "+1" + e_number

        # details = Activity.query.filter_by(user_id=user_id).order_by(desc(
        # Activity.activity_id)).first().details
        activity = user.activities[-1]
        details = activity.details

        #retrieve each user's last 'time'
        # time = Activity.query.filter_by(user_id=user_id).order_by(desc(Activity.activity_id)).first().time
        time = activity.time
        split_time = time.split(":")
        hours = int(split_time[0])
        minutes = int(split_time[1])

        if user.locations:
            lat = user.locations[-1].lat 
            lng = user.locations[-1].lng 
        else: 
            lat = None
            lng = None

        #Add 5 min to check time, but 1 min for TESTING
        changed_wait_time = change_to_wait_time(hours, minutes)

        # check_status = Check_Text.query.filter_by(user_id=user_id).first()
        check_status = user.check_texts[-1]
        
        t_or_f = check_status.true_false


         #If it is the right time, then clear scheduler
        if changed_wait_time in now_time:
            # print("\n\n\n\n")
            # print("CHANGED TIME", changed_wait_time)
            # print("NOW",now_time)
            # print("T OR F", t_or_f)
            # schedule.clear('first_text')
            #If user did not respond, send to emergency contact
            if t_or_f == False:
                # print("AFTER, T OR F", t_or_f)
                schedule_ec_text_time(hours, minutes, user_name, e_name, details, 
                    phone, formatted_enum, lat, lng)  

                #delete row
                Check_Text.query.filter_by(user_id=user_id).delete()
                db.session.commit()
                break
            #if they did respond, delete their row
            else:
                #delete row
                Check_Text.query.filter_by(user_id=user_id).delete()
                db.session.commit()
            



if __name__ == "__main__":

    schedule.run_continuously(1)




