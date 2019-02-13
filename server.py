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


    name = request.form.get("name")
    number = request.form.get("number")

    user = User.query.filter_by(name=name).first()

    if not user: 

        user = User(name=name)

        db.session.add(user)
        db.commit()

        user.add_number(number)

        ession["user_id"] = user.user_id

        return render_template("form.html")

    elif user.check_phone(number):

        session["user_id"] = user.user_id

        return render_template("homepage.html")
 
    

@app.route('/enter-info', methods=["GET"])
def show_form():

    return render_template("form.html")



# @app.route('/enter-info', methods=["POST"])
# def save_form_data():
  
#    #Retrieves data from form
    
#     # e_name = request.form.get("e_name")
#     # e_number = request.form.get("e_number")
#     # details = request.form.get("activity")
#     # hours = int(request.form.get("hours"))
#     # minutes = int(request.form.get("minutes"))
#     # time = f"{hours}:{minutes}" 

#     # #This checks or finds if any of their info are in database
#     # user = User.query.filter_by(name=name).first()



#     return redirect('/succes')

@app.route('/success')
def succes():

    return render_template("success.html")


if __name__ == "__main__":
    
    app.debug = True
    
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
