import requests

class FilmLocationsAPI(object):
  url = "https://data.sfgov.org/resource/wwmu-gmzc.json"

  def fetch_film_locations(self, query = "", limit = 100):
    response = requests.get(self.url, params={"$q": query, "$limit": limit})
    return response.json()