import os
import googlemaps

google_api_key = os.environ.get('GOOGLE_API_KEY', None)
# Lambdas can keep a small in-memory cache if the time between requests is small enough
# It's not 100% effective but it's worth trying
in_memory_geocode_cache = {}

def append_coordinates_to_locations(locations):
  '''
  Appends coordinates to a list of locations by calling Google's Geocode API

  Args:
    locations (dict): list of film locations. See format at API 
  '''
  for location in locations:
    address = location['locations']
    coordinates = None

    cached_coordinates = in_memory_geocode_cache.get(address, None)
    if cached_coordinates:
      coordinates = cached_coordinates
      print(f"Fetched address {address} from cache")
    else:
      coordinates = _get_coordinates_from_address(address)
      in_memory_geocode_cache[address] = coordinates

    location['coordinates'] = coordinates

  return locations

def _get_coordinates_from_address(address):
  '''
  Gets coordinates from Google's API

  Args:
    address (str): Address that we want the coordinates from

  Returns:
    coordinates: (dict): A dict with lat and lng values
  '''
  if not google_api_key:
    raise Exception("Please provide a valid Google API token")

  gmaps = googlemaps.Client(key=google_api_key)
  geocode_response = gmaps.geocode(f"{address}, San Francisco, CA")

  return geocode_response[0]['geometry']['location'] 