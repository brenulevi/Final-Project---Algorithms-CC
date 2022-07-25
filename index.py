def getLocation():
  from geopy.geocoders import Nominatim
  import geocoder

  Nomi_locator = Nominatim(user_agent="My app")

  my_location = geocoder.ip("me")

  latitude = my_location.geojson['features'][0]['properties']['lat']
  longitude = my_location.geojson['features'][0]['properties']['lng']

  location = str(Nomi_locator.reverse(f"{latitude}, {longitude}")).split(",")

  return location

class NerdFlix:
  def __init__(self) -> None:
    self.uf = getLocation()[7].strip(" ")
    pass

myClass = NerdFlix()

print(myClass.uf)