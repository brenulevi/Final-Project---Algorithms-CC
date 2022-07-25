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
  if user_type == "1": return "Customer"
  elif user_type == "2": return "Employeer"
  else:
    print("Invalid answer, try again!")
    getUser()

def createSafePassword():
  return "123123"

def ValidateCredentials(user_type, username, password):
  return {
    "validated": True,
    "username": username,
    "password": password
  }
#endregion

# App class
class NerdFlix:
  
  #Federative Unit
  uf = getLocation()
  #User type
  user_type = ""
  #What user is active now
  active_user = {}

  #Create account if user haven't
  def CreateAccount(self):
    username = input("What'll be your username?")
    password = input("Type your password, use a secure one! If you want type 123 and we create a safe password to you!")
    if password == "123":
      password = createSafePassword()
    else:
      response = ValidateCredentials(self.user_type, username, password)
      # if response["validated"] == True:
      #   #proceed

  
  #Login user with her credentials
  def Login(self):
    username = input("Alright! Give me you username\n")
    password = input("Received! Now your password, I promise it'll be very well protected\n")

    self.active_user["username"] = username
    self.active_user["password"] = password

#Instantiate App class
nerdFlix = NerdFlix()

#Set what type of user is using the app
nerdFlix.user_type = getUser()

#Get if the user have account and send her to Login or Create Account
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

print(nerdFlix.active_user)