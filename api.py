import requests
import os

class FilmLocationsAPI(object):
  url = "https://data.sfgov.org/resource/wwmu-gmzc.json"

  def __init__(self, api_token):
    if not api_token:
      raise Exception("Please provide a valid API token to fetch film locations")

    self.api_token = api_token

  def _get_headers(self):
    return {
      "X-App-Token": self.api_token
    }

  def fetch_film_locations(self, query="", limit=10):
    # Cover empty strings
    if not limit or limit == "":
      limit = 10

    print(f"Fetching film locations: query: {query}, limit {limit}")
    response = requests.get(self.url, params={"$q": query, "$limit": limit}, headers=self._get_headers())
    return response.json()