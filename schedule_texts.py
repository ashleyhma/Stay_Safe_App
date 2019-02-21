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

#Twilio Account Information
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
my_number = os.getenv('MY_NUMBER')
twilio_number = os.getenv('TWILIO_NUMBER')

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
    return f"Hi {user_name}, this is Stay Safe. Hope you are doing okay! If you do not respond within 5 minutes, we will send a text to your emergency contact."



def send_check_text(user_name):
    """Sends okay_text when it is the specified time using Twilio."""

    print("Sending text to User")

    client = Client(account_sid, auth_token)
    text = write_okay_text(user_name)

    message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=my_number
                        )

    print(client)
    print(text)
    print(message.sid)


    # return schedule.CancelJob


def schedule_check_text_time(hour, minutes, user_name):
    """takes inputted time and keeps checking time until the right time to call 
    the text function. """

    utc_hour = hour + 8

    if utc_hour == 24:
        u_hour = 0
    elif utc_hour == 25:
        u_hour = 1
    elif utc_hour == 26:
        u_hour = 2
    elif utc_hour == 27:
        u_hour = 3
    elif utc_hour == 28:
        u_hour = 4
    elif utc_hour == 29:
        u_hour = 5
    elif utc_hour == 30:
        u_hour = 6
    elif utc_hour == 31:
        u_hour = 7
    else:
        u_hour = utc_hour

    utc_time = str(datetime.time(u_hour, minutes)).split(":")
    time = utc_time[0] + ":" + utc_time[1]
    print(time)
 
    # utc_offset = 8

    # todays = datetime.datetime.now()
    # todays_date = str(datetime.datetime.now().date())

    # pacific_time = datetime.datetime.strptime(time, '%H:%M')

    # pacific_time = datetime.time(hours, minutes)

    # result_utc_datetime = pacific_time + datetime.timedelta(hours=utc_offset)
    # result_utc_datetime = datetime.combine(pacific_time + timedelta(hours=8))
    # print(pacific_time)
    # x = datetime.timedelta(hours=utc_offset)
    # print(pacific_time + x)
    # print(result_utc_datetime)

    # print(result_utc_datetime)

    schedule.every().day.at(time).do(send_check_text, user_name=user_name)



def write_ec_text(user_name, e_name, details, number):
    """Writes up specific text to emergency contact."""

    return f"Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, I might have not made it to my destination. Please give me a call at {number}."  




def send_ec_text(user_name, e_name, details, number):
    """Sends emergency contact text using Twilio."""

    print("Sending Text to Emergency Contact")

    client = Client(account_sid, auth_token)
    text = write_ec_text(user_name, e_name, details, number)

    message = client.messages.create(
                        body=text,
                        from_=twilio_number,
                        to=my_number
                        )

    print(text)
    print(message.sid)

    # return schedule.CancelJob


def schedule_ec_text_time(hour, minutes, user_name, e_name, details, number):
    """Check for the time that the emergency contact text will be sent out"""

    #Pacific to UTC 
    utc_hour = hour + 8 

    if utc_hour == 24:
        u_hour = 0
    elif utc_hour == 25:
        u_hour = 1
    elif utc_hour == 26:
        u_hour = 2
    elif utc_hour == 27:
        u_hour = 3
    elif utc_hour == 28:
        u_hour = 4
    elif utc_hour == 29:
        u_hour = 5
    elif utc_hour == 30:
        u_hour = 6
    elif utc_hour == 31:
        u_hour = 7
    else:
        u_hour = utc_hour

    #Adding 5 minutes to check time
    wait_min = minutes + 5 

    if wait_min == 61:
        later_min = 1
        u_hour += 1
    elif wait_min == 62:
        later_min = 2
        u_hour += 1 
    elif wait_min == 63:
        later_min = 3
        u_hour += 1
    elif wait_min == 64:
        later_min = 4
        u_hour += 1 
    elif wait_min == 65:
        later_min = 5
        u_hour += 1 
    else:
        later_min = wait_min

    utc_time = str(datetime.time(u_hour, later_min)).split(":")
    time = utc_time[0] + ":" + utc_time[1]
    print(time)


    # wait_time = datetime.timedelta(seconds=300)

    schedule.every().day.at(time).do(send_ec_text, user_name=user_name, 
        e_name=e_name, details=details, number=number)

def change_wait_time_to_utc(hour, minutes):
    """Change pacific time to utc time"""

    #Pacific to UTC 
    utc_hour = hour + 8 

    if utc_hour == 24:
        u_hour = 0
    elif utc_hour == 25:
        u_hour = 1
    elif utc_hour == 26:
        u_hour = 2
    elif utc_hour == 27:
        u_hour = 3
    elif utc_hour == 28:
        u_hour = 4
    elif utc_hour == 29:
        u_hour = 5
    elif utc_hour == 30:
        u_hour = 6
    elif utc_hour == 31:
        u_hour = 7
    else:
        u_hour = utc_hour

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


    #Adding 5 minutes to check time
    wait_min = minutes + 1 


    if wait_min == 60:
        later_min = 0
        u_hour += 1 
    elif wait_min == 61:
        later_min = 1
        u_hour += 1 
    else:
        later_min = wait_min

    utc_time = str(datetime.time(u_hour, later_min)).split(":")
    time = utc_time[0] + ":" + utc_time[1]
    # print(time)
    return time
            

# schedule_ec_text_time(hour, minute, user_name, e_name, details, number)


def check_time():
    """Checks if it is the right time (5 min after the first text sent)
        If it the value in db is false, then schedule emergency contact text."""

    print("checking...")
    print(schedule.jobs)

    #RIGHT NOW's TIME 
    now = datetime.datetime.utcnow()
    utc_h = now.hour
    utc_m = now.minute
    utc_now_time = str(datetime.time(utc_h, utc_m))

    #Querying everything in the check text table that isnt None 
    unchecked_text_queue = Check_Text.query.filter((Check_Text.true_false == "true") | (Check_Text.true_false == "false")).all()

    for user in unchecked_text_queue:
        #retrieve info for everyone in queue
        user_id = user.user_id
        user_name = user.user_name

        e_name = E_Contact.query.filter_by(user_id=user_id).order_by(desc(
        E_Contact.e_id)).first().e_name

        details = Activity.query.filter_by(user_id=user_id).order_by(desc(
        Activity.activity_id)).first().details

        phone = User_Phone.query.filter_by(user_id=user_id).first().phone


        #retrieve each user's last 'time'
        time = Activity.query.filter_by(user_id=user_id).order_by(desc(Activity.activity_id)).first().time
        split_time = time.split(":")
        hours = split_time[0]
        minutes = split_time[1]


        #Change that time to UTC time
        changed_wait_time = change_wait_time_to_utc(hour, minute)

        check_status = Check_Text.query.filter_by(user_id=user_id).first()
        
        t_or_f = check_status.true_false
        

        #If it is the right time, then clear scheduler
        if changed_wait_time in utc_now_time:
            if t_or_f == False:
                schedule_ec_text_time(hours, minutes, user_name, e_name, details, phone)  
                #delete row
                t_or_f = None
            else:
                #delete row
                t_or_f = None



if __name__ == "__main__":


    # def check_time():
    #     print("checking...")
    #     print(schedule.jobs)

    #     now = datetime.datetime.utcnow()
    #     utc_h = now.hour
    #     utc_m = now.minute
    #     utc_now_time = str(datetime.time(utc_h, utc_m))

    #     input_time = str(datetime.time(22, 42))

    #     if input_time in utc_now_time:
    #         schedule.clear("test")

    # schedule.every().seconds.tag("test").do(check_time)

    schedule.run_continuously(1)




