import json
import os
import googlemaps

from api import FilmLocationsAPI

google_api_key = os.environ.get('GOOGLE_API_KEY', None)

def handler(event, context):
  api_token = os.environ.get('SF_LOCATIONS_API_KEY', None)

  api = FilmLocationsAPI(api_token)
  query, limit = get_qs(event)

  locations = api.fetch_film_locations(query, limit)
  append_coordinates_to_locations(locations)

  return {
    "statusCode": 200,
    "body": json.dumps(locations)
  }

def get_qs(event):
  query_string = event.get('queryStringParameters', None)

  if not query_string:
    return None, None

  return query_string.get('query', None), query_string.get('limit', None)

def append_coordinates_to_locations(locations):
  for location in locations:
    address = locations[0]['locations']
    coordinates = get_coordinates_from_address(address)
    location['coordinates'] = coordinates

  return locations

def get_coordinates_from_address(address):
  if not google_api_key:
    raise Exception("Please provide a valid Google API token")

  gmaps = googlemaps.Client(key=google_api_key)
  geocode_response = gmaps.geocode(f"{address}, San Francisco, CA")

  return geocode_response[0]['geometry']['location'] 
