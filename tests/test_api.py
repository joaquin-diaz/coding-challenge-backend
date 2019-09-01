import unittest
from unittest.mock import patch, MagicMock

from api import FilmLocationsAPI
from .common import mock_response

class TestAPI(unittest.TestCase):
  def test_init_empty_api_key(self):
    with self.assertRaises(Exception) as e:
      FilmLocationsAPI(api_token=None)
      self.assertEqual(
        "Please provide a valid API token to fetch film locations", str(e),
        "It should fail to initialize without an api token"
        )

  def test_get_headers(self):
    api = FilmLocationsAPI(api_token='some_token')

    headers = api._get_headers()

    self.assertEqual(headers, {
      'X-App-Token': 'some_token'
    }, "It should set authentication header")

  @patch('api.requests')
  def test_get_locations_default_qs(self, mock_requests):
    mock_json = MagicMock()
    mock_json.return_value = mock_response
    mock_requests.get.return_value = MagicMock(
      json=mock_json 
    )

    api = FilmLocationsAPI(api_token='some_token')    
    response = api.fetch_film_locations()

    self.assertListEqual(response, mock_response)
    mock_requests.get.assert_called
    mock_requests.get.assert_called_with(
      api.url, 
      params={"$q": "", "$limit": "10"}, 
      headers={'X-App-Token': 'some_token'}
    )
    mock_json.assert_called

  @patch('api.requests')
  def test_get_locations_given_qs(self, mock_requests):
    mock_json = MagicMock()
    mock_json.return_value = mock_response
    mock_requests.get.return_value = MagicMock(
      json=mock_json 
    )

    api = FilmLocationsAPI(api_token='some_token')    
    response = api.fetch_film_locations('venom', 50)

    self.assertListEqual(response, mock_response)
    mock_requests.get.assert_called
    mock_requests.get.assert_called_with(
      api.url, 
      params={"$q": "venom", "$limit": 50}, 
      headers={'X-App-Token': 'some_token'}
    )
    mock_json.assert_called