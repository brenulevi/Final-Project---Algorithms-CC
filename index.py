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

# Function for return all products on db
def FindAllProducts():
  file = open("./db/db.json", "r+", encoding='utf8')
  db = json.load(file)
  file.close()

  values = list(db["products"].values())
  keys = list(db["products"])

  types = ["serie", "movie", "documentary"]

  for product in values:
    product["code"] = keys[values.index(product)]
    product["type"] = types[product["type"]-1]
    
  products_dict = {}
  for item in values:
    name = item.pop('code')
    products_dict[name] = item

  return products_dict
  
# Function for return a specific product on db based in code
def FindByCode(code):
  file = open("./db/db.json", "r+", encoding='utf8')
  db = json.load(file)
  file.close()

  values = list(db["products"].values())
  keys = list(db["products"])

  types = ["serie", "movie", "documentary"]

  for product in values:
    product["code"] = keys[values.index(product)]
    product["type"] = types[product["type"]-1]

  for product in values:
    if product["code"] == code:
      return product
  
  return "Product don't exists"

# Function for return all products based on type passed
def FindProductsByType(type):
  file = open("./db/db.json", "r+", encoding='utf8')
  db = json.load(file)
  file.close()

  values = list(db["products"].values())
  keys = list(db["products"])
  
  types = ["serie", "movie", "documentary"]
  
  for product in values:
    product["code"] = keys[values.index(product)]

  filtered_products = {}
  count = 0
  
  for product in values:
    if product["type"] == type:
      product["type"] = types[product["type"]-1]
      filtered_products[count] = product
      count+=1
    
  if len(filtered_products) == 0:
    return "Products don't exists"
  else:
    return filtered_products
#endregion

#region Classes
class NerdFlix:

  #User type
  user_type = ""
  #What user is active now
  active_user = {}

  def __init__(self) -> None:
    self.proceed = self.Start()
    if self.proceed == True:
      self.user_type = self.getUser()
    self.getAccount()
    pass

  # Initialize App
  def Start(self):
    print("============== WELCOME TO NERDFLIX ==============")
    print("\n\n\n")
    input("            Press any key to proceed             ")
    return True

  # Get what type of user is (Customer or employeer)
  def getUser(self):
    user_type = input("Hello! Who are you? Type 1 for CUSTOMER or 2 for EMPLOYEER\n")
    if user_type == "1": return "Customers"
    elif user_type == "2": return "Employees"
    else:
      print("Invalid answer, try again!")
      return self.getUser()

  # Get if user have or not an account
  def getAccount(self):
    have_account = input(f"Hello Mr/Ms {self.user_type}, Do you have an account? Type 1 for YES or 2 for NO\n")
    if have_account == "1": 
      self.Login()
    elif have_account == "2": 
      self.CreateAccount()
    else:
      print("Invalid answer, try again!")
      self.getAccount()

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
              "4 - Found product by code\n")
    if answer.lower() == "all":
      products = FindAllProducts()
      df = pandas.DataFrame(data=products)
      
      print("\n ALL PRODUCTS\n")
      print(df.transpose())
      print("\n")

      end_answer = ""
      while end_answer != "1":
        end_answer = input("Press 1 to go back to Dashboard\n")

      self.Dashboard()
    else:
      if answer == "4":
        response = FindByCode(input("What's the product code?\n"))

        if response != "Product don't exists":
          df = pandas.DataFrame(data=response, index=[0])
          print("\n")
          print(df)
          print("\n")

          input("Press Enter to go back to Dashboard")
          self.Dashboard()
        else:
          answer = input(f"{response}, do you want to try another search? (1 - YES)\n")
          if answer == "1":
            self.SearchProduct()
          else:
            self.Dashboard()
      elif answer == "1" or answer == "2" or answer == "3":
        response = FindProductsByType(int(answer))

        if response != "Products don't exists":
          df = pandas.DataFrame(data=response)
      
          print("\n")
          print(df.transpose())
          print("\n")

          input("Press Enter to back to Dashboard\n")
          self.Dashboard()
        else:
          answer = input(f"{response}, do you want to try another search? (1 - YES)\n")
          if answer == "1":
            self.SearchProduct()
          else:
            self.Dashboard()
      else:
        print("Invalid answer, try again")
        self.SearchProduct()

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

if nerdFlix.user_type == "Customers":
  user = Customer(nerdFlix.active_user)
  user.Dashboard()
elif nerdFlix.user_type == "Employees":
  user = Employeer(nerdFlix.active_user)
  user.Dashboard()
#endregion