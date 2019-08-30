import requests

class FilmLocationsAPI(object):
  url = "https://data.sfgov.org/resource/wwmu-gmzc.json"
  # TODO: API tokens should not be commited to the code
  api_token = "IegozTH7xlN32jXMfFpqR8x1K"

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