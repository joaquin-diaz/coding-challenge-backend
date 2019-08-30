import json
from api import FilmLocationsAPI

def handler(event, context):
  api = FilmLocationsAPI()
  query, limit = get_qs(event)

  body = json.dumps(api.fetch_film_locations(query, limit))

  return {
    "statusCode": 200,
    "body": body
  }

def get_qs(event):
  query_string = event.get('queryStringParameters', None)

  if not query_string:
    return None, None

  return query_string.get('query', None), query_string.get('limit', None)