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
  query, limit = get_qs(event)

  try:
    validate_qs(query, limit)
  except Exception as e:
    return {
      "statusCode": 401,
      "body": json.dumps({
        "error": str(e)
      })
    }

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

def validate_qs(query, limit):
  if query and not re.match(ALPHA_REGEX, query):
    raise Exception("Please provide an alphanumeric value in the search parameter")

  if limit and not re.match(INTEGER_REGEX, limit):
    raise Exception("Please provide an integer value in the limit parameter")
