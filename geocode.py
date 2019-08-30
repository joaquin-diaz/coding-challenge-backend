import os
import googlemaps

google_api_key = os.environ.get('GOOGLE_API_KEY', None)

def append_coordinates_to_locations(locations):
  for location in locations:
    address = locations[0]['locations']
    coordinates = _get_coordinates_from_address(address)
    location['coordinates'] = coordinates

  return locations

def _get_coordinates_from_address(address):
  if not google_api_key:
    raise Exception("Please provide a valid Google API token")

  gmaps = googlemaps.Client(key=google_api_key)
  geocode_response = gmaps.geocode(f"{address}, San Francisco, CA")

  return geocode_response[0]['geometry']['location'] 