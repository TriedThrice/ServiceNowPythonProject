import requests
import json
from bs4 import BeautifulSoup

# Adjust these details for each instance
INSTANCE_NAME = "dev290564"
USERNAME = "admin"
PASSWORD = "eg-/Tyt7ZL5I"

API_URL = f"https://{INSTANCE_NAME}.service-now.com/api/now/table/sys_user"
FILTER = "?sysparm_query=roles%3Dadmin&sysparm_view="
HEADER = {"Accept": "application/json"}

# Create list to store user info for later comparison
checkUserList = []

# Make API request
response = requests.get(API_URL + FILTER, auth=(USERNAME, PASSWORD), headers=HEADER)
#response = requests.get(API_URL, auth=(USERNAME, PASSWORD), headers=HEADER)
john = ["John Doe", "JohnDoe@gmail.com", "John Doe", "1234567890"]
checkUserList.append(john)

# Get XML file from the current instance 
# Response from instance, code 200 is success
if response.status_code == 200:
    users = response.json().get("result", [])
    for user in users:
        nameID = user.get("user_name")
        email = user.get("email")
        realname = user.get("name")
        sysID = user.get("sys_id")
        
        addUser = [nameID, email, realname, sysID]
        
        checkUserList.append(addUser)
        #print("Admin User:", nameID + ", " + email + ", " + sysID)
        #print("-" * 10)
    #print("Admin Users:", json.dumps(users, indent=4))
else:
    print("Error:", response.status_code, response.text)
    
defaultUserList = []

# Get the previously saved XML file for comparison
with open("defaultAdmins.xml", "r") as file:
    content = file.read()
    

# Parse the XML content
soup = BeautifulSoup(content, "xml")

# Extract user details and append to defaultUserList
for user in soup.find_all("sys_user"):
    user_name = user.find("user_name").text
    email = user.find("email").text
    name = user.find("name").text
    sys_id = user.find("sys_id").text
    
    defaultUserList.append([user_name, email, name, sys_id])

# Compare the two lists 
# Everything below this point is placeholder for when i know what kind of comparison and details are needed
match = True
for user in checkUserList:
    if user not in defaultUserList:
        print("New Admin User:", user)
        print("-" * 10)
        match = False
        
if match:
    print("No new Admin Users found.")
else:
    print("New Admin Users found.")
    # send message to admin on service now instance using REST API, email, or other method
    # for now, just print the message
    
    
