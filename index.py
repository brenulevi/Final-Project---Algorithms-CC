#region Imports
from geopy.geocoders import Nominatim
import geocoder
import json
import string
import secrets
import pandas
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
    return getUser()

# Function for create a random safe password
def createSafePassword():
  return ''.join(secrets.choice(string.ascii_letters + string.digits + '-_') for i in range(10))

# Function for validate if the user exists or not
def ValidateCredentials(user_type, username, password, caller):
  file = open("./db/db.json", "r+", encoding='utf8')
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
    return {
      "validated": False
    }

# Function for validate if the product exists or not
def ValidateProduct(code):
  file = open("./db/db.json", "r+", encoding='utf8')
  db = json.load(file)
  file.close()

  keys = list(db["products"])

  for key in keys:
    if int(key) == code:
      return {
        "validated": False
      }
  return {
    "validated": True
  }

def FindAllProducts():
  return True

def FindByCode():
  return True

def FindProductsByType(type):
  return True
#endregion

#region Classes
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

    response = ValidateCredentials(self.user_type, username, password, "create")
    if response["validated"] == True:
      
      file = open("./db/db.json", "r+", encoding='utf8')
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
      to_change_file = open("./db/db.json", "w", encoding='utf8')
      json.dump(db, to_change_file, indent=2, ensure_ascii=False)
      to_change_file.close()

      print("Account created succesfully!")
      self.active_user = response["user"]
    else:
      print("We saw here that you already have an account, try to login!")
      self.Login()

  
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
  def __init__(self, active_user) -> None:
    self.active_user = active_user
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
    self.procedures = [self.RegisterProduct, self.SearchProduct, self.UpdateProduct, self.BuysHistory, self.UpdateAccount, self.Exit]
    pass

  def Dashboard(self):
    answer = int(input(
        f"Hello {self.active_user['username']}, what do you want to do?\n"
        "1 - Register product\n"
        "2 - Search product\n"
        "3 - Update product\n"
        "4 - Customers buys\n"
        "5 - Update my account\n"
        "6 - Exit NerdFlix\n"  
      )) - 1
    if answer <= 5 and answer >= 0:
      self.procedures[answer]()
    else:
      print("Invalid answer! try again")
      self.Dashboard()

  def RegisterProduct(self):
    print("Nice! Let's register a product!")
    code = int(input("First things first, send me the product code: "))
    name = input("Thanks! Now I need the product name: ")

    type = 0
    while type != 1 and type != 2 and type != 3:
      type = int(input("Product type (1 - Serie / 2 - Movie / 3 - Documentary): "))

    price = input("Product price (0000.00): ")

    can_buy = 0
    while can_buy != 1 and can_buy != 2:
      can_buy = int(input("This product can be bought? (1 - Yes / 2 - No): "))
    if can_buy == 1:
      can_buy = True
    elif can_buy == 2:
      can_buy = False

    product = {
      "name": name,
      "type": type,
      "price": price,
      "can_buy": can_buy
    }

    response = ValidateProduct(code)
    if response["validated"] == True:

      file = open("./db/db.json", "r+", encoding='utf8')
      db = json.load(file)
      file.close()

      db["products"][str(code)] = product
      to_change_file = open("./db/db.json", "w", encoding='utf8')
      json.dump(db, to_change_file, indent=2, ensure_ascii=False)
      to_change_file.close()

      print("Product created!")
      self.Dashboard()

  def SearchProduct(self):
    print("Nice! Let's search for a product")

    answer = input("Choose a option:\n"
              "all - List all products\n"
              "1 - List all series\n"
              "2 - List all movies\n"
              "3 - List all documentaries\n"
              "4 - Found product by code")
    if answer.lower() == "all":
      products = FindAllProducts()

      headers = ["Code", "Name", "Type", "Price", "Can Buy"]

      print(pandas.DataFrame(products, headers, headers))
    else:
      if answer == "4":
        FindByCode()

        #print table
      else:
        FindProductsByType(int(answer))

        #print table

  def UpdateProduct(self):
    print("Update!!!")

  def BuysHistory(self):
    print("History!!!")
  
  def UpdateAccount(self):
    print("Account!!!")

  def Exit(self):
    print("Exit!!!")
    
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