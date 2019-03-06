# FUNCTIONS TO SCHEDULE TEXTS

import datetime, time, os, schedule, requests
from twilio.rest import Client
from twilio.rest import TwilioRestClient
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from model import *
from flask_sqlalchemy import SQLAlchemy 


#Twilio Account Information
account_sid = os.getenv('TEST_TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TEST_TWILIO_AUTH_TOKEN')
my_number = os.getenv('MY_NUMBER')
twilio_number = os.getenv('TEST_NUMBER')


def write_okay_text(user_name):
    """Writes up a generalized hey, are you okay? text """

    print(account_sid)
    print(auth_token)
    return f"""Hi {user_name}, this is Stay Safe. Hope you are doing okay! If you do not respond within 5 minutes, we will send a text to your emergency contact."""


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
    """Takes inputted time and schedules the send_check_text function. """

    #Changes string to datetime object
    datetime_time = str(datetime.time(hour, minutes)).split(":")
    time = datetime_time[0] + ":" + datetime_time[1]
 
    #Schedules are you okay text
    schedule.every().day.at(time).do(send_check_text, user_name=user_name, number=number).tag('first_text')


def write_ec_text(user_name, e_name, details, number, address=None):
    """Writes up text to send to emergency contact."""

    if address == None:
        return f"""Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, I might have not made it to my destination. Please give me a call at {number}."""  
    else:
        return f"""Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, I might have not made it to my destination. My last location is at {address}. Please give me a call at {number}."""  


def send_ec_text(user_name, e_name, details, number, e_number, address=None):
    """Sends emergency contact text using Twilio."""

    print("Sending Text to Emergency Contact")

    client = Client(account_sid, auth_token)
    text = write_ec_text(user_name, e_name, details, number, address)

    message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=e_number
                        )

    print(text)
    print(message.sid)

    return schedule.CancelJob


def schedule_ec_text_time(hour, minutes, user_name, e_name, details, number, e_number, address):
    """Adds 5 minutes to inputted time from form. Schedules emergency contact text at this time. """

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

    schedule.every().day.at(time).do(send_ec_text, user_name=user_name, 
        e_name=e_name, details=details, number=number, e_number=e_number, 
        address=address)


def change_to_wait_time(hour, minutes):
    """Changes inputted time to 5 minutes after. """


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

    #Current time 
    now = datetime.datetime.now()
    now_hour = now.hour
    now_minute = now.minute
    now_time = str(datetime.time(now_hour, now_minute))

    #Querying all in the check text table that isnt None 
    unchecked_text_queue = Check_Text.query.options(
        db.joinedload('user').joinedload('e_contacts')
    ).options(
        db.joinedload('user').joinedload('activities')
    ).all()

    for check in unchecked_text_queue:
        
        #User info
        user = check.user 
        user_id = user.user_id
        user_name = user.name

        #User phone
        phone = user.phones[-1].number

        #Emergency contact info
        e_name = user.e_contacts[-1].e_name
        e_number = user.e_contacts[-1].e_phones[-1].e_number
        formatted_enum = "+1" + e_number

        #Activity info
        activity = user.activities[-1]
        details = activity.details
        time = activity.time
        split_time = time.split(":")
        hours = int(split_time[0])
        minutes = int(split_time[1])

        #Checks if user allowed location to be sent
        if user.locations:
            address = user.locations[-1].address 
        else: 
            address = None

        #Adds 5 min to check time, but 1 min for TESTING
        changed_wait_time = change_to_wait_time(hours, minutes)

        #Checks if server has received a text from user
        check_status = user.check_texts[-1]
        t_or_f = check_status.true_false

        #Checks if it is the right time
        if changed_wait_time in now_time:

            #If user did not respond, send to emergency contact
            if t_or_f == False:
                schedule_ec_text_time(hours, minutes, user_name, e_name, details, 
                    phone, formatted_enum, address)  

                #delete row in db
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




