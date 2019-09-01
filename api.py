import requests
import os

class FilmLocationsAPI(object):
  '''
  Creates an instance of the API Client

  Args:
    api_token (str): SF Locations API Token
  
  Returns:
    FilmLocationsAPI instance
  '''
  url = "https://data.sfgov.org/resource/wwmu-gmzc.json"

  def __init__(self, api_token):
    if not api_token:
      raise Exception("Please provide a valid API token to fetch film locations")

    self.api_token = api_token

  def _get_headers(self):
    return {
      "X-App-Token": self.api_token
    }

  def fetch_film_locations(self, query="", limit="10"):
    '''
    Fetches film locations based on query. It needs to be an exact match, if the query is empty
    it returns all films up to the limit

    Args:
      query (str): query to match 
      limit (str): max number of films to fetch
    
    Returns:
      films ([dict]): list of films with this format:
        {
          "title": "180",
          "release_year": "2011",
          "locations": "Epic Roasthouse (399 Embarcadero)",
          "production_company": "SPI Cinemas",
          "director": "Jayendra",
          "writer": "Umarji Anuradha, Jayendra, Aarthi Sriram, & Suba ",
          "actor_1": "Siddarth",
          "actor_2": "Nithya Menon",
          "actor_3": "Priya Anand"
        }
    '''
    # Cover empty strings
    if not limit or limit == "":
      limit = 10

    print(f"Fetching film locations: query: {query}, limit {limit}")
    response = requests.get(self.url, params={"$q": query, "$limit": limit}, headers=self._get_headers())
    return response.json()