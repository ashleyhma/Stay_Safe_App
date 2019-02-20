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
    # print(time)
    return time

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

def check_if_received_text(hour, minute, from_number):
    """Check if text was received by server"""

    #Find time right now 
    now = datetime.datetime.utcnow()
    utc_h = now.hour
    utc_m = now.minutes
    utc_now_time = str(datetime.time(utc_h, utc_m))

    changed_wait_time = change_wait_time_to_utc(hour, minute)

    #when it is the right time
    if changed_wait_time in utc_now_time:
        #if the from number exists because of the request
        if from_number: 
            return True
        else:
            return False
            

# schedule_ec_text_time(hour, minute, user_name, e_name, details, number)


def check_time():

    print("checking...")
    print(schedule.jobs)

    now = datetime.datetime.utcnow()
    utc_h = now.hour
    utc_m = now.minute
    utc_now_time = str(datetime.time(utc_h, utc_m))

    changed_wait_time = change_wait_time_to_utc(hour, minute)

    t_f = Check_Text.query.filter_by(phone=phone).first().true_false
    

    #If it is the right time, then clear scheduler
    if changed_wait_time in utc_now_time:
        if t_f == False:
            schedule_ec_text_time(hour, minutes, user_name, e_name, details, phone)
           
       

            # schedule.clear("test")
        #delete row





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




