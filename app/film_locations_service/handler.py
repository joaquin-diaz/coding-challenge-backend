import json
from .api import FilmLocationsAPI

def handler(event, context):
  api = FilmLocationsAPI()
  query, limit = get_qs(event)

  return json.dumps(api.fetch_film_locations(query, limit))

def get_qs(event):
  query_string = event['queryStringParameters']
  return query_string.get('query', None), query_string.get('limit', None)