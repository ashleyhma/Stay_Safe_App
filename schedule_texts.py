# FUNCTIONS TO SCHEDULE 

import datetime
import time
import schedule
from twilio.rest import Client
from twilio.rest import TwilioRestClient


""" RUNS A JOB ONLY ONCE 

def job_that_executes_once():
    # Do some work ...
    return schedule.CancelJob

schedule.every().day.at('22:30').do(job_that_executes_once)

https://schedule.readthedocs.io/en/stable/faq.html#how-can-i-run-a-job-only-once """

def write_okay_text(user_name):
    """Writes up a generalized hey, are you okay? text """

    return f"Hi {user_name}, this is Stay Safe. Hope you are doing okay! If you do not respond within 5 minutes, we will send a text to your emergency contact."


def check_time(time):
    """takes inputted time and keeps checking time until the right time to call 
    the text function. """

    schedule.every().day.at(time).do(send_check_text)

    while True:
        schedule.run_pending()
        time.sleep(1)




def send_check_text(okay_text):
    """Sends okay_text when it is the specified time using Twilio."""



    return schedule.CancelJob


def write_ec_text(user_name, e_name, details, number):
    """Writes up specific text to emergency contact."""

    return f"Hi {e_name}, this is {user_name}. I am {details}. If you are receiving this, I might have not made it to my destination. Please give me a call at {number}."  

def check_ec_text_time(time):
    """Check for the time that the emergency contact text will be sent out"""

    schedule.every().day.at(time).do(send_ec_text)

    while True:
        schedule.run_pending()
        time.sleep(1)

def send_ec_text():
    """Sends emergency contact text using Twilio."""

    return schedule.CancelJob




