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
from datetime import timedelta  
import os
import datetime
import time
import sys

faker = Factory.create()

carMake = ["Nissan", "Chevy", "Honda", "Cadillac", "Ferrari",
           "Ford", "Lexus", "Hyundai", "Dodge", "Mitsubishi"]

carModel = ["Maxima", "Cobalt", "Civic", "ATS", "Enzo",
            "F-150", "IS-350", "Accent", "Dart", "Lancer"]

spotTypelist = ["student", "staff", "private", "handicapped"]

index = textColumns = 0
vehiclesNum = setsNum = 0
userURL = projectName = firebaseDirectory = header = vehicleString = []
lot = spotID = vacancy = spotType = occupant = []
userEmail = userID = cardID = firstName = lastName = phone = permitType = expDate = purchaseDate = []
make = model = color = licensePlate = []
authorized = False

projectName = raw_input("Firebase project = example for https://example.firebaseio.com\n"
                        "Please enter the name of your Firebase project: ")
userURL = "https://"
userURL = userURL + projectName
userURL = userURL + ".firebaseio.com"

spotsNum = 50
useraccountsNum = 100

firebase = firebase.FirebaseApplication(userURL, None)
text_ids = open("cardIDS.txt", "w")


sys.stdout.write("Uploading Spots section of database... ")
sys.stdout.flush()
for i in range(1, spotsNum+1):
        # Spots
    lot = "LB"           		# Lot
    firebaseDirectory = "/Spots/"
    firebaseDirectory = firebaseDirectory + lot
    spotID = str(i)  		        # Spot ID
    vacancy = True	                # Vacant
    authorized = False   		# Authorized
    occupant = 'none'   	     	# User Email
        
    index = randint(0,3)
    spotType = spotTypelist[index]
    
    firebase.put(firebaseDirectory, spotID, params={'print': 'silent'},
                         data={'vacancy': vacancy,
                               'type': spotType,
                               'occupant': occupant,
                               'authorized': authorized})
    #time.sleep(0.50)

print("COMPLETED")
sys.stdout.write("Uploading UserAccounts section of database... ")
sys.stdout.flush()
for i in range(1, useraccountsNum+1):
        # UserAccounts			# User ID
    userID = str(randint(1000000000, 9999999999))
					# Card ID
    cardID = str(randint(0, 2147483647));
    textColumns = textColumns + 1
    if i == useraccountsNum:
	text_ids.write("\"%s\"" % cardID)
    else:
    	text_ids.write("\"%s\", " % cardID)
    if textColumns >= 5:
    	text_ids.write("\n")
	textColumns = 0

    firebaseDirectory = "/UserAccounts/"
    userEmail = faker.email()           # User Email
    firstName = faker.first_name()      # First Name
    lastName = faker.last_name()        # Last Name
    phone = faker.phone_number()        # Phone Number    
    	# permitInfo
    index = randint(0,3)
    permitType = spotTypelist[index]    # Permit Type 
                                        # Purchase Date
    purchaseDate = datetime.datetime.date(faker.date_time_between(start_date="-1y", end_date="now", tzinfo=None))
                                        # Expiration Date (exactly one year added for permits)
    expDate = purchaseDate + timedelta(days=365)     
    
    firebase.put(firebaseDirectory, userID, params={'print': 'silent'},
                         data={'cardID': cardID,
			       'userEmail': userEmail,
                               'firstName': firstName,
                               'lastName': lastName,
                               'phone': phone,
                               'permit': {
                                   'type': permitType,
                                   'expDate': expDate,
                                   'purchaseDate': purchaseDate}})
    #time.sleep(0.50)

    firebaseDirectory = firebaseDirectory + userID + "/vehicles"                              
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
    	#time.sleep(0.50)
print "COMPLETED"
text_ids.close()
os._exit(0)

