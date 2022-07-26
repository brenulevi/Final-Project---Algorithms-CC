#region Imports
from geopy.geocoders import Nominatim
import geocoder
import json
#endregion

#region Functions
# Function for get user location for buys location
def getLocation():
  Nomi_locator = Nominatim(user_agent="My app")

  my_location = geocoder.ip("me")

  latitude = my_location.geojson['features'][0]['properties']['lat']
  longitude = my_location.geojson['features'][0]['properties']['lng']

  location = str(Nomi_locator.reverse(f"{latitude}, {longitude}")).split(",")[-4].strip(" ")

  return location

# Function for get what type of user is (Customer or employeer)
def getUser():
  user_type = input("Hello! Who are you? Type 1 for CUSTOMER or 2 for EMPLOYEER\n")
  if user_type == "1": return "Customers"
  elif user_type == "2": return "Employees"
  else:
    print("Invalid answer, try again!")
    getUser()

def createSafePassword():
  return "123123"

def ValidateCredentials(user_type, username, password, caller):
  file = open("./db/db.json", "r+")
  db = json.load(file)
  file.close()
  users = list(db["users"][user_type.lower()].values())

  have_account = []

  if caller == "create":
    for user in users:
      if user["username"] == username:
        have_account.append(True)
      else:
        have_account.append(False)

    if True in have_account:
      return {
        "validated": False
      }
    else:
      return {
        "validated": True,
        "user": {
          "username": username,
          "password": password
        }
      }
  else:
    for user in users:
      if(user["username"] == username and user["password"] == password):
        return {
          "validated": True,
          "user": {
            "username": username,
            "password": password
          }
        }
      else:
        return {
          "validated": False
        }
#endregion

#region App Class
class NerdFlix:
  
  #Federative Unit
  uf = getLocation()
  #User type
  user_type = ""
  #What user is active now
  active_user = {}

  #Create account if user haven't
  def CreateAccount(self):
    username = input("What'll be your username?\n")
    password = input("Type your password, use a secure one! If you want type 123 and we create a safe password to you!\n")
    if password == "123":
      password = createSafePassword()
    else:
      response = ValidateCredentials(self.user_type, username, password, "create")
      if response["validated"] == True:
        
        file = open("./db/db.json", "r+")
        db = json.load(file)
        file.close()

        if len(list(db["users"][self.user_type.lower()].keys())) > 0:
          id = format(int(list(db["users"][self.user_type.lower()].keys())[-1]) + 1, '04d')
        else:
          id = "0001"

        user = {
          "username": username,
          "password": password
        }

        db["users"][self.user_type.lower()][id] = user
        to_change_file = open("./db/db.json", "w")
        json.dump(db, to_change_file, indent=2)
        to_change_file.close()

        print("Account created succesfully!")
        self.active_user = response["user"]
      else:
        print("We saw here that you already have an account, try to login!")
        nerdFlix.Login()

  
  #Login user with her credentials
  def Login(self):
    username = input("Alright! Give me you username\n")
    password = input("Received! Now your password, I promise it'll be very well protected\n")
    response = ValidateCredentials(self.user_type, username, password, "login")
    if response["validated"] == True:
      print("Logged!")
      self.active_user = response["user"]
    else:
      print("Invalid credentials, try again!")
      self.Login()

class Customer:
  def __init__(self) -> None:
    self.active_user = nerdFlix.active_user
    pass

  def Dashboard(self):
    answer = input(
        f"Hello {self.active_user['username']}, what do you want to do?\n"
        "1 - Let's buy!\n"
        "2 - See my buys\n"
        "3 - Update my account\n"
        "4 - Delete my account\n"
        "5 - Exit NerdFlix\n"  
      )

class Employeer:
  def __init__(self, active_user) -> None:
    self.active_user = active_user
    pass

  def Dashboard(self):
    answer = input(
        f"Hello {self.active_user['username']}, what do you want to do?\n"
        "1 - Register product\n"
        "2 - Search product\n"
        "3 - Update product\n"
        "4 - Customers buys\n"
        "5 - Update my account\n"
        "6 - Exit NerdFlix\n"  
      )

#endregion

#region Interactions
#Instantiate App class
nerdFlix = NerdFlix()

#Set what type of user is using the app
nerdFlix.user_type = getUser()

while True:
  have_account = input(f"Hello Mr/Ms {nerdFlix.user_type}, Do you have an account? Type 1 for YES or 2 for NO\n")
  if have_account == "1": 
    nerdFlix.Login()
    break
  elif have_account == "2": 
    nerdFlix.CreateAccount()
    break
  else:
    print("Invalid answer, try again!")

if nerdFlix.user_type == "Customers":
  user = Customer(nerdFlix.active_user)
  user.Dashboard()
elif nerdFlix.user_type == "Employees":
  user = Employeer(nerdFlix.active_user)
  user.Dashboard()
#endregion