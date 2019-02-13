#This checks or finds if any of their info are in database
    user = User.query.filter_by(name=name).first()
    # user_id = user.user_id

    user.phones

    phone = User_Phone.query.filter_by(number=number).first()
    phone_id = phone.phone_id

    econtact = E_Contact.query.filter_by(e_name=e_name).first()
    e_id = econtact.e_id

    ephone = E_Phone.query.filter_by(e_number=e_number).first()
    ephone_id = ephone.ephone_id

    #Check if name matches the phone number by matching up user_id
    phone_user_id = phone.user_id

    #Check if userid matches econtact userid 
    econ_user_id = econtact.user_id

    #Check if econtactid matches enumber econtact id 
    enum_econ_id = ephone.e_id 

    #If user and phone does not match in database, then add all the information
    if user_id != phone_user_id:

        #Adding new_user first, to get user_id
        new_user = User(name=name)
        db.session.add(new_user)

        #Querying to get user_id
        user = User.query.filter_by(name=name).first()

        #Adding number and econtact to get econtact id
        new_number = User_Phone(number=number, user_id=user_id)
        new_econtact = E_Contact(e_name=e_name, user_id=user_id)
        db.session.add(new_number)
        db.session.add(new_econtact)

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id
        # print(e_id)

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone match, but userid and econtact userid doesnt
    elif (user_id == phone_user_id) and (user_id != econ_user_id):

        #Adding econtact to get econtact id
        new_econtact = E_Contact(e_name=e_name, user_id=user_id)
        db.session.add(new_econtact)

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone, user and econtact match but econtact and ephone doesnt
    elif (user_id == phone_user_id) and (user_id == econ_user_id) and (
        e_id != enum_econ_id):

        #Querying to get e contact id 
        econtact = E_Contact.query.filter_by(e_name=e_name).first()
        e_id = econtact.e_id

        # #Adding enumber and activity 
        new_enumber = E_Phone(e_number=e_number, e_id=e_id )
        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(new_enumber)
        db.session.add(activity)

        db.session.commit()

    #If user and phone, user and econtact, and econtact and ephone match
    elif (user_id == phone_user_id) and (user_id == econ_user_id) and (
        e_id == enum_econ_id):

        activity = Activity(details=details, time=time, user_id=user_id)
        db.session.add(activity)

        db.session.commit()        