# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 00:17:56 2017

@author: Michael
"""

# TURN OFF AUTHORIZATION OF YOUR FIREBASE PROJECT BEFORE RUNNING THE CODE.
# THE TWO PACKAGE NAMES ARE INCLUDED BELOW 
# ALSO THIS WAS DONE IN PYTHON 2.7

from faker import Factory # pip install Faker
from random import randint
from firebase import firebase # pip install python-firebase

faker = Factory.create()

carMake = ["Nissan", "Chevy", "Honda", "Cadillac", "Ferrari",
           "Ford", "Lexus", "Hyundai", "Dodge", "Mitsubishi"]

carModel = ["Maxima", "Cobalt", "Civic", "ATS", "Enzo",
            "F-150", "IS-350", "Accent", "Dart", "Lancer"]

spotTypelist = ["student", "staff", "private", "handicapped"]

index = 0
vehiclesNum = setsNum = 0
userURL = projectName = firebaseDirectory = header = vehicleString = []
lot = spotID = vacancy = spotType = occupant = []
userEmail = userID = firstName = lastName = phone = permitType = expDate = purchaseDate = []
make = model = color = licensePlate = []
authorized = False

projectName = raw_input("Firebase project = example for https://example.firebaseio.com\n"
                        "Please enter the name of your Firebase project: ")
userURL = "https://"
userURL = userURL + projectName
userURL = userURL + ".firebaseio.com"

setsNum = input("Please enter how many sets of data you want to create: ")

firebase = firebase.FirebaseApplication(userURL, None)

for i in range(setsNum):
        # Spots
    lot = faker.state_abbr()            # Lot
    firebaseDirectory = "/Spots/"
    firebaseDirectory = firebaseDirectory + lot
    spotID = randint(1, 250)            # Spot ID
    vacancy = faker.boolean()           # Vacant
    occupant = faker.email()
    if vacancy != True:
        authorized = faker.boolean()    # Authorized
        occupant = faker.email()        # User Email
    else:
        authorized = False
        occupant = 'none'
        
    index = randint(0,3)
    spotType = spotTypelist[index]
    
    firebase.put(firebaseDirectory, spotID, params={'print': 'silent'},
                         data={'vacancy': vacancy,
                               'type': spotType,
                               'occupant': occupant,
                               'authorized': authorized})


        # UserAccounts
    userID = faker.ean8()               # User ID    
    firebaseDirectory = "/UserAccounts/"
    userEmail = faker.email()           # User Email
    firstName = faker.first_name()      # First Name
    lastName = faker.last_name()        # Last Name
    phone = faker.phone_number()        # Phone Number    
            # permitInfo
    index = randint(0,3)
    permitType = spotTypelist[index]    # Permit Type
    expDate = faker.date()              # Purchase Date
    purchaseDate = faker.date()         # Expiration Date
    
    firebase.put(firebaseDirectory, userID, params={'print': 'silent'},
                         data={'userEmail': userEmail,
                               'firstName': firstName,
                               'lastName': lastName,
                               'phone': phone,
                               'permit': {
                                   'type': permitType,
                                   'expDate': expDate,
                                   'purchaseDate': purchaseDate}})

    firebaseDirectory = firebaseDirectory + userID                               
    vehiclesNum = randint(1,4)
    for j in range(vehiclesNum, 0, -1):
            # vehicleInfo
        vehicleString = str(j)
        header = "vehicle"
        header = header + vehicleString
        index = randint(0,9)
        make = carMake[index]           # Vehicle Make
        index = randint(0,9)
        model = carModel[index]         # Vehicle Model
        color = faker.safe_color_name() # Vehicle Color
        licensePlate = faker.ean8()     # License Plate
    
        firebase.put(firebaseDirectory, header, params={'print': 'silent'},
                         data={'make': make,
                               'model': model,
                               'color': color,
                               'licensePlate': licensePlate})
                               
