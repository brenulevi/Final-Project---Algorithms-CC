#region Imports
from datetime import datetime
from math import prod
from geopy.geocoders import Nominatim
import geocoder
import json
import string
import secrets
import pandas
import os
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
      }
  else:
    for user in users:
      if(user["username"] == username and user["password"] == password):
        return {
          "validated": True,
          "user": {
            "id": user["id"],
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
    os.system('cls||clear')
    print("============== WELCOME TO NERDFLIX ==============")
    print("\n\n\n")
    input("            Press any key to proceed             ")
    return True

  # Method to get what type of user is (Customer or employeer)
  def getUser(self):
    user_type = input("Hello! Who are you? Type 1 for CUSTOMER or 2 for EMPLOYEER\n")
    if user_type == "1": return "Customers"
    elif user_type == "2": return "Employees"
    else:
      print("Invalid answer, try again!")
      return self.getUser()

  # Method to get if user have or not an account
  def getAccount(self):
    os.system('cls||clear')
    have_account = input(f"Hello Mr/Ms {self.user_type}, Do you have an account? Type 1 for YES or 2 for NO\n")
    if have_account == "1": 
      self.Login()
    elif have_account == "2": 
      self.CreateAccount()
    else:
      print("Invalid answer, try again!")
      self.getAccount()

  # Method to create account if user haven't
  def CreateAccount(self):
    os.system('cls||clear')
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
        "id": id,
        "username": username,
        "password": password,
        "cart": {}
      }

      db["users"][self.user_type.lower()][id] = user
      to_change_file = open("./db/db.json", "w", encoding='utf8')
      json.dump(db, to_change_file, indent=2, ensure_ascii=False)
      to_change_file.close()

      print("Account created succesfully!")
      self.active_user = user
    else:
      print("We saw here that you already have an account, try to login!")
      self.Login()
 
  # Method to login user with her credentials
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

  # Method to update user data
  def UpdateAccount(self):
    os.system('cls||clear')
    file = open("./db/db.json", "r+", encoding="utf8")
    db = json.load(file)
    file.close()

    answer = input(f"Nice! I found you account here and the account info is:\nUsername: {db['users'][self.user_type.lower()][self.active_user['id']]['username']}\nPassword: {db['users'][self.user_type.lower()][self.active_user['id']]['password']}\n"
              "What do you want to change?\n1 - Username\n2 - Password\n")
    
    possibilities = ["username", "password"]

    if answer != "1" and answer != "2":
      self.UpdateAccount()
    else:
      new_credential = input(f"Type your new {possibilities[int(answer)-1]}:\n")

      db["users"][self.user_type.lower()][self.active_user["id"]][possibilities[int(answer)-1]] = new_credential
      
      to_change_file = open("./db/db.json", "w", encoding='utf8')
      json.dump(db, to_change_file, indent=2, ensure_ascii=False)
      to_change_file.close()

      input("Account updated! Press any key to back to dashboard!")
      user_active.active_user = db["users"][self.user_type.lower()][self.active_user["id"]]
      user_active.Dashboard()

class Customer:
  def __init__(self, active_user) -> None:
    self.active_user = active_user
    self.procedures = [self.BuyProduct, self.MyCart, self.MyBuyHistory, nerdFlix.UpdateAccount, self.Exit]
    pass

  # DASHBOARD
  def Dashboard(self):
    os.system('cls||clear')
    answer = input(
        f"Hello {self.active_user['username']}, what do you want to do?\n"
        "1 - Let's buy!\n"
        "2 - See my cart\n"
        "3 - See my buy's history\n"
        "4 - Update my account\n"
        "5 - Exit NerdFlix\n"  
      )
    if int(answer) - 1 <= 5 and int(answer) - 1 >= 0:
      if int(answer) - 1 == 0:
        self.BuyProduct(0)
      else:
        self.procedures[int(answer) - 1]()
    else:
      print("Invalid answer, try again")
      self.Dashboard()

  # Method to buy products
  def BuyProduct(self, filter_procedure):
    os.system('cls||clear')
    print("Let's Buy!")

    procedures = [FindAllProducts, FindProductsByType]

    if filter_procedure == 0:
      products = procedures[filter_procedure]()
    else:
      products = procedures[1](filter_procedure)

    if products != "Products don't exists":
      df = pandas.DataFrame(data=products)
      print("\n")
      print(df.transpose())
      print("\n")
    else:
      print("Products not found")
      input("Press any key to try again")
      self.BuyProduct(0)

    print("Type the product code to buy: ")
    answer = input(
              "1 - Show all products  "
              "2 - Show all series  "
              "3 - Show all movies  "
              "4 - Show all documentaries  "
              "5 - See my shop cart "
              "6 - Back to Dashboard\n")
    if len(answer) == 6:
      response = ValidateProduct(answer)
      if response["validated"] == True:
        file = open("./db/db.json", "r+", encoding="utf8")
        db = json.load(file)
        file.close()
        
        if not answer in db["users"][nerdFlix.user_type.lower()][self.active_user["id"]]["cart"]:
          product_to_buy = FindByCode(answer)
          if product_to_buy != "Product don't exists":
            if product_to_buy["can_buy"] == True:
              product_to_buy["location"] = getLocation()
              product_to_buy["date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
              db["users"][nerdFlix.user_type.lower()][self.active_user["id"]]["cart"][answer] = product_to_buy

              if len(list(db["buys"].keys())) > 0:
                id = format(int(list(db["buys"].keys())[-1]) + 1, '04d')
              else:
                id = "0001"

              db["buys"][id] = {
                "name": product_to_buy["name"],
                "type": product_to_buy["type"],
                "price": product_to_buy["price"],
                "can_buy": product_to_buy["can_buy"],
                "code": product_to_buy["code"],
                "location": product_to_buy["location"],
                "date": product_to_buy["date"],
                "user": self.active_user
              }

              file_to_change = open("./db/db.json", "w", encoding="utf8")
              json.dump(db, file_to_change, indent=2, ensure_ascii=False)
              file_to_change.close()

              answer = input("Product added to your cart! What do you want to do now?\n"
                            "1 - Add another product to your cart "
                            "2 - See my cart "
                            "3 - Go to Dashboard\n")
              if answer == "1":
                self.BuyProduct(0)
              elif answer == "2":
                self.MyCart()
              else: self.Dashboard()
            else:
              input("This product can't be bought now, try again later")
              self.BuyProduct(0)
          else:
            input("Product don't exists")
            self.BuyProduct(0)
        else:
          input("You already have this product on cart!")
          self.BuyProduct(0)
      else:
        input("Product not found, try another code")
        self.BuyProduct(0)
    else:
      if int(answer) > 0 and int(answer) < 5:
        self.BuyProduct(int(answer) - 1)
      elif int(answer) == 6:
        self.Dashboard()
      elif int(answer) == 5:
        self.MyCart()
      else:
        print("Invalid answer, try again")
        self.BuyProduct(0)

  # Method to get the user cart
  def MyCart(self):
    print("My cart!")

  # Method to see buy history
  def MyBuyHistory(self):
    print("History!")
  
  # Method to exit application
  def Exit(self):
    exit()

class Employeer:
  def __init__(self, active_user) -> None:
    self.active_user = active_user
    self.procedures = [self.RegisterProduct, self.SearchProduct, "", self.BuysHistory, nerdFlix.UpdateAccount, self.Exit]
    pass

  # DASHBOARD
  def Dashboard(self):
    os.system('cls||clear')
    answer = input(
        f"Hello {self.active_user['username']}, what do you want to do?\n"
        "1 - Register product\n"
        "2 - Search product\n"
        "3 - Update product\n"
        "4 - Customers buys\n"
        "5 - Update my account\n"
        "6 - Exit NerdFlix\n"  
      )
    if int(answer) - 1 <= 5 and int(answer) - 1 >= 0:
      if int(answer) - 1 == 2:
        self.UpdateProduct(0)
      else:
        self.procedures[int(answer)-1]()
    else:
      print("Invalid answer! try again")
      self.Dashboard()

  # Method to register a new product in database
  def RegisterProduct(self):
    os.system('cls||clear')
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

  # Method to search for a product in specific or list they
  def SearchProduct(self):
    os.system('cls||clear')
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

  # Method to get what product infos will be changed
  def UpdateProduct(self, filter_procedure):
    os.system('cls||clear')
    print("Let's update!")

    procedures = [FindAllProducts, FindProductsByType]

    if filter_procedure == 0:
      products = procedures[filter_procedure]()
    else:
      products = procedures[1](filter_procedure)

    if products != "Products don't exists":
      df = pandas.DataFrame(data=products)
      print("\n")
      print(df.transpose())
      print("\n")
    else:
      print("Products not found")
      input("Press any key to try again")
      self.UpdateProduct(0)

    print("Type the product code to update: ")
    answer = input(
              "1 - Show all products  "
              "2 - Show all series  "
              "3 - Show all movies  "
              "4 - Show all documentaries  "
              "5 - Back to Dashboard\n")
    if len(answer) == 6:
      self.ChangeProductOnDb(answer)
    else:
      if int(answer) > 0 and int(answer) < 5:
        self.UpdateProduct(int(answer) - 1)
      elif int(answer) == 5:
        self.Dashboard()
      else:
        print("Invalid answer, try again")
        self.UpdateProduct(0)

  # Method who actually updates the product in database
  def ChangeProductOnDb(self, code):
    product = FindByCode(code)
    df = pandas.DataFrame(data=product, index=[0])
    print("Okay, this code represents that product:")
    print("\n")
    print(df)
    print("\n")

    while True:
      answer = int(input(
              "What element do you want to update?\n"
              "1 - Name  "
              "2 - Type  "
              "3 - Price  "
              "4 - Can Buy\n"))
        
      if answer > 5 and answer < 0:
        print("Invalid answer, try again")
      else:
        break

    code = product["code"]

    del product["code"]

    product_keys = list(product)
    key = product_keys[answer-1]

    new_value = input(f"Alright, at moment the value is {product[key]}, what'll be the new value?\n")
    product[key] = new_value

    file = open("./db/db.json", "r+", encoding="utf8")
    db = json.load(file)
    file.close()

    db["products"][code] = product
    if db["products"][code]["type"] == "serie":
      db["products"][code]["type"] = 1
    elif db["products"][code]["type"] == "movie":
      db["products"][code]["type"] = 2
    else:
      db["products"][code]["type"] = 3

    to_change = open("./db/db.json", "w", encoding="utf8")
    json.dump(db, to_change, indent=2, ensure_ascii=False)
    to_change.close()

    print("Atualizado!")

    answer = input("Do you want to update more? (1 - YES)\n")
    if answer == "1":
      self.ChangeProductOnDb(code)
    else:
      self.Dashboard()

  # Method to see all buys history
  def BuysHistory(self):
    print("History!!!")

  # Method to close application
  def Exit(self):
    exit()
#endregion

#region Interactions

#Instantiate App class
nerdFlix = NerdFlix()

if nerdFlix.user_type == "Customers":
  user_active = Customer(nerdFlix.active_user)
  user_active.Dashboard()
elif nerdFlix.user_type == "Employees":
  user_active = Employeer(nerdFlix.active_user)
  user_active.Dashboard()
#endregion