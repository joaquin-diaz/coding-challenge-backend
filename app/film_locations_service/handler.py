import json
from .api import FilmLocationsAPI

def handler(event, context):
  api = FilmLocationsAPI()

  return json.dumps(api.fetch_film_locations())