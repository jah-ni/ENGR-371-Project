#ENGR 371 - Library Occupancy API integration - Winter 2026
#Code Sourced from https://github.com/opendataConcordiaU/documentation/blob/master/getting_started.md
#And addapted by Jahni Juby for ENGR 371 project
#Gina Cody School for Engineering 

#Imports
import urllib.request
import json
import csv
import os
from datetime import datetime

#My Registered Authentification User and Key - Jahni Juby (40301198)  
user = "964"
key = "5bc8161aa69339530d95532e000627a7"

#API---- Provided by Concordia University
endpoints = {
    "occupancy": {"params": []},
    "computers": {"params": []},
    "events": {"params": []},
    "hours": {"params": ["date as 'YYYY-MM-DD'"]},
    "room_list": {"params": [], "path": "rooms/getRoomsList"},
    "reservations": {
        "params": ["resourceID", "scheduleID"],
        "path": "rooms/getRoomReservations",
    },
}

def openConnection(username, password):
    """Set up authentication and open connection"""
    API_url = "https://opendata.concordia.ca"
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, API_url, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    opener.open(API_url)
    urllib.request.install_opener(opener)


def validateRequest(endpoint, params):
    """Validate that a valid argument with the correct number of parameters has been supplied."""
    if endpoint not in endpoints:
        helpInfo = ", ".join(endpoints.keys())
        print(f"Invalid endpoint. Please use one of the following: {helpInfo}")
        return False
    elif len(params) != len(endpoints[endpoint]["params"]):
        helpInfo = ", ".join(endpoints[endpoint]["params"])
        print(f"Invalid params. {endpoint} requires the following: {helpInfo}")
    else:
        return True


def makeRequest(endpoint, *args):
    """Make request and return the response after validation"""
    if validateRequest(endpoint, args):
        params = "/".join(args)
        path = (
            endpoints[endpoint]["path"] if "path" in endpoints[endpoint] else endpoint
        )
        url = f"https://opendata.concordia.ca/API/v1/library/{path}/{params}"
        with urllib.request.urlopen(url) as req:
            res = req.read()
        return res
    else:
        return False
    
def get_occupancy():

    #URL for concordiea occupancy endpath: https://opendata.concordia.ca/API/v1/library/occupancy/
    url = "https://opendata.concordia.ca/API/v1/library/occupancy/"
    
    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                raw_data = response.read().decode('utf-8')
                save_to_csv(raw_data) # Call the save function here
            else:
                print(f"Error:{response.getcode()}")
    except Exception as e:
        print( f"An error occurred: {e}")

if __name__ =="__main__":
    openConnection(user, key)
    response = makeRequest("reservations", "*", "*")
    print(response)

#END OF API provided by Concordia University
#CODE TO TAKE CONCORDIA DATA AND TRANLATE IT TO CSV FILE FOR MS EXCELL USAGE
#------------------------------------------------------
def save_to_csv(raw_data):
    file_exists = os.path.isfile('library_data.csv')
    
    data = json.loads(raw_data)
    
    webster_occ = data.get("Webster", {}).get("Occupancy", "N/A")
    webster_time = data.get("Webster", {}).get("LastRecordTime", "N/A")
    
    # Time stamp on data was weird so this shows montreal time of request.
    #Should email for further clearification on data timestamp, seems to be ahead in time zone
    #Might be due to API server host location, although google said concordia hosts its own servers...?
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open('library_data.csv', mode='a', newline='') as  file:
        writer = csv.writer(file)
        
        #write header only if the file is not found
        if not file_exists:
            writer.writerow(['LocalTime', ' WebsterOccupancy', ' WebsterAPITime'])
        
        writer.writerow([current_time, webster_occ, webster_time])
    
    print(f"Data appended to library_data.csv at {current_time} montreal time")

# --- Running the code ---
#gotta request access w/ openConnection then run the get_occupancy function
openConnection(user, key)
get_occupancy()