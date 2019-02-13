from model import *

from sqlalchemy import func

from server import app

def load_data():

    Julian = User(name='Julian')
    Beth = User(name='Beth')
    Katy = User(name='Katy')

    phone1 = User_Phone(number='5101234567', user_id='1')
    phone2 = User_Phone(number='4158883344', user_id='1')
    phone3 = User_Phone(number='6508888888', user_id='2')
    phone4 = User_Phone(number='6191312222', user_id='3')

    Ariana = E_Contact(e_name='Ariana', user_id='1')
    Henry = E_Contact(e_name='Henry', user_id='1')
    Gloria = E_Contact(e_name='Gloria', user_id='1')
    Chris = E_Contact(e_name='Chris', user_id='2')
    Bob = E_Contact(e_name='Bob', user_id='3')

    ephone1 = E_Phone(e_number='1234567890', e_id='1')
    ephone2 = E_Phone(e_number='5556663322', e_id='2')
    ephone3 = E_Phone(e_number='2123336666', e_id='3')
    ephone4 = E_Phone(e_number='4153393399', e_id='4')
    ephone5 = E_Phone(e_number='6804425522', e_id='5')

    activity1 = Activity(details='walking home', time='17:00', user_id='1')
    activity2 = Activity(details='walking dog', time='20:00', user_id='1')
    activity3 = Activity(details='on a date', time='19:00', user_id='2')
    activity4 = Activity(details='at the club', time='01:00', user_id='3')


    db.session.add(Julian)
    db.session.add(Beth)
    db.session.add(Katy)
    db.session.add(phone1)
    db.session.add(phone2)
    db.session.add(phone3)
    db.session.add(phone4)
    db.session.add(Ariana)
    db.session.add(Henry)
    db.session.add(Gloria)
    db.session.add(Chris)
    db.session.add(Bob)
    db.session.add(ephone1)
    db.session.add(ephone2)
    db.session.add(ephone3)
    db.session.add(ephone4)
    db.session.add(ephone5)
    db.session.add(activity1)
    db.session.add(activity2)
    db.session.add(activity3)
    db.session.add(activity4)


    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_data()



