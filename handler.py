import json
import re
import os

from api import FilmLocationsAPI
from geocode import append_coordinates_to_locations

ALPHA_REGEX = r'^\w+$'
INTEGER_REGEX = r'^[0-9]+$'

def handler(event, context):
  api_token = os.environ.get('SF_LOCATIONS_API_KEY', None)

  api = FilmLocationsAPI(api_token)
  query, limit, include_coordinates = get_qs(event)

  try:
    validate_limit(limit, include_coordinates)
  except Exception as e:
    return {
      "statusCode": 400,
      "body": json.dumps({
        "error": str(e)
      })
    }

  locations = api.fetch_film_locations(query, limit)
  # Some locations don't have an address
  cleaned_locations = [location for location in locations if location.get('locations', None)]

  if include_coordinates == "true":
    append_coordinates_to_locations(cleaned_locations)

  return {
    "statusCode": 200,
    "body": json.dumps(cleaned_locations)
  }

def get_qs(event):
  query_string = event.get('queryStringParameters', None)

  if not query_string:
    return None, None, None

  return query_string.get('query', None), query_string.get('limit', None), query_string.get('include_coordinates', None)

def validate_limit(limit, include_coordinates):
  if limit and not re.match(INTEGER_REGEX, limit):
    raise Exception("Please provide an integer value in the limit parameter")

  if limit and include_coordinates == "true" and int(limit) > 10:
    raise Exception("Please provide a limit between 0 and 10 when including locations")